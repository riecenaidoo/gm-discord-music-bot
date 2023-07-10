import importlib
import os

import main

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


class ExampleSelector(App):

    def __init__(self, package, token):
        super().__init__()
        self.token = token
        self.package = package

    def build(self):
        pkg = importlib.import_module(self.package)
        pkg_path = os.path.dirname(pkg.__file__)
        modules = ([name for _, name, _ in pkgutil.iter_modules([pkg_path])])

        grid = GridLayout(rows=len(modules))

        for module in modules:
            grid.add_widget(Button(
                text=f"{module}",
                on_release=self.call
            ))

        return grid

    def call(self, instance: Button):
        module_name = instance.text
        module = importlib.import_module(name=f"{self.package}.{module_name}", package=self.package)
        module.run(self.token)


if __name__ == '__main__':
    ExampleSelector('bumbles', main.get_token(os.path.join("config", "token.txt"))).run()
