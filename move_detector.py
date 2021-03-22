import numpy as np
import cv2
import os
import background as bg
import time

np.random.seed(404)
os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')


class MoveDetector:
    def __init__(self, box_min_area=1000):
        self.background = bg.Background(10)
        self.captureStream = cv2.VideoCapture(0)
        self.box_min_area = box_min_area

    def process_frame(self, frame):
        if self.background.is_working():
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray_background = cv2.cvtColor(self.background.get_background(), cv2.COLOR_BGR2GRAY)
            diff_frame = cv2.absdiff(gray_frame, gray_background)
            blurred = cv2.GaussianBlur(diff_frame, (11, 11), 0)
            _, threshold_frame = cv2.threshold(blurred, 50, 255, cv2.THRESH_BINARY)
            return threshold_frame
        else:
            return frame

    def get_boxes(self, frame):
        if self.background.is_working():
            threshold_frame = self.process_frame(frame)
            boxes, _ = cv2.findContours(threshold_frame.copy(), cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)
            return boxes
        else:
            return None

    def apply_boxes(self, frame, boxes):
        if boxes is not None:
            indices = apply_non_max_suppression(boxes)
            for i, box in enumerate(boxes):
                if area(box) > self.box_min_area and i in indices:  # show only big bix
                    x, y, w, h = cv2.boundingRect(box)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return frame

    def loop(self):
        while True:
            start = time.time()
            _, frame = self.captureStream.read()
            self.background.add_frame(np.copy(frame))

            boxes = self.get_boxes(np.copy(frame))
            image = self.apply_boxes(frame, boxes)
            cv2.imshow('frame', image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            end = time.time()
            print(end - start)
        # When everything done, release the capture
        self.captureStream.release()
        cv2.destroyAllWindows()


def area(box):
    _, _, w, h = cv2.boundingRect(box)
    return w * h


def apply_non_max_suppression(boxes):
    centered_box = []
    for box in boxes:
        box_as_array = list(cv2.boundingRect(box))
        centered_box.append(box_as_array)
    scores = [1.0 for _ in range(len(boxes))]
    indices = cv2.dnn.NMSBoxes(centered_box, scores, 0.5, 0.1)
    print(len(boxes), len(indices))
    return indices


def fix_color(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
