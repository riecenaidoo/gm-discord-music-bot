"""Contains the entry point script to initialise the different components of the Bot and
start the asyncio event loop. Handles environment variables and cli args."""

import sys
import os
import logging
import asyncio
# Installed
import discord
import dotenv
# Local
import bot
import utils
from server import WebSocketConsole
from console import Command


_log = logging.getLogger(__name__)
_log.addHandler(utils.HANDLER)
_log.setLevel(logging.INFO)


def get_console_input() -> list[str]:
    instruction = ""
    while len(instruction) == 0:
        instruction = input()
    _log.debug(f"Received input '{instruction}'.")
    return instruction.split(" ")


def run(token: str, hostname, port: int):
    """|Blocking| Starts the MusicClient Bot and its console interfaces."""
    
    discord.utils.setup_logging(handler=utils.HANDLER, formatter=utils.FORMATTER, level=logging.WARNING, root=False)
    client = bot.build_client()
    console = bot.build_console(client)
    _log.info(f"Starting WebSocket @ {hostname}/{port}")
    web_console = WebSocketConsole(console=console, hostname=hostname, port=port)
    
    async def quit():
        """|coro| Shuts down the Consoles and the Client."""
        
        _log.debug("Received shutdown signal. Closing consoles and shutting down the Bot.")
        console.online = False
        web_console.stop()
        await client.quit()
        _log.info("BoBo says, 'Tata for now!'.")
        
    console.add_command(Command("quit", quit))
    
    async def runner():
        """|coro| Starts the coroutines of the Bot and its consoles, submitting
        them to the event loop."""
        
        await asyncio.gather(client.start(token=token, reconnect=True), 
                             console.start(get_console_input),
                             web_console.start())

    try:
        asyncio.run(runner())
    except KeyboardInterrupt:
        _log.warning("Received Keyboard Interrupt signal. Service will shutdown.")
        return
    
    
if __name__ == "__main__":
    """
    Token controls access to the Discord bot.
    For safety, it is passed through an environment variable.
    You can set the environment variable in your shell,
    or using a `.env` file as the variable/key `DISCORD_BOT_TOKEN`.
    """

    dotenv.load_dotenv()
    bot_token = os.environ.get("DISCORD_BOT_TOKEN")
    socket_hostname = os.environ.get("WEBSOCKET_HOSTNAME", "localhost")
    socket_port = os.environ.get("WEBSOCKET_PORT", 5000)
    
    if bot_token == None:
        _log.fatal("Required environment variable `DISCORD_BOT_TOKEN` is missing.")
        sys.exit(5)   # Auth Error.


    run(token=bot_token,hostname=socket_hostname,port=socket_port)
