import argparse
import logging
import pathlib

import requests

import bot

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

max_wishes = 3
wishes = {}

def draw(message):
    logging.info(f"{message.sender} asked to draw {message.arguments}")
    if message.sender not in wishes:
        wishes[message.sender] = 1
    else:
        wishes[message.sender] += 1

    if wishes[message.sender] > max_wishes:
        logging.warning(f"They've already spent their {max_wishes} wishes")
        return


if __name__ == '__main__':
    logger.debug("starting")

    ai_bot = bot.Bot()
    ai_bot.connect()

    ai_bot.listen_and_react(
        action=draw,
        command="!ai",
    )
