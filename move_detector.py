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

    def loop(self):
        while (True):
            start = time.time()
            # Capture frame-by-frame
            prev_frame = None
            ret, frame = self.captureStream.read()
            self.background.add_frame(np.copy(frame))
            if prev_frame is not None and prev_frame == frame:
                print(True)
            # Our operations on the frame come here
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Display the resulting frame
            if self.background.get_background() is not None:
                cv2.imshow('frame', self.background.get_background())
            else:
                cv2.imshow('frame', gray)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            end = time.time()
            prev_frame = frame
            #print(end-start)
        # When everything done, release the capture
        self.captureStream.release()
        cv2.destroyAllWindows()






