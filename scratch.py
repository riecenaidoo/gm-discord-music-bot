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

import bumbles

examples_package = 'bumbles'
# token = main.get_token(os.path.join("config", "token.txt"))
token = "is this the function you're looking for?"


class ExampleSelector(App):

    def build(self):
        pkg_path = os.path.dirname(bumbles.__file__)
        snippets = ([name for _, name, _ in pkgutil.iter_modules([pkg_path])])
        grid = GridLayout(rows=len(snippets))

        directory = dict()

        for snippet in snippets:
            func = __import__(f"{examples_package}.{snippet}", fromlist=[f"{examples_package}"]).run
            directory.update({snippet: func})

        print(directory)

        for snip in directory:
            print(snip)
            print(directory.get(snip))
            grid.add_widget(Button(text=f"{snip}",
                                   on_release=lambda x: directory.get(snip)(token)))

        # for snippet in snippets:
        #     func = __import__(f"{examples_package}.{snippet}", fromlist=[f"{examples_package}"]).run
        #     grid.add_widget(Button(text=f"{snippet}",
        #                            on_release=lambda x: func(token)))  # Why are these binding to the same thing?

        return grid


if __name__ == '__main__':
    ExampleSelector().run()
