import threading
import subprocess
import json
import os
import time
from back_end.human_detection import start_camera_capture, get_persons_detected
from back_end.queue_calculator import get_queue_time

def run_electron_app():
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the script's directory
    electron_path = os.path.join(script_dir, 'node_modules', 'electron', 'dist', 'electron.exe')
    app_path = os.path.join(os.getcwd(), 'front_end', 'main.js')

    try:
        print(f"Attempting to launch Electron app from: {os.path.abspath(app_path)}")
        subprocess.Popen([electron_path, app_path], shell=True)  # Use Popen to avoid blocking
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Function to start camera capture in a background thread
def start_camera_in_background():
    print("Starting camera in the background...")
    camera_thread = threading.Thread(target=start_camera_capture, daemon=True)  # Start camera capture in the background
    camera_thread.start()

# Main function to coordinate everything
def main():

    # Step 3: Start the camera in a background thread
    start_camera_in_background()

    # Step 4: Launch the Electron app
    print("Launching Electron app...")
    run_electron_app()

    # Step 5: Keep `main.py` alive so the camera thread doesn't stop
    while True:
            # Step 1: Calculate queue time
        queue_time = get_persons_detected()
    
            # Step 2: Save the queue time to a JSON file
        queue_time_data = json.dumps({"queue_time": queue_time})
        queue_time_file_path = os.path.join(os.getcwd(), 'front_end', 'queue_time.json')
        
        with open(queue_time_file_path, "w") as f:
            f.write(queue_time_data)
        time.sleep(1)

# Run the script
if __name__ == "__main__":
    main()
