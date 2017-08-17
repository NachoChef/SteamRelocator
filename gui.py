from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from movegames import *
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
import movegames

class SteamRelGrLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(SteamRelGrLayout, self).__init__(**kwargs)
        self.install, self.libraries, self.lib_contents = movegames.setup()
        self.ids.libSpin1.values = self.libraries

class SteamRelocatorApp(App):
    def build(self):
        return SteamRelGrLayout()

if __name__ == '__main__':
    SteamRelocatorApp().run()
