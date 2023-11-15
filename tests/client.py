import requests

x = requests.post("http://localhost:5050/command/playlist_")

print(x.text)