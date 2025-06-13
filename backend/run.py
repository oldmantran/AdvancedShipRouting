print("Starting run.py")

try:
    from app import create_app
    print("Imported create_app successfully")
    app = create_app()
    print("App created")
except Exception as e:
    print("Error during app creation:", e)
    app = None

if __name__ == '__main__':
    if app:
        print("About to run Flask app")
        try:
            app.run(debug=True)
        except Exception as e:
            print("Error running Flask app:", e)
    else:
        print("Flask app was not created. Exiting.")