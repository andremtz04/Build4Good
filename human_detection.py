import numpy as np
import cv2

cv2.startWindowThread()
cap = cv2.VideoCapture(0)

while(True):
    # read frame
    ret, frame = cap.read()

    # manipulate frame
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    ret,frame = cv2.threshold(frame,80,255,cv2.THRESH_BINARY)

    # display frame
    cv2.imshow("frame", frame)

    # break loop if user presses q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
cv2.waitKey(1)