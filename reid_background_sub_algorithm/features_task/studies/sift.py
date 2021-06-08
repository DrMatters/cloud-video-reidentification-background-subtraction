import operator

import cv2

import utils

img = cv2.imread('../data/images/human/3.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

sift = cv2.xfeatures2d.SIFT_create()
keypoints = sift.detect(gray, None)

keypoints = sorted(keypoints, key=operator.attrgetter('response'), reverse=True)

utils.draw_percent_steps(keypoints, gray, 10)
