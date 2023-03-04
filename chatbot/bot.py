import logging
import pathlib
import socket
import time

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

defaults = {
    "server": "irc.chat.twitch.tv",
    "port": 6667,
    "channel": "#mayonesia",
    "nick": "mayonesia",
}

def default(value):
    return defaults[value]

def get_token():
    return pathlib.Path('./token').read_text().strip()

class Bot:

    irc_socket = socket.socket()

    def __init__(self,
        server=default('server'),
        port=default('port'),
        channel=default('channel'),
        nick=default('nick'),
        token=None,
        password=None,
    ):

        self.server = server
        self.port = port

        self.channel = channel

        self.nick = nick
        if token is None:
            self.token = get_token()
        self.password = f"oauth:{self.token}"

        self.irc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.encoding = "UTF-8"

    def message(self, text):
        self.irc_socket.send(bytes(text + "\n", self.encoding))

    def connect(self):
        logger.info(f"Connecting to server {self.server}")
        self.irc_socket.connect((self.server, self.port))

        self.message(f"PASS {self.password}")
        self.message(f"NICK {self.nick}")
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
