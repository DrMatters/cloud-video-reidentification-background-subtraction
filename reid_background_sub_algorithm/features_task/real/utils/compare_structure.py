import pathlib
import os
import json
import argparse
from pprint import pprint

MY_WALK = ["calibration/calibration.txt", "calibration/camera_position.txt", "calibration/ROIs.txt",
           "demo_code/downloadDukeMTMC.m", "demo_code/Evaluation.zip", "demo_code/MCT.zip", "demo_code/SCT.zip",
           "demo_data/Data.zip", "detections/camera1.mat", "detections/camera2.mat", "detections/camera3.mat",
           "detections/camera4.mat", "detections/camera5.mat", "detections/camera6.mat", "detections/camera7.mat",
           "detections/camera8.mat", "detections/camera9.mat", "ground_truth/trainval.mat",
           "ground_truth/trainvalRaw.mat", "misc/data_distribution.png", "misc/devkit-mtmc.zip",
           "misc/devkit-mtmc.zip_old", "misc/draw_on_map.m", "misc/DukeMTMC.docx", "misc/DukeMTMC.pdf",
           "misc/map.png", "misc/map_large.png", "misc/motchallenge-devkit.zip", "misc/tracker_output.zip",
           "misc/world_to_map.m", "videos/camera1/00000.mts", "videos/camera1/00001.mts",
           "videos/camera1/00002.mts", "videos/camera1/00003.mts", "videos/camera1/00004.mts",
           "videos/camera1/00005.mts", "videos/camera1/00006.mts", "videos/camera1/00007.mts",
           "videos/camera1/00008.mts", "videos/camera1/00009.mts", "videos/camera2/00000.mts",
           "videos/camera2/00001.mts", "videos/camera2/00002.mts", "videos/camera2/00003.mts",
           "videos/camera2/00004.mts", "videos/camera2/00005.mts", "videos/camera2/00006.mts",
           "videos/camera2/00007.mts", "videos/camera2/00008.mts", "videos/camera2/00009.mts",
           "videos/camera3/00000.mts", "videos/camera3/00001.mts", "videos/camera3/00002.mts",
           "videos/camera3/00003.mts", "videos/camera3/00004.mts", "videos/camera3/00005.mts",
           "videos/camera3/00006.mts", "videos/camera3/00007.mts", "videos/camera3/00008.mts",
           "videos/camera3/00009.mts", "videos/camera4/00000.mts", "videos/camera4/00001.mts",
           "videos/camera4/00002.mts", "videos/camera4/00003.mts", "videos/camera4/00004.mts",
           "videos/camera4/00005.mts", "videos/camera4/00006.mts", "videos/camera4/00007.mts",
           "videos/camera4/00008.mts", "videos/camera4/00009.mts", "videos/camera5/00000.mts",
           "videos/camera5/00001.mts", "videos/camera5/00002.mts", "videos/camera5/00003.mts",
           "videos/camera5/00004.mts", "videos/camera5/00005.mts", "videos/camera5/00006.mts",
           "videos/camera5/00007.mts", "videos/camera5/00008.mts", "videos/camera5/00009.mts",
           "videos/camera6/00000.mts", "videos/camera6/00001.mts", "videos/camera6/00002.mts",
           "videos/camera6/00003.mts", "videos/camera6/00004.mts", "videos/camera6/00005.mts",
           "videos/camera6/00006.mts", "videos/camera6/00007.mts", "videos/camera6/00008.mts",
           "videos/camera7/00000.mts", "videos/camera7/00001.mts", "videos/camera7/00002.mts",
           "videos/camera7/00003.mts", "videos/camera7/00004.mts", "videos/camera7/00005.mts",
           "videos/camera7/00006.mts", "videos/camera7/00007.mts", "videos/camera7/00008.mts",
           "videos/camera8/00000.mts", "videos/camera8/00001.mts", "videos/camera8/00002.mts",
           "videos/camera8/00003.mts", "videos/camera8/00004.mts", "videos/camera8/00005.mts",
           "videos/camera8/00006.mts", "videos/camera8/00007.mts", "videos/camera8/00008.mts",
           "videos/camera8/00009.mts", "videos/camera9/00000.mts", "videos/camera9/00001.mts",
           "videos/camera9/00002.mts", "videos/camera9/00003.mts", "videos/camera9/00004.mts",
           "videos/camera9/00005.mts", "videos/camera9/00006.mts", "videos/camera9/00007.mts",
           "videos/camera9/00008.mts"]


def create_relative_walk(directory):
    res = []
    for dirpath, dirnames, filenames in os.walk(directory):
        cur_dir = pathlib.Path(dirpath)
        for filename in filenames:
            full = cur_dir / filename
            rel_path = full.relative_to(directory).as_posix()
            res.append(rel_path)
    return res


def compare_dir_with_walk(walk, directory):
    walk = set(walk)
    dir_walk = set(create_relative_walk(directory))
    not_present_in_walk = dir_walk - walk
    not_present_in_dir = walk - dir_walk
    return not_present_in_walk, not_present_in_dir


def main():
    parser = argparse.ArgumentParser(description='Compares folder structure with saved walk')
    parser.add_argument("--stored_walk", default='./res_walk.json', type=str, help="Location of .json file containing "
                                                                                   "saved file structure")
    parser.add_argument("--folder", required=True, type=str, help="The location of the folder containing file "
                                                                  "structure to compare with stored file structure")
    args = parser.parse_args()
    stored_walk_location = args.stored_walk

    if pathlib.Path(stored_walk_location).exists():
        with open(stored_walk_location, 'r') as f:
            walk = json.load(f)
    else:
        print('WARN: Saved file structure not found, using default')
        walk = MY_WALK

    not_present_in_walk, not_present_in_folder = compare_dir_with_walk(walk, args.folder)
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print('Files found in local folder, but not found in saved structure:')
    pprint(list(not_present_in_walk))
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print('Files found in saved structure, but not found in local folder:')
    pprint(list(not_present_in_folder))
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    if not not_present_in_folder and not not_present_in_walk:
        print('Folders are equal!')


if __name__ == '__main__':
    main()
