from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

class libMenu(Button):
    def __init__(self):
        dropdown = DropDown()
        for i in ('a', 'b', 'c'):
            btn = Button(text=i, size_hint_y=None, height=30)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)
        tb = Button(text='Choose dir', size_hint=(1,1))
        tb.bind(on_release=dropdown.open)

class DropBut(Button):
    def __init__(self, **kwargs):
        super(DropBut, self).__init__(**kwargs)
        self.drop_list = None
        self.drop_list = DropDown()

        types = ['Item1', 'Item2', 'Item3', 'Item4', 'Item5', 'Item6']

        for i in types:
            btn = Button(text=i, size_hint_y=None, height=50)
            btn.bind(on_release=lambda btn: self.drop_list.select(btn.text))

            self.drop_list.add_widget(btn)

        self.bind(on_release=self.drop_list.open)
        self.drop_list.bind(on_select=lambda instance, x: setattr(self, 'text', x))

class TestApp(App):
    def build(self):
        return libMenu()

TestApp().run()