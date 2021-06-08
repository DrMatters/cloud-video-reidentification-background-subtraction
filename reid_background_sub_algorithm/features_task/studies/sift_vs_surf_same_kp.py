import cv2

img = cv2.imread('../../data/images/human/3.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

sift: cv2.xfeatures2d_SIFT = cv2.xfeatures2d.SIFT_create()
surf: cv2.xfeatures2d_SURF = cv2.xfeatures2d.SURF_create()
sift_kp, sift_desc = sift.detectAndCompute(gray, None)
surf_kp, surf_desc = surf.compute(gray, sift_kp)

pass
