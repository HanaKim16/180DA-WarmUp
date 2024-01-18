import cv2
import numpy as np

#cap = cv2.VideoCapture("longer ducky.mp4") #for Q1
cap = cv2.VideoCapture("flash ducky.mp4")   #for Q2

# Question 1
# Colors Threshold (0, 48, 119), (255, 255, 255)
#HSV is clearer here because there is less contrast in the video.
#Without the flash, the object appears clearer in HSV because it isn't bright
# I believe the threshold range is large - meaning the gaps in between the min and max are quite large.
# observe the threshold numbers above, the minimum values are quite low whereas the maximum values were maxed.

# Question 2 With Flash
# Colors Threshold (0, 69, 124), (188, 255, 255)
# The object starts to appear in the mask more quickly (the red filter doesn't need to maximize)
# I believe this occurs because of the bright light that makes the object more detectible



success, frame = cap.read()

def nothing(x):
    pass

cv2.namedWindow("Trackbars")

cv2.createTrackbar("L-H","Trackbars",0,255,nothing)
cv2.createTrackbar("L-S","Trackbars",0,255,nothing)
cv2.createTrackbar("L-V","Trackbars",0,255,nothing)
cv2.createTrackbar("U-H","Trackbars",0,255,nothing)
cv2.createTrackbar("U-S","Trackbars",0,255,nothing)
cv2.createTrackbar("U-V","Trackbars",0,255,nothing)

while True:
    success, frame = cap.read()
    
    frame = cv2.resize(frame, (600, 400))

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos("L-H","Trackbars")
    l_s = cv2.getTrackbarPos("L-S","Trackbars")
    l_v = cv2.getTrackbarPos("L-V","Trackbars")
    u_h = cv2.getTrackbarPos("U-H","Trackbars")
    u_s = cv2.getTrackbarPos("U-S","Trackbars")
    u_v = cv2.getTrackbarPos("U-V","Trackbars")

    lower = np.array([l_h,l_s,l_v])
    upper = np.array([u_h,u_s,u_v])
    
    mask = cv2.inRange(hsv, lower, upper)

    result = cv2.bitwise_and(frame, frame, mask = mask)

    cv2.imshow("Frame", frame)
    cv2.imshow("HSV", hsv)
    cv2.imshow("Mask", mask)
    cv2.imshow("Result", result)

    key = cv2.waitKey(1)
    if key == 27:
        break