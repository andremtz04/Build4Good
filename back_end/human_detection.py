import numpy as np
import cv2
import time

FRAMERATE = 10
persons_detected = 0

# Initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

def start_camera_capture():
    print("Starting camera...")

    # Open webcam video stream
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    cap.set(cv2.CAP_PROP_FPS, FRAMERATE)

    # Output video file
    out = cv2.VideoWriter(
        'output.avi',
        cv2.VideoWriter_fourcc(*'MJPG'),
        15.0,
        (640, 480)
    )

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

        # Detect people in the image
        boxes, weights = hog.detectMultiScale(frame, winStride=(8, 8))
        persons_detected = len(boxes)

        # Draw detected boxes
        for (x, y, w, h) in boxes:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Write to output video
        out.write(frame.astype('uint8'))

        # Display the frame
        cv2.imshow('Human Detection', frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Control frame rate
        time.sleep(1 / FRAMERATE)

    # Cleanup
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)  # Ensure window closes properly
    print("Camera closed.")

# Run the function if this script is executed directly
if __name__ == "__main__":
    start_camera_capture()
