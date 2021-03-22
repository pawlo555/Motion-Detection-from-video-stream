import numpy as np


class Background:
    """
    Class responsible for generating and keeping proper background.
    """
    def __init__(self, frames_number, average_alfa=0.1):
        """
        :param frames_number: frames number needed to start working
        :param average_alfa: smoothing factor in background update
        """
        self.frames_to_work = frames_number
        self.frames = []
        self.work = False
        self.background = None
        self.average_alfa = average_alfa

    def add_frame(self, frame):
        """
        :param frame: frame get from VideoCapture read() function
        :returns: None
        """
        if self.work:
            self.update_background(frame)
        else:
            self.insert_frame(frame)

    def update_background(self, frame):
        """
        Updating frame using moving average
        :param frame: frame used to update background
        :return: None
        """
        if self.background is not None:
            self.background = (self.background*(1-self.average_alfa) +
                               frame*self.average_alfa).astype(dtype=np.uint8)
        else:
            raise ValueError("Background in None")

    def insert_frame(self, frame):
        """
        Adding frame to self.frames
        :param frame: frame to be added
        :return: None
        """
        self.frames.append(frame)
        if len(self.frames) >= self.frames_to_work:
            self.create_background()
            self.work = True

    def create_background(self):
        """
        Creating a background
        :return: None
        """
        if self.background is None:
            self.background = np.median(self.frames, axis=0).astype(dtype=np.uint8)
        else:
            raise ValueError("Creating a not None background")

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
