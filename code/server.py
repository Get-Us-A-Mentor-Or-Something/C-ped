from os import path

from flask import Flask, g, session, redirect, request, url_for, jsonify, render_template, send_from_directory, escape
from flask_socketio import SocketIO, disconnect


def main():
    # The path to directory this code is ran in.
    CUR_PATH = path.dirname(path.abspath(__file__))

    # The port on which server is hosted.
    PORT = 8080
    # !!! FUN !!! DEBUG MODE. Gives access to most stuff on server, very dangerous to be put on production.
    DEBUG = False
    # Secret key used to encrypt requests and stuff.
    SECRET_KEY = "SUPER SECRET KEY WE'RE NOT ACTUALLY USING AND WHICH SHOULD BE PUT IN CONFIGS AS TO PROTECT FROM HACKERS AND STUFF"


    # The directory with all web-related templates.
    template_dir = path.join(CUR_PATH, '../templates')
    # The directory for static files, such as .css, client-side JavaScript.
    static_dir = path.join(CUR_PATH, '../static')

    app = Flask(__name__, template_folder=template_dir, static_url_path='')
    app.config['SECRET_KEY'] = SECRET_KEY
    # app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    socketio = SocketIO(app)


    @app.after_request
    def after_request(response):
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        # response.headers['Content-Security-Policy'] = "default-src 'self'"
        response.headers['X-Content-Type-Options'] = 'nosniff'
        # response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response


    @app.route('/')
    def index():
        return render_template("index.html")


    @app.route('/static/<path:path>')
    def send_static(path):
        return send_from_directory(static_dir, path)

    print(
        "=====\n" +
        "Server started on 0.0.0.0:" + str(PORT)
        )

    socketio.run(app, host='0.0.0.0', port=PORT, debug=DEBUG)
