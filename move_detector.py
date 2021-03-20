import numpy as np
import cv2
import matplotlib.pyplot as plt
from IPython.display import Video
import vlc
import background as bg

np.random.seed(404)

import os
os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')

import time

def fix_color(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


class MoveDetector:
    def __init__(self):
        self.background = bg.Background(10)
        self.captureStream = cv2.VideoCapture(0)

    def process_frame(self, frame):
        if self.background.is_working():
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray_background = cv2.cvtColor(self.background.get_background(), cv2.COLOR_BGR2GRAY)
            diff_frame = cv2.absdiff(gray_frame, gray_background)
            blurred = cv2.GaussianBlur(diff_frame, (11, 11), 0)
            _, threshold_frame = cv2.threshold(blurred, 30, 255, cv2.THRESH_BINARY)
            return threshold_frame
        else:
            print("Frame:", frame)
            return frame

    def loop(self):
        while (True):
            start = time.time()
            _, frame = self.captureStream.read()
            self.background.add_frame(np.copy(frame))

            image = self.process_frame(np.copy(frame))
            cv2.imshow('frame', image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            end = time.time()
            print(end-start)
        # When everything done, release the capture
        self.captureStream.release()
        cv2.destroyAllWindows()






