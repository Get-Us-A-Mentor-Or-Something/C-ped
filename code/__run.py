def run():
    # see server.py for more detail, all server-related stuff is handled there.
    import server


if __name__ == "__main__":
    # Semi-automatic backend restarting in case it dropped for any reason.
    while True:
        try:
            run()

        # Anything in run() called for a forced 
        except SystemExit:
            break

        # Exceptions displaying.
        except Exception as err:
            try:
                exc_info = sys.exc_info()
            finally:
                # Display the *original* exception
                traceback.print_exception(*exc_info)
                del exc_info

        stopper = input().lower()
        if stopper == "q" or stopper == "quit":
            break

    print("Stopping server...")
