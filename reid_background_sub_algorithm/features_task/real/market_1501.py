import os
from typing import FrozenSet

import albumentations as albu
import pandas as pd
from torch.utils import data
import cv2


class MarketDataset(data.Dataset):
    REQUIRED_COLUMNS: FrozenSet[str] = frozenset({'filename', 'pers_id'})

    def __init__(self, folder: str, index_df: pd.DataFrame = None,
                 transforms=albu.Compose([albu.HorizontalFlip()]),
                 preprocessing=None):
        assert set(index_df.columns).issubset(self.REQUIRED_COLUMNS), \
            ('Required columns are not present in dataframe. Expected:'
             f' {self.REQUIRED_COLUMNS}. Got: {set(index_df.columns)}')
        self._folder = folder
        self._index_df = index_df
        self._transforms = transforms
        self._preprocessing = preprocessing

    def __getitem__(self, idx):
        row = self._index_df.loc[idx, :]
        filename = row['filename']
        person_id = row['pers_id']

        full_path = os.path.join(self._folder, filename)

        img = cv2.imread(full_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        augmented = self._transforms(image=img)
        img = augmented['image']
        if self._preprocessing:
            preprocessed = self._preprocessing(image=img)
            img = preprocessed['image']
        return img, person_id

    def __len__(self):
        return len(self._index_df)
