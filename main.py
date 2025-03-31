import threading, subprocess
import cv2
import json
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # import from other folders

from back_end.human_detection import queue_tracker

def run_camera():
    # Open the camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to grab frame.")
            break

        # Here, you can add your detection logic
        # Example: Resize the frame
        frame = cv2.resize(frame, (640, 480))

        # Display the frame
        cv2.imshow("Camera", frame)

        # Close the camera window when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Function to run the Electron app after saving the queue time
def run_electron_app():
    try:
        # Get the current directory and build the path to main.js
        current_directory = os.getcwd()
        electron_app_path = os.path.join(current_directory, 'front_end', 'main.js')

        # Verify the Electron app path
        print(f"Attempting to launch Electron app at: {electron_app_path}")

        # Check if the Electron app file exists
        if not os.path.exists(electron_app_path):
            print(f"Error: The Electron app file does not exist at {electron_app_path}")
            return

        # Full path to the Electron binary
        electron_binary_path = os.path.join(current_directory, 'node_modules', '.bin', 'electron')

        # Debugging: Verify that Electron binary exists
        print(f"Electron binary path: {electron_binary_path}")
        if not os.path.exists(electron_binary_path):
            print(f"Error: Electron binary not found at {electron_binary_path}")
            return

        # Run the Electron app using the full path to the Electron binary
        result = subprocess.run(
            [electron_binary_path, electron_app_path],  # Use the full path to Electron binary
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Debugging: Check if there is any output from Electron
        print("Electron Standard Output:")
        print(result.stdout.decode())  # Print standard output from Electron

        print("Electron Standard Error (if any):")
        print(result.stderr.decode())  # Print any errors from Electron if any

    except subprocess.CalledProcessError as e:
        print(f"Error while running Electron app: {e}")
        print("Error Output:", e.stderr.decode())
    except Exception as ex:
        print(f"Unexpected error: {ex}")
        
# Main function to calculate queue time and launch Electron
def main():
    try:
        # Step 1: Calculate queue time
        queue_time = queue_tracker.get_queue_time()
        print(f"Queue Time Calculated: {queue_time}")

        # Step 2: Save the queue time to a JSON file
        queue_time_data = json.dumps({"queue_time": queue_time})
        queue_time_file_path = os.path.join(os.getcwd(), 'front_end', 'queue_time.json')

        print(f"Saving queue time data to: {queue_time_file_path}")
        with open(queue_time_file_path, "w") as f:
            f.write(queue_time_data)

        print(f"Queue time saved to {queue_time_file_path}")

        # Step 3: Run the camera in a background thread
        camera_thread = threading.Thread(target=run_camera)
        camera_thread.start()

        # Step 4: Launch the Electron app
        print("Launching Electron app...")
        run_electron_app()

    except Exception as e:
        print(f"Error in main function: {e}")

# Run the script
if __name__ == "__main__":
    main()