"""
Source: https://discordpy.readthedocs.io/en/latest/intro.html#basic-concepts

discord.py revolves around the concept of events. 
An event is something you listen to and then respond to. 
For example, when a message happens, 
you will receive an event about it that you can respond to.

A quick example to showcase how events work:
"""

import os

import discord


# Helper Methods

def get_token(token_file):
    """Open and read the file containing the token,
    which should be on a single line."""

    try:
        with open(token_file, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"WARNING: The specified token file '{token_file}' was not found.")


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


def run():
    intents = discord.Intents.default()
    intents.message_content = True

    client = MyClient(intents=intents)

    """
    Token controls access to the bot.
    For safety, it is stored and read from a file that
    does not get pushed to the repo, and is only saved
    locally.
    """
    token = get_token(os.path.join("config", "token.txt"))
    if token:
        client.run(token)
