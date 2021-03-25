# coding:utf-8
from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.graphics.texture import Texture
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
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
        print("app clean")


class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)

        self.controlPanel = GridLayout()
        self.buttonsPanel = GridLayout()
        self.txtPanel = GridLayout()

        self.rows = 2
        self.controlPanel.cols = 2
        self.buttonsPanel.cols = 4
        self.buttonsPanel.rows = 3
        self.txtPanel.cols = 2

        # inside app
        self.add_widget(self.controlPanel)
        self.add_widget(self.buttonsPanel)

        # inside control panel
        self.my_camera1 = KivyCamera( fps=30)
        self.controlPanel.add_widget(self.my_camera1)
        self.controlPanel.add_widget(self.txtPanel)

        # inside buttons panel
        self.Button1 = Button(text="Set \nMin Box \nArea \nSubmit")
        self.Button1.bind(on_press=self.pressed1)

        self.Button2 = Button(text="Set \nMin Threshold \nSubmit")
        self.Button2.bind(on_press=self.pressed2)

        self.Button3 = Button(text="Debug 1")
        self.Button3.bind(on_press=self.pressed3)

        self.Button4 = Button(text="Video \nSource \nSubmit")
        self.Button4.bind(on_press=self.pressed4)

        self.Button5 = Button(text="Set \nAverage Alfa \nSubmit")
        self.Button5.bind(on_press=self.pressed5)

        self.Button6 = Button(text="Set \nBlur Size \nSubmit")
        self.Button6.bind(on_press=self.pressed6)

        self.Button7 = Button(text="Debug 2")
        self.Button7.bind(on_press=self.pressed7)

        self.Button8 = Button(text="Clean App")
        self.Button8.bind(on_press=self.pressed8)

        self.Button9 = Button(text="Add Mask \n Submit")
        self.Button9.bind(on_press=self.pressed9)

        self.Button10 = Button(text="Remove Maks")
        self.Button10.bind(on_press=self.pressed10)

        self.Button11 = Button(text="Debug 3")
        self.Button11.bind(on_press=self.pressed11)

        self.Button12 = Button(text="Exit")
        self.Button12.bind(on_press=self.pressed12)

        self.buttonsPanel.add_widget(self.Button1)
        self.buttonsPanel.add_widget(self.Button2)
        self.buttonsPanel.add_widget(self.Button3)
        self.buttonsPanel.add_widget(self.Button4)
        self.buttonsPanel.add_widget(self.Button5)
        self.buttonsPanel.add_widget(self.Button6)
        self.buttonsPanel.add_widget(self.Button7)
        self.buttonsPanel.add_widget(self.Button8)
        self.buttonsPanel.add_widget(self.Button9)
        self.buttonsPanel.add_widget(self.Button10)
        self.buttonsPanel.add_widget(self.Button11)
        self.buttonsPanel.add_widget(self.Button12)

        # inside txt panel
        self.inputPanel = TextInput(multiline=False)
        self.txtPanel.add_widget(self.inputPanel)

        self.outputPanel = Label(text="it will be output")
        self.txtPanel.add_widget(self.outputPanel)

    def pressed1(self, instance):
        # newMinBox
        command = self.inputPanel.text
        self.inputPanel.text = ""
        self.outputPanel.text = "min box size = \n" + command
        if command != '':
            a = int(command)
            if a > 0:
                self.my_camera1.new_min_box(a)
            else:
                self.outputPanel.text = "bad value = " + command
        else:
            self.outputPanel.text = "no value given" + command

    def pressed2(self, instance):
        # newMinThreshold DONE
        command = self.inputPanel.text
        self.inputPanel.text = ""
        self.outputPanel.text = "min threshold = \n" + command
        if command != '':
            a = int(command)
            if a > 0:
                self.my_camera1.new_min_threshold(int(command))
            else:
                self.outputPanel.text = "bad value = " + command
        else:
            self.outputPanel.text = "no value given" + command

    def pressed3(self, instance):
        self.outputPanel.text = "debug 1 ON"
        self.my_camera1.debug1()

    def pressed4(self, instance):
        command = self.inputPanel.text
        self.inputPanel.text = ""
        self.outputPanel.text = "video path/link/cam = \n" + command
        if command == '0':
            command = 0
        print("Comand:" + str(type(command)))
        self.my_camera1.new_source(command)

    def pressed5(self, instance):
        command = self.inputPanel.text
        self.inputPanel.text = ""
        self.outputPanel.text = "average alfa = \n" + command
        if command != '':
            a = float(command)
            if 0 <= a <= 1:
                self.my_camera1.new_average_alfa(float(command))
            else:
                self.outputPanel.text = "bad value = " + command
        else:
            self.outputPanel.text = "no value given" + command

    def pressed6(self, instance):
        command = self.inputPanel.text
        self.inputPanel.text = ""
        self.outputPanel.text = "blure size = \n" + command
        if command != '':
            a = int(command)
            if a % 2 == 1 and a > 0:
                self.my_camera1.new_blur_size(int(command))
            else:
                self.outputPanel.text = "bad value = " + command
        else:
            self.outputPanel.text = "no value given" + command

    def pressed7(self, instance):
        self.outputPanel.text = "debug 2 ON"
        self.my_camera1.debug2()

    def pressed8(self, instance):
        self.outputPanel.text = "app cleaned"
        self.my_camera1.back_to_str()

    def pressed9(self, instance):
        # AddMask
        command = self.inputPanel.text
        self.inputPanel.text = ""
        self.outputPanel.text = "mask added, path = \n" + command
        self.my_camera1.new_mask(command)

    def pressed10(self):
        # RemoveMask
        self.outputPanel.text = "mask removed"
        self.my_camera1.remove_mask()

    def pressed11(self):
        # Debug 3
        self.outputPanel.text = "debug 3 ON"
        self.my_camera1.debug3()

    def pressed12(self):
        # close app
        self.my_camera1.detector.captureStream.release()
        App.get_running_app().stop()


class MyApp(App):
    def build(self):
        return MyGrid()

    def on_stop(self):
        # without this, app will not exit even if the window is closed
        print("Closing")


if __name__ == '__main__':
    MyApp().run()
