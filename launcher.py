import os
import subprocess
import sys
import webbrowser
from threading import Timer

# def install_requirements():
#     try:
#         print("Installing requirements...")
#         with open("requirements.txt", "r", encoding='utf-8-sig') as f:
#             packages = f.readlines()
        
#         for package in packages:
#             package = package.strip()
#             if package:
#                 print(f"Installing {package}...")
#                 subprocess.check_call([sys.executable, "-m", "pip", "install", package])
#         print("All requirements installed successfully.")
#     except subprocess.CalledProcessError as e:
#         print(f"Failed to install requirements: {e}")
#         sys.exit(1)
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         sys.exit(1)

def run_app():
    try:
        print("Starting the Flask app...")
        os.system("python wsgi.py")
        print("Flask app has been started.")
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

if __name__ == "__main__":
    print("Launcher script started.")
    
    # print("Starting installation process...")
    # install_requirements()

    print("Delaying browser opening...")
    # Delay opening the browser to allow the server to start
    Timer(2, open_browser).start()

    print("Running the Flask app...")
    run_app()
