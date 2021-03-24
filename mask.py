import numpy as np
from PIL import Image, ImageDraw

class Mask:
    def __init__(self, img=None, size=(720, 540)):
        self.mask = None
        self.size = size

        if img: self.set_mask(img)

    def set_size(self, size):
        """
        Setting the size of the mask to the size of the frame
        :param size: size of the frame
        """
        self.size = size

    def set_mask(self, img):
        """
        Setting mask with path to B&W image,
        where white pixels pass frame pixels through, 
        and black ones do not.
        :param self: Mask object
        :param img: path to mask image
        """
        image = Image.open(img).convert("L").resize(self.size)
        self.mask = np.array(image)[:,:] // 255

    def add_mask(self, frame):
        """ 
        Add mask to a frame
        :param self: Mask object
        :param frame: frame to be masked
        """
        return np.multiply(frame, self.mask)