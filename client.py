import requests

x = requests.post("http://localhost:5050/command/join/1")

print(x.text)