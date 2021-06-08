from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import glob
import os
import os.path as osp
import pathlib

import cv2
import xmltodict
from sklearn import model_selection
import numpy as np
from PIL import Image

import torchreid
from torchreid import data
from torchreid.data import VideoDataset


class Saivt_SoftBioImageReader(data.ImageReader):
    def read_image(self, path):
        # 1. get roi
        # 2. cut selected image
        path = pathlib.Path(path)
        directory = path.parents[0]
        _, camera_no = self.extract_num_right(directory.stem)
        _, subject_no = self.extract_num_right(directory.parents[0].stem)
        im_no = int(path.stem.split('-')[-1].split('.')[0])

        # TODO: index rois of all images to memory

        roi_info = self.get_roi(camera_no, directory, im_no, subject_no)
        l = int(roi_info['@l'])
        r = int(roi_info['@r'])
        t = int(roi_info['@t'])
        b = int(roi_info['@b'])

        image = cv2.imread(str(path))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        cropped = image[t:b, l:r]
        cropped = np.stack((cropped, np.zeros(cropped.shape[:2], np.uint8)),
                           axis=2)

        # cropped = Image.fromarray(cropped)
        return cropped

    @staticmethod
    def extract_num_right(s: str):
        head = s.rstrip('0123456789')
        tail = s[len(head):]
        return head, tail

    @staticmethod
    def get_roi(camera_no, directory, im_no, subject_no):
        with open(directory / f'Sub{subject_no}-Cam{camera_no}-ROI.xml') as roi_data:
            roi_dict = xmltodict.parse(roi_data.read())
            for im in roi_dict['SoftBiometricDatabaseSubjectView']['ROI']:
                # todo: binsearch?
                cur_no: str = im['@image']
                cur_no_int = int(cur_no.split('-')[-1].replace('.jpeg', ''))
                if cur_no_int == im_no:
                    return im
        raise AssertionError(f'ROI not found for the subject: {subject_no},'
                             f' camera: {camera_no}, image: {im_no}')


class Saivt_SoftBio(VideoDataset):
    dataset_dir = 'SAIVT-SoftBio'

    def __init__(self, root='', **kwargs):
        self.root = osp.abspath(osp.expanduser(root))
        self.cur_dataset_dir = osp.join(self.root, self.dataset_dir)

        self.data_dir = osp.join(self.cur_dataset_dir, 'Uncontrolled')

        person_ids = [f.name for f in os.scandir(self.data_dir) if f.is_dir()]
        train_pers, test_pers = \
            model_selection.train_test_split(person_ids, random_state=42)
        query_pers, gallery_pers = \
            model_selection.train_test_split(test_pers, random_state=42,
                                             train_size=0.5)

        # tracklets in format: [
        #                       (img_names, {paths}
        #                       person_id,
        #                       camera_id)
        #                      ]

        train = self.prepare_tracklets(train_pers)
        query = self.prepare_tracklets(query_pers)
        gallery = self.prepare_tracklets(gallery_pers)

        reader = Saivt_SoftBioImageReader()
        super(Saivt_SoftBio, self).__init__(train, query, gallery,
                                            image_reader=reader, **kwargs)

    def prepare_tracklets(self, persons):
        tracklets = []
        dirname2pid = {dirname: i for i, dirname in enumerate(persons)}
        for person in persons:
            person_dir = osp.join(self.data_dir, person)
            img_names = glob.glob(osp.join(person_dir, '*/*.jpeg'))
            assert len(img_names) > 0
            img_names = tuple(img_names)
            pid = dirname2pid[person]
            tracklets.append((img_names, pid, 0))
        return tracklets


torchreid.data.register_video_dataset('saivt_softbio', Saivt_SoftBio)


if __name__ == "__main__":
    datamanager = torchreid.data.VideoDataManager(
        root='E:\\datasets',
        sources='saivt_softbio',
        targets='saivt_softbio',
        height=256,
        width=128,
        batch_size_train=2,
        batch_size_test=2,
        transforms=['random_flip', 'random_crop'],
        train_sampler='RandomSampler'
    )
    for i, batch in enumerate(datamanager.return_dataloaders()[0]):
        if i < 10:
            print(batch[0].shape)
        else:
            break

    pass
