import cv2
import numpy as np


def main():
    cap = cv2.VideoCapture('../data/videos/test.mp4')
    mog = cv2.createBackgroundSubtractorMOG2()
    knn = cv2.createBackgroundSubtractorKNN()

    codec = cv2.VideoWriter_fourcc(*'XVID')
    fps = cap.get(cv2.CAP_PROP_FPS)

    writer = None
    while cap.isOpened():
        ret, frame = cap.read()
        if ret is False:
            break
        frame = cv2.resize(frame, None, fx=0.3, fy=0.3)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        mog_mask = mog.apply(frame)
        knn_mask = knn.apply(frame)

        frame = np.concatenate((frame, mog_mask, knn_mask), 1)
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        if writer is None:
            writer = cv2.VideoWriter('../data/videos/output/test.avi',
                                     codec, fps, (frame.shape[1], frame.shape[0]))

        writer.write(frame)
        cv2.imshow('vid', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()