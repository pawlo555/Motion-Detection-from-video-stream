import numpy as np
import cv2
import background as bg
import time


class MoveDetector:
    def __init__(self, capture_link=0, box_min_area=800, blur_size=15, min_threshold=10,
                 supression_threshold=0.5, frames_to_work=10, average_alfa=0.1):
        """
        :param capture_link: link to the stream (0 is for local camera)
        :param box_min_area: minimal box area
        :param blur_size: size of the blur, the bigger the larger boxes will be detected
        :param min_threshold:
        :param supression_threshold: value for non_max_suppression, between 0 and 1.
        :param frames_to_work: frames to start detecting move
        :param average_alfa: change of the background speed, between 0 and 1.
        """
        self.background = bg.Background(frames_to_work, average_alfa)
        self.captureStream = cv2.VideoCapture(capture_link)
        self.box_min_area = box_min_area
        self.blur_shape = (blur_size, blur_size)
        self.min_threshold = min_threshold
        self.supression_threshold = supression_threshold

    def process_frame(self, frame):
        """
        Processing frame from BGR to black and white image, with white as places when move is detected
        :param frame: frame to be proceeds
        :return: proceeds frame
        """
        if self.background.is_working():
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray_background = cv2.cvtColor(self.background.get_background(), cv2.COLOR_BGR2GRAY)
            diff_frame = cv2.absdiff(gray_frame, gray_background)

            blurred = cv2.GaussianBlur(diff_frame, self.blur_shape, 0)
            _, threshold_frame = cv2.threshold(blurred, self.min_threshold, 255, cv2.THRESH_BINARY)
            return threshold_frame
        else:
            return frame

    def get_boxes(self, frame):
        """
        Finds boxes in input frame
        :param frame: get from be captureStream.read() function
        :return: boxes where move was detected, None if background is not working
        """
        if self.background.is_working():
            threshold_frame = self.process_frame(frame)
            boxes, _ = cv2.findContours(threshold_frame.copy(), cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)
            return boxes
        else:
            return None

    def apply_boxes(self, frame, boxes):
        """
        Adding boxes to the frame, checking box area and do non_max_supression()
        :param frame: frame to which boxes will be added
        :param boxes: boxes to be added to frame
        :return: frame with boxes
        """
        if boxes is not None:
            indices = self.apply_non_max_suppression(boxes)
            for i, box in enumerate(boxes):
                if area(box) > self.box_min_area and i in indices:  # show only big bix
                    x, y, w, h = cv2.boundingRect(box)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return frame

    def apply_non_max_suppression(self, boxes):
        """
        Doing non_max_suppression using cv2
        :param boxes: array of boxes
        :return: array of indexes to boxes which non overlap with others
        """
        centered_box = []
        for box in boxes:
            box_as_array = list(cv2.boundingRect(box))
            centered_box.append(box_as_array)
        scores = [1.0 for _ in range(len(boxes))]
        indices = cv2.dnn.NMSBoxes(centered_box, scores, 0.5, self.supression_threshold)
        return indices

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
    """
    Counts an area of the box
    :param box: cv2 box which area have to be counted
    :return: area of the box
    """
    _, _, w, h = cv2.boundingRect(box)
    return w * h
