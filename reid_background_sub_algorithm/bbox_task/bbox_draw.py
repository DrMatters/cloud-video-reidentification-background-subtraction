import collections
import operator
import pathlib
from pathlib import Path
from typing import Any, Union, List, Dict, Set

import cv2
import xmltodict

import settings

SELECT_FILE = 'VIRAT_S_000001'
DATASETS_FOLDER = pathlib.Path(settings.datasets_path)
DATASET_SUBFOLDER = pathlib.Path('./VIRAT/BigSizeVideo/')
CUR_FOLDER: Union[Path, Any] = DATASETS_FOLDER / DATASET_SUBFOLDER / SELECT_FILE
DEBUG = True
RESIZE_SCALE = 0.5

EventWithId = collections.namedtuple('EventWithId', [
    'framespan',
    'external_id'
])


def check_for_gaps(person):
    spans = person['attribute']['data:bbox']
    end = int(spans[0]['@framespan'].split(':')[0]) - 1
    max_gap = 0
    for idx, span in enumerate(spans):
        start, new_end = span['@framespan'].split(':')
        start = int(start)
        new_end = int(new_end)
        detected_gap = start - end - 1
        if detected_gap > 0:
            print(f'Detected gap for person id={person["@id"]}.'
                  f' Length={detected_gap}, starts at [{end}], index=({idx})')
            max_gap = max(max_gap, detected_gap)
        end = new_end
    return max_gap


def create_event_list(persons: List):
    events: List[EventWithId] = []
    for idx, person in enumerate(persons):
        start, end = person['@framespan'].split()[0].split(':')
        start = int(start)
        end = int(end)
        events.append(EventWithId(start, idx))
        events.append(EventWithId(end, idx))
    events = sorted(events, key=operator.attrgetter('framespan'))
    return events


def update_active_persons(frame_no: int, events: List[EventWithId],
                          expected_event_id: int,
                          active_persons_external_ids: Set[int]):
    cur_frame_events = []
    while events[expected_event_id].framespan == frame_no:
        cur_frame_events.append(events[expected_event_id])
        expected_event_id += 1

    for event in cur_frame_events:
        event_person_id = event.external_id
        if event_person_id in active_persons_external_ids:
            active_persons_external_ids.remove(event_person_id)
        else:
            active_persons_external_ids.add(event_person_id)
    return expected_event_id


def play(markdown: Dict, capture: cv2.VideoCapture):
    resize_resolution = (
        int(capture.get(cv2.CAP_PROP_FRAME_WIDTH) * RESIZE_SCALE),
        int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT) * RESIZE_SCALE)
    )

    persons = markdown['viper']['data']['sourcefile']['object']
    if DEBUG:
        for person_id in persons:
            check_for_gaps(person_id)

    events: List[EventWithId] = create_event_list(persons)

    show_frames = False
    frame_no = 0
    expected_event_id = 0
    active_persons_ids = set()
    if DEBUG:
        frame_no = 3400 - 1
        capture.set(cv2.CAP_PROP_POS_FRAMES, 3400)
    while capture.isOpened():
        ret, frame = capture.read()
        if ret is False:
            break

        if frame_no == events[expected_event_id].framespan:
            show_frames = True
            expected_event_id = update_active_persons(frame_no, events,
                                                      expected_event_id,
                                                      active_persons_ids)

        current_bboxes = get_bboxes_for_active(active_persons_ids, frame_no,
                                               persons)
        frame = put_bboxes_on_frame(current_bboxes, frame)

        if show_frames:
            frame = cv2.resize(frame, resize_resolution)
            cv2.imshow('vid', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        frame_no += 1


def put_bboxes_on_frame(current_bboxes, frame):
    for bbox_with_id in current_bboxes:
        h = int(bbox_with_id[0]['@height'])
        w = int(bbox_with_id[0]['@width'])
        x = int(bbox_with_id[0]['@x'])
        y = int(bbox_with_id[0]['@y'])

        COL_WHITE = (0xff, 0xff, 0xff)
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), COL_WHITE,
                              thickness=5)
        font = cv2.FONT_HERSHEY_SIMPLEX
        frame = cv2.putText(frame, str(bbox_with_id[1]), (x, y + h), font, 1,
                            (0, 0, 0), thickness=6)
    return frame


def get_bboxes_for_active(active_persons_ids, frame_no, persons):
    current_bboxes = []
    for person_id in active_persons_ids:
        person = persons[person_id]
        if 'current_bbox_id' not in person:
            person['current_bbox_id'] = 0
        current_bbox_id = person['current_bbox_id']
        current_bbox = person['attribute']['data:bbox'][current_bbox_id]
        end = int(current_bbox['@framespan'].split(':')[1])
        if end == frame_no:
            person['current_bbox_id'] += 1
        current_bboxes.append((current_bbox, person_id))
    return current_bboxes


def main():
    TRACKING_FILE = CUR_FOLDER / 'tracking.xgtf'
    VIDEO_FILE = CUR_FOLDER / (SELECT_FILE + '.mp4.mpg')

    with open(TRACKING_FILE) as markdown_file:
        markdown = xmltodict.parse(markdown_file.read())
    del markdown_file

    cap = cv2.VideoCapture(VIDEO_FILE.absolute().as_posix())

    play(markdown, cap)


if __name__ == '__main__':
    main()
