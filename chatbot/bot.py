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

logging.getLogger("irc.client")
logging.basicConfig(level=logging.DEBUG)

def parse(msg):
    return msg.split('PRIVMSG #mayonesia :')[1].strip()

class Bot:

    irc_socket = socket.socket()

    def __init__(self):
        self.irc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, channel, msg):
        self.irc_socket.send(bytes("PRIVMSG " + channel + " " + msg + "\n", "UTF-8"))

    def connect(self, server, port, channel, bot_nick, bot_pass):
        print("Server connection: " + server)
        self.irc_socket.connect((server, port))

        self.irc_socket.send(bytes("PASS " + bot_pass + "\n", "UTF-8"))
        self.irc_socket.send(bytes("NICK " + bot_nick + "\n", "UTF-8"))
        time.sleep(2)
        self.irc_socket.send(bytes("JOIN " + channel + "\n", "UTF-8"))

    def response(self):
        r = self.irc_socket.recv(2040).decode("UTF-8")
        if r.find('PING') != -1:
            # TODO don't hardcode what to PONG
            self.irc_socket.send(bytes('PONG :tmi.twitch.tv' + '\r\n', "UTF-8"))
        return r

if __name__ == '__main__':
    logging.debug("starting")

    bot = Bot()
    bot.connect(server_hostname, irc_port, channel, bot_username, bot_password)

    while True:
        text = bot.response()
        logging.debug(text)

        if "PRIVMSG" in text and channel in text:
            if parse(text) == '!up':
                print("UP!")
                requests.get(f"http://{dumbometer_ip}/up")
