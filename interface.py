"""Dynamically created interface for the main script using
Kivy."""

import importlib
import os.path
import pkgutil

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

"""
os.environ['KIVY_NO_CONSOLELOG'] = '1'  # Add before Kivy import statements

Disabling Kivy's console log to declutter console while in testing phase
of development. 

[Read More](https://kivy.org/doc/stable/guide/environment.html)
"""


class ModuleSelector(App):
    """Dynamically created gui that enables the user
    to select a specific module from a package and run
    the example code snippet inside it."""

    def __init__(self, package: str, token: str):
        """Initialises the selector.
        :param package: package name containing the modules to select from
        :param token: the access token to pass to the example code snippet's run method
        """

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
        """Handles the execution of the chosen example
        code snippet by dynamically importing the module
        and calling its run method.

        All example code snippets in the package must have a
        run() method, which would be their entry point.
        """

        module_name = instance.text
        module = importlib.import_module(name=f"{self.package}.{module_name}", package=self.package)
        module.run(self.token)
