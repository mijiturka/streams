import argparse
import logging
import pathlib

import requests

import bot

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def draw(message):
    logging.info(f"{message.sender} asked to draw {message.arguments}")

if __name__ == '__main__':
    logger.debug("starting")

    ai_bot = bot.Bot()
    ai_bot.connect()

    ai_bot.listen_and_react(
        action=draw,
        command="!ai",
    )
