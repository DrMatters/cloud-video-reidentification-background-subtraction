import cv2

import utils

img = cv2.imread('../data/images/human/3.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

surf = cv2.xfeatures2d.SURF_create(400)
keypoints = surf.detect(gray, None)

utils.draw_percent_steps(keypoints, gray, 10)
