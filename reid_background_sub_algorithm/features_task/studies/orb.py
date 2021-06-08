import operator

import cv2

import utils

img = cv2.imread('../data/images/human/3.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

orb: cv2.ORB = cv2.ORB_create()
keypoints, des = orb.detectAndCompute(gray, None)

keypoints = sorted(keypoints, key=operator.attrgetter('response'), reverse=True)

utils.draw_percent_steps(keypoints, img, 10)
