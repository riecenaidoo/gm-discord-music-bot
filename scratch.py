import os.path
import pkgutil

import examples
import main

pkg_path = os.path.dirname(examples.__file__)
snippets = ([name for _, name, _ in pkgutil.iter_modules([pkg_path])])
print(snippets)

s = snippets[0]
print(f"examples.{snippets[0]}")

func = __import__(f"examples.{snippets[0]}", fromlist=["examples"])
func.run(main.get_token(os.path.join("config", "token.txt")))
