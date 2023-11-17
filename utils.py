"""Shared methods."""
import logging
import typing
import functools
import asyncio


FORMATTER = logging.Formatter(fmt="%(asctime)s %(levelname)-8s [%(funcName)s() in %(name)s:%(lineno)s] %(message)s",
                  datefmt="%H:%M:%S")

HANDLER = logging.StreamHandler()
HANDLER.setFormatter(FORMATTER)


def to_thread(func: typing.Callable):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)

    return wrapper