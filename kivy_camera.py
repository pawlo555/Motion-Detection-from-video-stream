from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import move_detector as md
import cv2


class KivyCamera(Image):
    def __init__(self, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.detector = md.MoveDetector()
        Clock.schedule_interval(self.update, 1.0 / fps)

    def update(self, dt):
        ret, frame = self.detector.captureStream.read()
        image = self.detector.process_frame(frame)
        if ret:
            # convert it to texture
            buf1 = cv2.flip(image, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(
                size=(image.shape[1], image.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture

    def new_source(self, command):
        self.detector = md.MoveDetector(command)

    def new_min_box(self, command):
        self.detector.set_box_min_area(command)

    def new_blur_size(self, command):
        self.detector.set_blur_size(command)

    def new_min_threshold(self, command):
        self.detector.set_min_threshold(command)

    def new_average_alfa(self, command):
        self.detector.set_average_alfa(command)

    def new_mask(self, command):
        self.detector.add_mask(command)

    def remove_mask(self):
        self.detector.add_mask("no_mask.png")

    def debug1(self):
        # do debug
        self.detector.set_state(md.States.Normal)

    def debug2(self):
        self.detector.set_state(md.States.Background)

    def debug3(self):
        self.detector.set_state(md.States.Threshold)

    def back_to_str(self):
        self.detector.back_to_default()
