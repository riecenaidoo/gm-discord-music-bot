"""Shared methods."""

import logging

FORMATTER = logging.Formatter(fmt="%(asctime)s %(levelname)-8s [%(funcName)s() in %(name)s:%(lineno)s] %(message)s",
                  datefmt="%H:%M:%S")

HANDLER = logging.StreamHandler()
HANDLER.setFormatter(FORMATTER)