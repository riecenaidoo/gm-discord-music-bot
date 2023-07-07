"""
Script Executions
"""
import os

from examples import (message_listener, channel_retriever, selective_message_listener,
                      voice_joiner, voice_emitter)


# Helper Methods

def get_token(token_path):
    """Open and read the file containing the token,
    which should be on a single line."""

    try:
        with open(token_path, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"[WARNING] The specified token file at '{token_path}' was not found.")


if __name__ == "__main__":
    """
    Token controls access to the bot.
    For safety, it is stored and read from a file that
    does not get pushed to the repo, and is only saved
    locally.
    """
    token = get_token(os.path.join("config", "token.txt"))
    if token:
        raise RuntimeError("[INFO] Uncomment the script you're testing!")  # Comment Out
        # message_listener.run(token)
        # channel_retriever.run(token)
        # selective_message_listener.run(token)
        # voice_joiner.run(token)
        # voice_emitter.run(token)
