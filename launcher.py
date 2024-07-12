import os
import subprocess
import sys
import webbrowser
import time
import socket
import atexit

try:
    import win32event
    import win32api
    import winerror
except ImportError:
    print("Error: pywin32 package is required for Windows-specific functionality.")
    print("Please install it using 'pip install pywin32' and try again.")
    sys.exit(1)

# Ensure single instance
try:
    mutex = win32event.CreateMutex(None, 1, "FlaskAppLauncherMutex")
    if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
        print("Another instance of the application is already running.")
        sys.exit(1)
except Exception as e:
    print(f"Failed to create mutex: {e}")
    sys.exit(1)

def install_requirements():
    try:
        print("Installing requirements...")
        with open("requirements.txt", "r", encoding='utf-8-sig') as f:
            packages = f.readlines()
        
        for package in packages:
            package = package.strip()
            if package:
                print(f"Installing {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print("All requirements installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install requirements: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

def run_app():
    try:
        print("Starting the Flask app...")
        process = subprocess.Popen([sys.executable, "wsgi.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("Flask app has been started.")
        return process
    except Exception as e:
        print(f"Failed to start the Flask app: {e}")
        sys.exit(1)

def open_browser():
    try:
        print("Opening the default web browser...")
        webbrowser.open_new("http://127.0.0.1:5000")
        print("Default web browser opened.")
    except Exception as e:
        print(f"Failed to open the web browser: {e}")

def check_server_running():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', 5000)) == 0

# Define cleanup function
def cleanup():
    print("Cleaning up...")
    # Ensure the Flask server process is terminated
    if 'process' in locals() and process.poll() is None:
        process.terminate()

# Register cleanup function to be called on exit
atexit.register(cleanup)

if __name__ == "__main__":
    print("Launcher script started.")
    
    # Install requirements if not already installed
    # install_requirements()

    print("Running the Flask app...")
    process = run_app()

    print("Waiting for the Flask app to start...")
    for _ in range(30):  # Try for up to 30 seconds
        if check_server_running():
            print("Server is running, opening the browser.")
            open_browser()
            break
        time.sleep(1)
    else:
        print("Server did not start within the expected time.")
        try:
            stdout, stderr = process.communicate(timeout=10)
            print(f"Flask app output: {stdout}")
            print(f"Flask app errors: {stderr}")
        except subprocess.TimeoutExpired:
            print("Flask app did not provide output within the timeout period.")
        process.terminate()
        sys.exit(1)

    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    rc = process.poll()

    print("Flask app has exited.")
