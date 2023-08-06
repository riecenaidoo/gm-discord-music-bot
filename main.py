import os

from dotenv import load_dotenv

from bot import run


def get_user_input() -> list[str]:
    instruction = ""
    while len(instruction) == 0:
        instruction = input(" > ")

    return instruction.split(" ")


if __name__ == "__main__":
    """
    Token controls access to the Discord bot.
    For safety, it is passed through an environment variable.
    You can set the environment variable in your shell,
    or using a `.env` file as the variable/key `DISCORD_BOT_TOKEN`.
    """

    load_dotenv()
    run(token=os.environ["DISCORD_BOT_TOKEN"], input_method=get_user_input)
