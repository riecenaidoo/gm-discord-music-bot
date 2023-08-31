import os
import asyncio
import discord
import bot
import dotenv


def get_console_input() -> list[str]:
    instruction = ""
    while len(instruction) == 0:
        instruction = input(" > ")

    return instruction.split(" ")


def run(token: str):
    """Blocking. Starts the MusicClient bot and its console interface."""
    
    discord.utils.setup_logging()
    client = bot.build_client()
    console = bot.build_console(client)
    
    async def runner():
        await asyncio.gather(client.start(token=token, reconnect=True), 
                             console.start(get_console_input))

    try:
        asyncio.run(runner())
    except KeyboardInterrupt:
        return
    
    
if __name__ == "__main__":
    """
    Token controls access to the Discord bot.
    For safety, it is passed through an environment variable.
    You can set the environment variable in your shell,
    or using a `.env` file as the variable/key `DISCORD_BOT_TOKEN`.
    """

    dotenv.load_dotenv()
    run(token=os.environ["DISCORD_BOT_TOKEN"])

discord.Client.run