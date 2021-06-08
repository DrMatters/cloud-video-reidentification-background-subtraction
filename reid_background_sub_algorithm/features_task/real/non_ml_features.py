import collections
from typing import Callable, Tuple, List

import cv2
import albumentations as albu
import numpy as np


class DownsamplingFill:
    def __init__(self, cell_side_len: int,
                 detect_and_compute: Callable[[np.ndarray], Tuple[List[cv2.KeyPoint], np.ndarray]],
                 resolve_multiple: Callable[[List[cv2.KeyPoint], List[np.ndarray]], np.ndarray]):
        self._cell_side = cell_side_len
        self._extract = detect_and_compute
        self._resolve = resolve_multiple

    def downsample(self, image: np.array):
        keypoints, descriptors = self._extract(image)
        keypoints_of_cell = collections.defaultdict(list)
        descriptors_of_cell = collections.defaultdict(list)
        keypoints_index = {}
        for index, keypoint in enumerate(keypoints):
            # save mapping from cv2.KeyPoint to it's index to find descriptor later
            keypoints_index[keypoint.pt + (keypoint.angle,)] = index
            cell_x = int(keypoint.pt[0] // self._cell_side)
            cell_y = int(keypoint.pt[1] // self._cell_side)
            keypoints_of_cell[(cell_x, cell_y)].append(keypoint)
            descriptors_of_cell[(cell_x, cell_y)].append(descriptors[index])

        grid_shape = np.asarray(image.shape) // self._cell_side
        # add one dimension for descriptor vector
        grid_shape = np.append(grid_shape, descriptors.shape[1])
        grid = np.zeros(grid_shape, dtype=descriptors.dtype)

        for cell, cell_keypoints in keypoints_of_cell.items():
            cell_descriptors = descriptors_of_cell[cell]
            descriptor = self._resolve(cell_keypoints, cell_descriptors)
            grid[cell[1], cell[0]] = descriptor
        return grid

class DescriptorsPreprocessing:
    def __init__(self,
                 detect_and_compute: Callable[[np.ndarray], Tuple[List[cv2.KeyPoint], np.ndarray]]):
        self._extract = detect_and_compute

    def _extract_descriptors(self, image, **kwargs):
        keypoints, cur_descriptors = self._extract(image)
        return cur_descriptors

    def get_preprocessing(self):
        _transform = [
            albu.Lambda(image=self._extract_descriptors)
        ]
        return albu.Compose(_transform)
