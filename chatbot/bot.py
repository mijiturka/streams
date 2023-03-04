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


class Message:
    def __init__(self, channel, msg):
        sender, payload = [part.strip() for part in msg.split(f'PRIVMSG {channel} :')]
        self.sender = sender
        self.payload = payload

        self.command = None
        self.arguments = None

        if payload.startswith('!'):
            try:
                command, arguments = [part.strip() for part in payload.split(' ', 1)]
                if arguments == "":
                    arguments = None
                self.command = command
                self.arguments = arguments
            except ValueError:
                # this command has no arguments
                self.command = payload
                self.arguments = None

    def __repr__(self):
        return str({
            'sender': self.sender,
            'command': self.command,
            'arguments': self.arguments,
            'payload': self.payload
        })

    def __str__(self):
        return f"{self.sender}:_{self.command}_{self.arguments}"

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
        # Connection set-up
        self.server = server
        self.port = port

        self.channel = channel

        self.nick = nick
        if token is None:
            self.token = get_token()
        self.password = f"oauth:{self.token}"

        # This bot will only listen for one command, and perform one action as a result
        self._listening = False

        # Other stuff bot needs
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

    def listen_and_react(self, action, command):
        logger.debug("listen_and_react() called")
        # Shouldn't really happen because we're busy-looping; so can't get to a second function call.
        # Placing this here just in case I forget about this when making changes
        if self._listening:
            raise Exception(
                "Bot is not a multifuncitonal pony. "
                "It's already listening for a command. "
                "call .stop_listening() first if you want to make it listen for something else."
            )
        self._listening = True

        while self._listening:
            text = self.receive()
            logger.debug(text)

            if "PRIVMSG" in text and self.channel in text:
                msg = Message(self.channel, text)
                logging.debug(msg)

                if msg.command == command:
                    logger.info(f"command={msg.command}")
                    action(msg)

    def stop_listening(self):
        self._listening = False
