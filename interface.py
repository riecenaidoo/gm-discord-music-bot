"""Dynamically created interface for the main script using
Kivy."""

import importlib
import os.path
import pkgutil


class ModuleSelector:
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
        self.menu = []

        pkg = importlib.import_module(self.package)
        pkg_path = os.path.dirname(pkg.__file__)
        modules = ([name for _, name, _ in pkgutil.iter_modules([pkg_path])])

        for module in modules:
            self.menu.append(f"{module}")

    def call(self, module_name: str):
        """Handles the execution of the chosen example
        code snippet by dynamically importing the module
        and calling its run method.

        All example code snippets in the package must have a
        run() method, which would be their entry point.
        """

        module = importlib.import_module(name=f"{self.package}.{module_name}", package=self.package)
        module.run(self.token)

    def run(self):
        print("(Type QUIT to exit)\n\n")
        print("Example Snippets:")
        for index, item in enumerate(self.menu):
            print(f"[{index}] {item}")

        choice = None
        while choice != "QUIT".casefold():
            choice = input("Example[?] > ").casefold()
            try:
                i = int(choice)
                if i < 0 or i >= len(self.menu):
                    print("Please select an item in the list.")
                    continue
                self.call(self.menu[i])
            except ValueError:
                print("Please choose the 'i' of a snippet i.e: [i] ...")
