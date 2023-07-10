import importlib
import os

"""

Disabling Kivy's console log to declutter console while in testing phase
of development.

[Read More](https://kivy.org/doc/stable/guide/environment.html)
"""
# os.environ['KIVY_NO_CONSOLELOG'] = '1'

import os.path
import pkgutil

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

import bumbles

examples_package = 'bumbles'
# token = main.get_token(os.path.join("config", "token.txt"))
token = "is this the function you're looking for?"


def call(func_name: str):
    print(func_name)  # For some reason, we are always receiving foo.
    func = importlib.import_module(name=f"{examples_package}.{func_name}", package=examples_package)
    func.run(token)


class ExampleSelector(App):

    def build(self):
        pkg_path = os.path.dirname(bumbles.__file__)
        snippets = ([name for _, name, _ in pkgutil.iter_modules([pkg_path])])
        grid = GridLayout(rows=len(snippets))

        buttons = set()
        for snip in snippets:
            buttons.add(Button(text=f"{snip}"))

        for button in buttons:
            button.bind(on_release=lambda x: call(button.text))

        for button in buttons:
            grid.add_widget(button)

        return grid


if __name__ == '__main__':
    ExampleSelector().run()
