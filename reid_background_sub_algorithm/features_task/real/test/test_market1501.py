import functools

import cv2
from torch.utils import data

import utils
from features_task.real import market_1501, non_ml_features


def identity_collate(data):
    return data


DATASET_FOLDER = '/Users/DrMatters/Documents/git/vision/data/datasets/' \
                 'market1501/Market-1501-v15.09.15/'
surf: cv2.xfeatures2d_SURF = cv2.xfeatures2d.SURF_create(400)
dac_surf = functools.partial(surf.detectAndCompute, mask=None)
descriptorator = non_ml_features.DescriptorsPreprocessing(dac_surf)

index_df = utils.create_index_df(DATASET_FOLDER + 'bounding_box_test')
ds = market_1501.MarketDataset(DATASET_FOLDER + 'bounding_box_test',
                               index_df,
                               preprocessing=descriptorator.get_preprocessing())
ld = data.DataLoader(ds, drop_last=True, collate_fn=identity_collate)

num_desc = []
for i, res in enumerate(ld):
    num_desc.append(res[0][0].shape[0])
    if i == 500:
        break

pass