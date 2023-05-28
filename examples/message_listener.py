"""
Listens to all messages in the Discord Server,
displaying them out in the terminal.
"""


import discord


# This example requires the 'message_content' intent.
class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    """ 'async' in Python: 
    Asynchronous programming is a characteristic of modern programming 
    languages that allows an application to perform various operations 
    without waiting for any of them.

    [Source](https://www.velotio.com/engineering-blog/async-features-in-python#:~:text=Async%20programming%20in%20Python,waiting%20for%20any%20of%20them.)
    """

    @staticmethod
    async def on_message(message):
        print(f'Message from {message.author}: {message.content}')


def run(token):
    intents = discord.Intents.default()
    intents.message_content = True

    client = MyClient(intents=intents)
    client.run(token)
