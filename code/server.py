import mimetypes

import global_vars

from os import path

from flask import (
    Flask,
    render_template,
    send_from_directory,
    request,
    session,
)
from flask_socketio import SocketIO, disconnect

from client import Client


def get_connections_by_ip(ip):
    if ip not in global_vars.client_infos_by_ip.keys():
        return 0

    return sum(
        client_info.clients_connected
        for client_info in global_vars.client_infos_by_ip[ip]
    )


def disconnect_message(request, reason=None):
    print(
        "Disconnected("
        + str(global_vars.client_count)
        + "/"
        + str(global_vars.max_client_count)
        + ") user("
        + str(request.remote_addr)
        + ")."
        + (" Reason: " + reason)
        if reason
        else ""
    )


def main(CFG):
    # The path to directory this code is ran in.
    CUR_PATH = path.dirname(path.abspath(__file__))

    server_CFG = CFG["Server"]

    # The IP to run server on.
    IP = server_CFG.get("ip", "0.0.0.0")
    # The port on which server is hosted.
    PORT = server_CFG.getint("port", 8080)
    # !!! FUN !!! DEBUG MODE. Gives access to most stuff on server,
    # very dangerous to be put on production.
    DEBUG = server_CFG.getboolean("debug", False)
    # Secret key used to encrypt requests and stuff.
    SECRET_KEY = server_CFG.get("secret_key")

    # The directory with all web-related templates.
    template_dir = path.join(CUR_PATH, "../templates")
    # The directory for static files, such as .css, client-side JavaScript.
    static_dir = path.join(CUR_PATH, "../static")

    mimetypes.init()

    # So it's not system-dependant.
    mimetypes.add_type("text/css", ".css")
    mimetypes.add_type("text/javascript", ".js")
    mimetypes.add_type("text/html", ".html")

    app = Flask(__name__, template_folder=template_dir, static_url_path="")
    app.config["SECRET_KEY"] = SECRET_KEY

    # app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    socketio = SocketIO(app)

    @app.after_request
    def after_request(response):
        response.headers[
            "Strict-Transport-Security"
        ] = "max-age=31536000; includeSubDomains"
        # response.headers['Content-Security-Policy'] = "default-src 'self'"
        response.headers["X-Content-Type-Options"] = "nosniff"
        # response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/static/<path:file_path>")
    def send_static(file_path):
        file_mimetype = mimetypes.guess_type(file_path)[0]

        return send_from_directory(
            static_dir,
            file_path,
            mimetype=file_mimetype
        )

    @socketio.on("connect")
    def on_connect(methods=["GET", "POST"]):
        if (
            global_vars.max_client_count >= 0
            and global_vars.client_count + 1 > global_vars.max_client_count
        ):
            disconnect_message(request, "Server overcrowded")
            disconnect(request.sid)
            return

        if (
            global_vars.max_clients_per_ip >= 0
            and get_connections_by_ip(request.remote_addr)
            >= global_vars.max_clients_per_ip
        ):
            disconnect_message(request, "Too many connections on one IP")
            disconnect(request.sid)
            return

        client = Client(session, request)
        client.on_connect()

    @socketio.on("disconnect")
    def on_disconnect(methods=["GET", "POST"]):
        if request.sid in global_vars.clients_by_sid.keys():
            global_vars.clients_by_sid[request.sid].on_disconnect()

    print("=====\n" + "Server starting on " + str(IP) + ":" + str(PORT))

    socketio.run(app, host=IP, port=PORT, debug=DEBUG)
