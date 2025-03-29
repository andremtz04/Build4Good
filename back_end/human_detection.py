import numpy as np
import cv2

from queue_calculator import Queue_Calculator
import multiprocessing

FRAMERATE = 5

########## Our "main" file ################
from constants import FRAMERATE

def main():
    # open webcam video stream
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, FRAMERATE)

    # refresh queue counting 5 times/sec, 10 min estimated per person
    queue_tracker = Queue_Calculator(5, 10)

    # initialize the HOG descriptor/person detector
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    cv2.startWindowThread()

    # open webcam video stream
    cap = cv2.VideoCapture(0)

    # the output will be written to output.avi
    # out = cv2.VideoWriter(
    #     'output.avi',
    #     cv2.VideoWriter_fourcc(*'MJPG'),
    #     15.,
    #     (640,480))

    # persons_detected becomes shared value across processes
    persons_detected = multiprocessing.Value('i', 0)

    # pass in persons_detected so its available to queue_tracker object
    process = multiprocessing.Process(target=queue_tracker.start_tracking, args=(persons_detected,))
    process.start()

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # resizing for faster detection
        frame = cv2.resize(frame, (640, 480))
        # using a greyscale picture, also for faster detection
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # detect people in the image
        # returns the bounding boxes for the detected objects
        boxes, weights = hog.detectMultiScale(frame, winStride=(8,8) )

        boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

        # ensure safe updates
        with persons_detected.get_lock():
            persons_detected.value = len(boxes)
            #print("Persons detected:", persons_detected)

        for (xA, yA, xB, yB) in boxes:
            # display the detected boxes in the colour picture
            cv2.rectangle(frame, (xA, yA), (xB, yB),
                            (0, 255, 0), 2)
        
        # Write the output video 
        #out.write(frame.astype('uint8'))

        # Display the resulting frame
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            queue_tracker.stop_tracking()
            process.terminate()
            process.join()
            break

    # When everything done, release the capture
    cap.release()
    # and release the output
    # out.release()
    # finally, close the window
    cv2.destroyAllWindows()
    cv2.waitKey(1)

# magic stuff 
if __name__ == "__main__":
    multiprocessing.set_start_method("spawn")
    main()