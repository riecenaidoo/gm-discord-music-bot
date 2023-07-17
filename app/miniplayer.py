from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout


class Miniplayer(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pause_button = Button(text="[Pause]")
        self.resume_button = Button(text="[Resume]")

    def build(self):
        grid = GridLayout(cols=2)
        grid.add_widget(self.pause_button)
        grid.add_widget(self.resume_button)

        return grid


if __name__ == '__main__':
    Miniplayer().run()
