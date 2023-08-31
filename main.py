import os
import asyncio
import discord
import bot
import dotenv
import server
from console import Command

def get_console_input() -> list[str]:
    instruction = ""
    while len(instruction) == 0:
        instruction = input(" > ")

    return instruction.split(" ")


def run(token: str, hostname, port: int):
    """Blocking. Starts the MusicClient bot and its console interface."""
    
    discord.utils.setup_logging()
    client = bot.build_client()
    console = bot.build_console(client)
    web_console = server.WebSocketConsole(console=console, hostname=hostname, port=port)
    
    async def quit():
        """Shuts down the Console and the Client."""
        console.online = False
        web_console.stop()
        await client.quit()
        
    console.add_command(Command("quit", quit))
    
    async def runner():
        await asyncio.gather(client.start(token=token, reconnect=True), 
                             console.start(get_console_input),
                             web_console.start())

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
    run(token=os.environ["DISCORD_BOT_TOKEN"],hostname="localhost",port=5000)

discord.Client.run