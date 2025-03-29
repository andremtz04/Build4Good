import numpy as np
import cv2
import time
import os
from ultralytics import YOLO

FRAMERATE = 10
CONFIDENCE_THRESHOLD = 0.5
persons_detected = 0

# Initialize trained YOLOv8 model
base_dir = os.path.dirname(__file__)
model_path = os.path.join(base_dir, "models", "best.pt")  # Adjust path if needed
model = YOLO(model_path)

def start_camera_capture():
    print("Starting camera...")

    # Open webcam video stream
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    cap.set(cv2.CAP_PROP_FPS, FRAMERATE)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame. Exiting...")
            break

        # Resize for faster detection
        frame = cv2.resize(frame, (640, 480))

        # Convert to grayscale for faster detection
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # Use YOLOv8 for detecting people
        results = model(frame)

        # Extract bounding boxes
        boxes = []
        for result in results:
            for box in result.boxes:
                conf = box.conf[0].item()
                if conf >= CONFIDENCE_THRESHOLD:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])  # Convert to int
                    boxes.append([x1, y1, x2, y2])

        global persons_detected
        persons_detected = len(boxes)

        # Draw bounding boxes on the frame
        for (xA, yA, xB, yB) in boxes:
            cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)

        # Display the frame
        cv2.imshow('Human Detection', frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Control frame rate
        time.sleep(1 / FRAMERATE)

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)  # Ensure window closes properly
    print("Camera closed.")

# Run the function if this script is executed directly
if __name__ == "__main__":
    start_camera_capture()
