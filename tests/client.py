import requests

x = requests.post("http://localhost:5050/command/leave")

print(x.text)