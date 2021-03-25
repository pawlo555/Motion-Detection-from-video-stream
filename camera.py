# coding:utf-8
from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import move_detector as md
import GUI as grid
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
    
    def newSource(self, command):
        self.detector = md.MoveDetector(command)

    def newMinBox(self,command):
        self.detector.set_box_min_area(command)

    def newBlureSize(self,command):
        self.detector.set_blur_size(command)

    def newMinTreshold(self,command):
        self.detector.set_min_threshold(command)

    def newAverageAlfa(self,command):
        self.detector.set_average_alfa(command)

    def newMask(self,command):
        self.detector.add_mask(command)

    def removeMask(self):
        self.detector.add_mask("no_mask.png")
        print("mask removed")

    def debug1(self):
        self.detector.set_state(self.detector.state.Normal)
    
    def debug2(self):
        self.detector.set_state(self.detector.state.Background)
    
    def debug3(self):
        self.detector.set_state(self.detector.state.Threshold)

    def backToStr(self):
        #kamera wraca do stanu początkowego
        print("app clean")



