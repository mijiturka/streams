import argparse
import logging
import pathlib
import socket
import sys
import time

import requests

dumbometer_ip = "ADD"
server_hostname = "irc.chat.twitch.tv"
irc_port = 6667
channel = "#mayonesia"
bot_username = "mayonesia"
token = pathlib.Path('./token').read_text().strip()
bot_password = f"oauth:{token}"


logging.basicConfig(level=logging.DEBUG)

class Bot:

    irc_socket = socket.socket()

    def __init__(self):
        self.encoding = "UTF-8"
        self.irc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def message(self, text):
        self.irc_socket.send(bytes(text + "\n", self.encoding))

    def connect(self, server, port, channel, bot_nick, bot_pass):
        logging.info(f"Connecting to server {server}")
        self.irc_socket.connect((server, port))

        self.message(f"PASS {bot_pass}")
        self.message(f"NICK {bot_nick}")
        time.sleep(2)
        self.message(f"JOIN {channel}")

    def send(self, channel, msg):
        self.message(f"PRIVMSG {channel} {msg}")

    def receive(self):
        r = self.irc_socket.recv(2040).decode(self.encoding)
        if r.find('PING') != -1:
            # TODO don't hardcode what to PONG
            self.message('PONG :tmi.twitch.tv\r')
        return r

def parse(msg):
    return msg.split(f'PRIVMSG {channel} :')[1].strip()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description = 'Connects to twitch chat, looks for the !up command, increases the dumbometer'
    )
    parser.add_argument('dumbometer_ip')
    args = parser.parse_args()

    dumbometer_url = f"http://{args.dumbometer_ip}/up"

    logging.debug("starting")

    bot = Bot()
    bot.connect(server_hostname, irc_port, channel, bot_username, bot_password)

    while True:
        text = bot.receive()
        logging.debug(text)

        if "PRIVMSG" in text and channel in text:
            if parse(text) == '!up':
                logging.info("!up")
                requests.get(dumbometer_url)
