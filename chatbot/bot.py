import logging
import pathlib
import socket
import time

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

defaults = {
    "server_hostname": "irc.chat.twitch.tv",
    "irc_port": 6667,
    "channel": "#mayonesia",
    "bot_username": "mayonesia",
}

def default(value):
    return defaults[value]

class Bot:

    irc_socket = socket.socket()

    def __init__(self,
        server_hostname=default('server_hostname'),
        irc_port=default('irc_port'),
        channel=default('channel'),
        bot_username=default('bot_username'),
        token=None,
        bot_password=None,
    ):

        self.server_hostname = server_hostname
        self.irc_port = irc_port

        self.channel = channel

        self.bot_username = bot_username
        if token is None:
            self.token = pathlib.Path('./token').read_text().strip()
        self.bot_password = f"oauth:{self.token}"        

        self.irc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.encoding = "UTF-8"

    def message(self, text):
        self.irc_socket.send(bytes(text + "\n", self.encoding))

    def connect(self):
        logger.info(f"Connecting to server {self.server_hostname}")
        self.irc_socket.connect((self.server_hostname, self.irc_port))

        self.message(f"PASS {self.bot_password}")
        self.message(f"NICK {self.bot_username}")
        time.sleep(2)
        self.message(f"JOIN {self.channel}")

    def send(self, msg):
        self.message(f"PRIVMSG {self.channel} {msg}")

    def receive(self):
        r = self.irc_socket.recv(2040).decode(self.encoding)
        if r.find('PING') != -1:
            # TODO don't hardcode what to PONG
            self.message('PONG :tmi.twitch.tv\r')
        return r

    def parse(self, msg):
        return msg.split(f'PRIVMSG {self.channel} :')[1].strip()
