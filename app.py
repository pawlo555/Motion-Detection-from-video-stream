# coding:utf-8
from kivy.app import App
import GUI as grid

class MyApp(App):
    def build(self):
        return grid.MyGrid()

    def on_stop(self):
        # without this, app will not exit even if the window is closed
        print("Closing")