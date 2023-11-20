"""Contains the entry point script to initialise the different components of the Bot and
start the asyncio event loop. Handles environment variables and cli args."""

import argparse
import asyncio
import logging
import os
import sys
import api

import discord
import dotenv

import utils
from bot.music_client import build_client
from companion import CompanionConsole
from console import Command, build_console


_log = logging.getLogger(__name__)
_log.addHandler(utils.HANDLER)
_log.setLevel(logging.INFO)


def get_console_input() -> list[str]:
    """Get a line of input from the command-line, split by spaces."""
    instruction = ""
    while len(instruction) == 0:
        instruction = input()
    _log.debug("Received input '%s'.", instruction)
    return instruction.split(" ")


def run(token: str, hostname, port: int):
    """|Blocking| Starts the MusicClient Bot and its console interfaces."""

    discord.utils.setup_logging(
        handler=utils.HANDLER,
        formatter=utils.FORMATTER,
        level=logging.WARNING,
        root=False,
    )
    client = build_client()
    console = build_console(client)
    API = api.APIHandler(client, "__name__")
    _log.info("Opening TCP Socket @ %s/%s", hostname, port)
    web_console = CompanionConsole(console=console, hostname=hostname, port=port)

    async def shutdown():
        """|coro| Shuts down the Consoles and the Client."""

        _log.debug(
            "Received shutdown signal. Closing consoles and shutting down the Bot."
        )
        console.online = False
        web_console.stop()
        await client.quit()
        _log.info("BoBo says, 'Tata for now!'.")

    console.add_command(Command("quit", shutdown))

    async def runner():
        """|coro| Starts the coroutines of the Bot and its consoles, submitting
        them to the event loop."""

        await asyncio.gather(
            client.start(token=token, reconnect=True),
            console.start(get_console_input),
            web_console.start(),
            API.start(HOSTNAME, API_PORT)
        )

    try:
        asyncio.run(runner())
    except KeyboardInterrupt:
        _log.warning("Received Keyboard Interrupt signal. Service will shutdown.")
        return


if __name__ == "__main__":
    # Token controls access to the Discord bot.
    # For safety, it is passed through an environment variable.
    # You can set the environment variable in your shell,
    # or using a `.env` file as the variable/key `DISCORD_BOT_TOKEN`.

    HOSTNAME = "0.0.0.0"  # Defaults
    PORT = 5000
    API_PORT = 5050

    dotenv.load_dotenv()
    bot_token = os.environ.get("DISCORD_BOT_TOKEN", None)
    socket_hostname = os.environ.get("WEBSOCKET_HOSTNAME", HOSTNAME)
    socket_port = os.environ.get("WEBSOCKET_PORT", PORT)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t",
        "--TOKEN",
        help="Set the Bot TOKEN to use for connecting to Discord."
        + "\n\tWARNING: It is advisable to pass the token as an "
        + "environment variable in the `.env` file instead.",
    )
    parser.add_argument(
        "-n",
        "--HOSTNAME",
        help="Set the HOSTNAME to host the WebSocket on. Defaults to"
        + f" '{HOSTNAME}'.",
    )
    parser.add_argument(
        "-p",
        "--PORT",
        type=int,
        help=f"Set the PORT to host the WebSocket on. Defaults to '{PORT}'.",
    )
    parser.add_argument(
        "-a",
        "--API_PORT",
        type=int,
        help=f"Set the API PORt to host the API Handler on. Defaults to '{API_PORT}'",
    )
    args = parser.parse_args()

    if args.TOKEN:
        _log.warning(
            "Received Bot Token via CLI args. For safety, pass this as an environment"
            + " variable, or in the '.env' file instead."
        )
        bot_token = args.TOKEN
    if args.HOSTNAME:
        socket_hostname = args.HOSTNAME
    if args.PORT:
        socket_port = args.PORT

    if bot_token is None:
        _log.fatal("Required environment variable `DISCORD_BOT_TOKEN` is missing.")
        sys.exit(5)  # Auth Error.

    run(token=bot_token, hostname=socket_hostname, port=socket_port)
