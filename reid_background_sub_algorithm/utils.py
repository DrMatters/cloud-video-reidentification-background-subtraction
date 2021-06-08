import os

import cv2
import pandas as pd


def get_filenames_in_current(folder: str):
    walk = os.walk(folder)
    for current_catalog, sub_catalogs, files in walk:
        if current_catalog == folder:
            return sorted(files)


def create_index_df(folder: str):
    filenames = pd.Series(get_filenames_in_current(folder))
    filenames = filenames[filenames.str.endswith('jpg')]
    index_df = filenames.str.split('_', expand=True, n=2)
    index_df = index_df.iloc[:, :1]
    index_df = index_df.rename(columns={
        0: 'pers_id', 1: 'env_descr',
        2: 'orig_id'
    })
    index_df['filename'] = filenames
    return index_df


def simple_draw(img):
    draw_step_size([], img)


def draw_percent_steps(keypoints, img, percent_on_step=10, delay=1000):
    step_size = int(len(keypoints) * (percent_on_step / 100))
    draw_step_size(keypoints, img, step_size, delay)


def draw_fixed_steps(keypoints, img, num_steps=20, delay=1000):
    step = len(keypoints) // num_steps
    draw_step_size(keypoints, img, step, delay)


def draw_step_size(keypoints, img, step=100, delay=1000):
    i = len(keypoints) // step
    if i > 0:
        while i > 0:
            i -= 1
            frame = cv2.drawKeypoints(img, keypoints[:i * step], None,
                                      flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS,
                                      color=(150, 0, 0)
                                      )

            # Display the resulting frame
            cv2.imshow('frame', frame)
            if cv2.waitKey(delay) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
    else:
        image = cv2.drawKeypoints(img, keypoints, None,
                                  flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS,
                                  color=(150, 0, 0)
                                  )
        cv2.imshow('image', image)
        if cv2.waitKey() & 0xFF == ord('q'):
            cv2.destroyAllWindows()
