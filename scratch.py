import os.path
import pkgutil

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

import examples
import main

token = main.get_token(os.path.join("config", "token.txt"))


class ExampleSelector(App):

    def build(self):
        pkg_path = os.path.dirname(examples.__file__)
        snippets = ([name for _, name, _ in pkgutil.iter_modules([pkg_path])])
        grid = GridLayout(rows=len(snippets))

        for snippet in snippets:
            button = Button(text=f"{snippet}")
            func = __import__(f"examples.{snippet}", fromlist=["examples"])
            button.bind(on_release=lambda x: func.run(token))
            grid.add_widget(button)

        return grid


if __name__ == '__main__':
    ExampleSelector().run()
