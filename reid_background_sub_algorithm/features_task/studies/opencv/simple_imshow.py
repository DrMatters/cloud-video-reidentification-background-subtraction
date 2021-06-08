import cv2

image = cv2.imread('./data/images/test.jpeg', cv2.IMREAD_GRAYSCALE)
if image is None:
    raise AssertionError("Image not open")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
cv2.imshow('test image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
