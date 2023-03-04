import argparse
import logging
import pathlib

import requests

import bot

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    args_parser = argparse.ArgumentParser(
        description = 'Connects to twitch chat, looks for the !up command, increases the dumbometer'
    )
    args_parser.add_argument('dumbometer_ip')
    args = args_parser.parse_args()

    dumbometer_url = f"http://{args.dumbometer_ip}/up"

    logger.debug("starting")

    up_bot = bot.Bot()
    up_bot.connect()

    while True:
        text = up_bot.receive()
        logger.debug(text)

        # TODO move to bot.py
        channel = "#mayonesia"
        if "PRIVMSG" in text and channel in text:
            if up_bot.parse(text) == '!up':
                logger.info("!up")
                requests.get(dumbometer_url)
