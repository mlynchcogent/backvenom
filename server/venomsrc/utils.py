#!/usr/bin/env python3

from venomsrc.config import Config
from venomsrc.crypto import Crypto
from venomsrc.colored import Colors
import os
from datetime import datetime
from json import dumps
import venomsrc.globals

class Utils:
    """
        multiple useful methods:
        log: Logging
        ssend: Secure Socket send
        srecv: Secure Socket recv
    """
    def __init__(self):
        self.CONFIG = Config()  # config file vars
        self.crypto = Crypto() # Crypto Utils
        # DEBUG type  message print
        self.INFO = 0
        self.WARNING = 1
        self.OK = 2
        self.ERROR = 3


    @staticmethod
    def getPayloads() -> str:
        """
        Return .py files from modules/malware
        """
        file_set = set()
        for dir_, _, files in os.walk("modules/malware"):
            for file_name in files:
                rel_dir = os.path.relpath(dir_, "modules/malware")
                rel_file = os.path.join(rel_dir, file_name)
                file_set.add(rel_file)
        return dumps(dict.fromkeys([malware for malware in file_set if malware.endswith(".py")], None))

    @staticmethod
    def currentListeners():
        """ return dict with current listeners"""
        listener_list = dict()
        for listener in venomsrc.globals.listeners:
            listener_list[str(listener)] = {"payload": listener.payload, "lport": str(listener.lport),
                                            "UUID": str(listener.uuid)
                                            }
        return listener_list

    def log(self, mode: int, toprint: str, log: bool) -> None:
        """
            if CONFIG DEBUG is True, print message.
            if log is True (arg log), save to logging path
            @param mode: message type
            @param toprint: message to print
            @param log: log to file ?
            @return: None
        """
        message = str(datetime.now())
        if mode == 0:
            save_log = message + " [INFO] " + toprint
            message += " [\033[96mINFO\033[0m] " + toprint
        elif mode == 1:
            save_log = message + " [WARNING] " + toprint
            message += " [\033[93mWARNING\033[0m] " + toprint
        elif mode == 2:
            save_log = message + " [OK] " + toprint
            message += " [\033[92mOK\033[0m] " + toprint
        else:
            save_log = message + " [INFO] " + toprint
            message += " [\033[91mERROR\033[0m] " + toprint

        message += '\n'
        save_log += '\n'

        if (self.CONFIG.DEBUG):
            print(message, end='')

        if log:
            with open(self.CONFIG.LOGGING_PATH, "a+") as f:
                f.writelines(save_log)

    async def ssend(self, writer: object, string: str, password="") -> None:
        """
        Socket secure AES send
        @param write: async socket object
        @param string: string to send
        @param password: password generated by server
        @return: None
        """

        if not password:
            password = Config.getPass()
        try:
            writer.write(self.crypto.aes_encrypt(string, password))
            await writer.drain()
        except Exception as e:
            print(str(e))
            exit()
            self.log(self.ERROR, "Error sending data", 1)

    async def srecv(self, reader: object, password="") -> str:
        """
        Socket secure AES recv
        @param reader: async socket object
        @return: plain text string
        @param password: password generated by server

        @return: Socket received string
        """
        if not password:
            password = Config.getPass()

        try:
            data = (await reader.read(self.CONFIG.RCV_BLOCK_SZ))
            if not data:
                return 0
            return self.crypto.aes_decrypt(data, password).strip()
        except Exception as e:
            print(e)
            self.log(self.ERROR, "Error receiving data", 1)