import numpy as np
import cv2

cap = cv2.VideoCapture(0)

#def bindbox(event, x, y, flags, param):
#    if event == cv2.EVENT_LBUTTONDOWN:
#        pixel_value = frame [y, x]
#        print("yellow RGB", pixel_value)

#cv2.namedWindow('Object Box')
#cv2.setMouseCallback('Object Box', bindbox)

RGB = np.array([255, 170, 51])

while(True):
    ret, frame = cap.read()

    if not ret:
        print("Can not find object.")
        break

    mask = cv2.inRange(frame, RGB, RGB)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        max_contour = max(contours, key=cv2.contourArea)

        x, y, w, h = cv2.boundingRect(max_contour)

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('Tracking Object', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()