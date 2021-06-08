import functools
from typing import List

import cv2
import numpy as np

from features_task.real import non_ml_features


def resolve_max_response(keypoints: List[cv2.KeyPoint],
                         descriptors: List[np.ndarray]) -> np.ndarray:
    index = range(len(keypoints))
    max_index = max(index, key=lambda item: keypoints[item].response)
    return descriptors[max_index]


def resolve_first(keypoints: List[cv2.KeyPoint],
                  descriptors: List[np.ndarray]) -> np.ndarray:
    return descriptors[0]


orb: cv2.ORB = cv2.ORB_create()
sift: cv2.xfeatures2d_SIFT = cv2.xfeatures2d.SIFT_create()
surf: cv2.xfeatures2d_SURF = cv2.xfeatures2d.SURF_create()

dac_orb = functools.partial(orb.detectAndCompute, mask=None)
sift_orb = functools.partial(sift.detectAndCompute, mask=None)
surf_orb = functools.partial(surf.detectAndCompute, mask=None)

orb_downs = non_ml_features.DownsamplingFill(
    8, dac_orb, resolve_max_response
)
sift_downs = non_ml_features.DownsamplingFill(
    8, sift_orb, resolve_max_response
)
surf_downs = non_ml_features.DownsamplingFill(
    8, surf_orb, resolve_max_response
)

img = cv2.imread('../data/images/human/3.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

res = [orb_downs.downsample(gray), sift_downs.downsample(gray), surf_downs.downsample(gray)]

print('Finished')
