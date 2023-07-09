import os

"""

Disabling Kivy's console log to declutter console while in testing phase
of development.

[Read More](https://kivy.org/doc/stable/guide/environment.html)
"""
os.environ['KIVY_NO_CONSOLELOG'] = '1'

import os.path
import pkgutil

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

import main
import bumbles

examples_package = 'bumbles'
token = main.get_token(os.path.join("config", "token.txt"))


class ExampleSelector(App):

    def build(self):
        pkg_path = os.path.dirname(bumbles.__file__)
        snippets = ([name for _, name, _ in pkgutil.iter_modules([pkg_path])])
        grid = GridLayout(rows=len(snippets))

        for snippet in snippets:
            button = Button(text=f"{snippet}")
            func = __import__(f"{examples_package}.{snippet}", fromlist=[f"{examples_package}"])
            button.bind(on_release=lambda x: func.run(token))
            grid.add_widget(button)

        return grid


if __name__ == '__main__':
    ExampleSelector().run()
