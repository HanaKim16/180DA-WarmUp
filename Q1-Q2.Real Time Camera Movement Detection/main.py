import cv2
from PIL import Image

from util import get_limits

yellow = [0, 255, 255]  # yellow in BGR colorspace
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lowerLimit, upperLimit = get_limits(yellow)

    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)

    mask_ = Image.fromarray(mask)

    bbox = mask_.getbbox()

    if bbox is not None:
        x1, y1, x2, y2 = bbox

        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

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