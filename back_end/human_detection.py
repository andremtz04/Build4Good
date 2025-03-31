import numpy as np
import cv2
import os
from ultralytics import YOLO

from queue_calculator import Queue_Calculator

########## Our "main" file ################
from constants import FRAMERATE, CONFIDENCE_THRESHOLD

def start_camera_capture():
    # open webcam video stream
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, FRAMERATE)

    # refresh queue counting 5 times/sec, 10 min estimated per person
    queue_tracker = Queue_Calculator(5, 10)

    # Load the trained model to detect humans
    base_dir = os.path.dirname(__file__)
    model_path = os.path.join(base_dir, "models", "best.pt")
    model = YOLO(model_path)

    cv2.startWindowThread()

    # open webcam video stream
    cap = cv2.VideoCapture(0)

    # the output will be written to output.avi
    # out = cv2.VideoWriter(
    #     'output.avi',
    #     cv2.VideoWriter_fourcc(*'MJPG'),
    #     15.,
    #     (640,480))

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # resizing for faster detection
        frame = cv2.resize(frame, (640, 480))
        # using a greyscale picture, also for faster detection
        # gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # detect people in the image
        # returns the bounding boxes for the detected objects
            #boxes, weights = hog.detectMultiScale(frame, winStride=(8,8) )
            #boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
        
        # Use YOLOv8 model to detect people
        results = model(frame)

        # Extract bounding boxes
        boxes = []
        for result in results:
            for box in result.boxes:
                conf_score = box.conf[0].item()
                if conf_score >= CONFIDENCE_THRESHOLD:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])  # Convert to int
                    boxes.append([x1, y1, x2, y2])

        # ensure safe updates
        # persons_detected = len(boxes)

        for (xA, yA, xB, yB) in boxes:
            # display the detected boxes in the colour picture
            cv2.rectangle(frame, (xA, yA), (xB, yB),
                            (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    # finally, close the window
    cv2.destroyAllWindows()
    cv2.waitKey(1)

if __name__ == "__main__":
    start_camera_capture()