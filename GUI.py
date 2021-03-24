# coding:utf-8
from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.graphics.texture import Texture
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
import move_detector as md


import cv2
import numpy


class KivyCamera(Image):
    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.detector = md.MoveDetector()
        self.capture = self.detector.captureStream
        Clock.schedule_interval(self.update, 1.0 / fps)

    def update(self, dt):
        ret, frame = self.capture.read()
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
        
    def newSource(self,command):
        self.detector.set_capture_link(command)

    def newMinBox(self,command):
        self.detector.set_box_min_area(command)

    def newBlureSize(self,command):
        self.detector.set_blur_size(command)

    def newMinTreshold(self,command):
        self.detector.set_min_threshold(command)

    def newAverageAlfa(self,command):
        self.detector.set_average_alfa(command)

    
    
    def debug1(self):
        #do debug
        print("1")

    def debug2(self):
        #do debug
        print("1")

    def debug3(self):
        #do debug
        print("1")

    def changeHipeer(self):
        #hiperparametry
        print("1")

    def backToStr(self):
        #kamera wraca do stnau początkowego
        print("1")




class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid,self).__init__(**kwargs)
        
        self.controlPanel = GridLayout()
        self.buttonsPanel = GridLayout()
        self.txtPanel = GridLayout()

        self.cols = 2
        self.controlPanel.rows = 2
        self.buttonsPanel.cols = 3
        self.buttonsPanel.rows = 3
        self.txtPanel.cols = 2

        ### inside app
        self.capture = 1
        self.my_camera1 = KivyCamera(capture=self.capture, fps=30)
        self.add_widget(self.my_camera1)
        
        self.add_widget(self.controlPanel)
        ###

        ### inside control panel
        self.controlPanel.add_widget(self.txtPanel)

        self.controlPanel.add_widget(self.buttonsPanel)
        ###

        ### inside buttons panel
        self.Button1 = Button(text = "Video Source Submit")
        self.Button1.bind(on_press = self.pressed1)
        self.buttonsPanel.add_widget(self.Button1)
        
        self.Button2 = Button(text = "Set Min Box Area Submit")
        self.Button2.bind(on_press = self.pressed2)
        self.buttonsPanel.add_widget(self.Button2)

        self.Button3 = Button(text = "Set Blur Size Submit")
        self.Button3.bind(on_press = self.pressed3)
        self.buttonsPanel.add_widget(self.Button3)

        self.Button4 = Button(text = "Set Min Threshold Submit")
        self.Button4.bind(on_press = self.pressed4)
        self.buttonsPanel.add_widget(self.Button4)

        self.Button5 = Button(text = "Set Average Alfa Submit")
        self.Button5.bind(on_press = self.pressed5)
        self.buttonsPanel.add_widget(self.Button5)

        self.Button6 = Button(text = "Debug 1")
        self.Button6.bind(on_press = self.pressed6)
        self.buttonsPanel.add_widget(self.Button6)

        self.Button7 = Button(text = "Debug 2")
        self.Button7.bind(on_press = self.pressed7)
        self.buttonsPanel.add_widget(self.Button7)

        self.Button8 = Button(text = "Clean App")
        self.Button8.bind(on_press = self.pressed8)
        self.buttonsPanel.add_widget(self.Button8)

        self.Button9 = Button(text = "Exit")
        self.Button9.bind(on_press = self.pressed9)
        self.buttonsPanel.add_widget(self.Button9)
        ###

        ### inside txt panel
        self.inputPanel = TextInput(multiline = False)
        self.txtPanel.add_widget(self.inputPanel)

        self.outputPanel = Label(text = "it will be output")
        self.txtPanel.add_widget(self.outputPanel)
        ###
    
    def pressed1(self,instance):
        #newSoure
        command = self.inputPanel.text
        self.inputPanel.text =""
        self.outputPanel.text = "video path/link/cam = \n" + command
        if(command == '0'):
            command = 0
        try:
            self.my_camera1.newSource(command)
        except:
            pass
        #read stream/path/ETC


    def pressed2(self,instance):
        #newMinBox
        command = self.inputPanel.text
        self.inputPanel.text =""
        self.outputPanel.text = "min box size = \n" + command
        self.my_camera1.newMinBox(int(command))

    def pressed3(self,instance):
        #newBlureSize
        command = self.inputPanel.text
        self.inputPanel.text =""
        self.outputPanel.text = "blure size = \n" + command
        self.my_camera1.newBlureSize(int(command))

    def pressed4(self,instance):
        #newMinTreshold
        command = self.inputPanel.text
        self.inputPanel.text =""
        self.outputPanel.text = "min treshold = \n" + command
        self.my_camera1.newMinTreshold(int(command))


    def pressed5(self,instance):
        #newAverageAlfa
        command = self.inputPanel.text
        self.inputPanel.text =""
        self.outputPanel.text = "average alfa = \n" + command
        self.my_camera1.newAverageAlfa(float(command))


    def pressed6(self,instance):
        print("penis6")
        self.my_camera1.debug3()

    #??? maski?
    def pressed7(self,instance):
        print("7 clicked")
        #????

    #???
    def pressed8(self,instance):
        print("penis8")
        self.my_camera1.backToStr()

    #DONE
    def pressed9(self,instance):
        App.get_running_app().stop()
        Window.close()
        #close app


    
    def loadCam(self,instance):
        self.capture = cv2.VideoCapture(self.a)


class MyApp(App):
    def build(self):
        return MyGrid()

    def on_stop(self):
        #without this, app will not exit even if the window is closed
        self.capture.release()



if __name__ == '__main__':
    MyApp().run()

