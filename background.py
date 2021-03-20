import numpy as np


class Background:
    """
    Class responsible for generating and keeping proper background.
    """
    def __init__(self, frames_number):
        """
        :param frames_number: number of frames after the background could be created and starts to work
        """
        self.frames_to_work = frames_number
        self.frames = []
        self.work = False
        self.background = None

    def add_frame(self, frame):
        """
        :param frame: frame get from VideoCapture read() function
        :returns: None
        """
        if self.work:
            self.update_background(frame)
        else:
            self.add_frame(frame)

    def update_background(self, frame):
        """
        Updating frame using moving average
        :param frame: frame used to update background
        :return: None
        """
        if self.background is not None:
            self.background = (self.background*0.95 + frame*0.05).astype(dtype=np.unit8)
        else:
            raise ValueError("Background in None")

    def add_frame(self, frame):
        """
        Adding frame to self.frames
        :param frame: frame to be added
        :return: None
        """
        self.frames.append(frame)
        if len(self.frames) >= self.frames_to_work:
            self.create_background
            self.work = True

    def create_background(self):
        """
        Creating a background
        :return: None
        """
        self.background = np.median(self.frames, axis=0).astype(dtype=np.uint8)

    def get_background(self):
        """
        :return: self.background
        """
        return self.background

    def is_working(self):
        """
        :return: self.work
        """
        return self.work
