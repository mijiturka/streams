import argparse
import logging

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

    up_bot.listen_and_react(
        # Disregard message details and just go for it
        action=lambda msg: requests.get(dumbometer_url),
        command="!up",
    )
