"""
Script Executions
"""
import os

from dotenv import load_dotenv

from interface import ModuleSelector

if __name__ == "__main__":
    """
    Token controls access to the Discord bot.
    For safety, it is passed through an environment variable.
    You can set the environment variable in your shell,
    or using a `.env` file which is loaded with `load_dotenv`.
    """

    load_dotenv()
    ModuleSelector(package='examples', token=os.environ["DISCORD_BOT_TOKEN"]).run()
