import os.path
import pkgutil

import examples

pkg_path = os.path.dirname(examples.__file__)
snippets = ([name for _, name, _ in pkgutil.iter_modules([pkg_path])])
print(snippets)
