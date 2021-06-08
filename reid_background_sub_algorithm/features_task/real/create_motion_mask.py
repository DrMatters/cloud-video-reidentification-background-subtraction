import abc
import os
import pathlib
import shutil
from typing import List, Tuple, Callable

import cv2


class BaseTransformer:
    @abc.abstractmethod
    def transform(self, entity):
        pass

    @staticmethod
    @abc.abstractmethod
    def create():
        pass


class OpencvMOG(BaseTransformer):
    def __init__(self):
        self.mog: cv2.BackgroundSubtractorMOG2 = \
            cv2.createBackgroundSubtractorMOG2()

    @staticmethod
    def create():
        return OpencvMOG()

    def transform(self, entity):
        return self.mog.apply(entity)


class MotionMaskCreator:
    def __init__(self, base_folder: str = './', file_extension: str = '.jpeg',
                 output_subfolder_name: str = 'masks'):
        self._extension = file_extension
        self._base_folder = base_folder
        self._output_subfolder = output_subfolder_name

    @staticmethod
    def _get_all_leafs(root) -> List:
        # 0 - current path
        # 1 - subfolders
        # 2 - files
        res = [folder[0] for folder in os.walk(root) if len(folder[1]) == 0]
        return res

    def _get_files_from_leaf(self, folder_path):
        elems = list(os.walk(folder_path))
        if len(elems[0][1]) > 1:
            raise IndexError("Folder is not a leaf")
        elems = elems[0][2]
        filenames = [filename for filename in elems
                     if filename.endswith(self._extension)]
        filenames = sorted(filenames)
        full_paths = [os.path.join(folder_path, fn) for fn in filenames]
        return full_paths, filenames

    def _prepare_folder(self, folder_path, exists_error=False) -> \
            Tuple[List[str], List[str], pathlib.Path]:
        full_paths, filenames = self._get_files_from_leaf(folder_path)
        masks_folder = pathlib.Path(folder_path) / self._output_subfolder
        if masks_folder.exists():
            if exists_error:
                raise FileExistsError(f'Masks older exists: {masks_folder}')
            else:
                shutil.rmtree(masks_folder)
        masks_folder.mkdir()
        return full_paths, filenames, masks_folder

    def do_things(self, read_callback: Callable, save_callback: Callable,
                  create_transformer: Callable[[], BaseTransformer]):
        leafs = self._get_all_leafs(self._base_folder)
        leafs = [l for l in leafs if not l.endswith('masks')]
        for leaf in leafs:
            print(f'Current leaf: {leaf}')
            full_paths, filenames, masks_folder = self._prepare_folder(leaf)
            transformer = create_transformer()
            for f_path, f_name in zip(full_paths, filenames):
                result_path = masks_folder / f_name
                entity = read_callback(f_path)
                tr_entity = transformer.transform(entity)
                save_callback(str(result_path), tr_entity)


if __name__ == '__main__':
    a = MotionMaskCreator('E:\\datasets\\SAIVT-SoftBio\\Uncontrolled')
    mog: cv2.BackgroundSubtractorMOG2 = cv2.createBackgroundSubtractorMOG2()
    a.do_things(cv2.imread, cv2.imwrite, OpencvMOG.create)
