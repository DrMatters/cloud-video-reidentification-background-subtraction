import cv2
import numpy as np
from skimage import exposure
from skimage.feature import hog

import utils

img = cv2.imread('../data/images/human/1.png')
hog_image: np.ndarray
fd, hog_image = hog(img, orientations=8, pixels_per_cell=(8, 8),
                    cells_per_block=(1, 1), visualize=True, multichannel=True)
# noinspection PyTypeChecker
hog_image = exposure.rescale_intensity(hog_image, in_range=(0, 10), out_range=np.uint8)
hog_image = hog_image.astype(np.uint8)
hog_image = cv2.cvtColor(hog_image, cv2.COLOR_GRAY2BGR)

added = cv2.add(hog_image, (img * 0.7).astype(np.uint8))
utils.simple_draw(added)
