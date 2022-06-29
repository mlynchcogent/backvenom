#!/usr/bin/env python3
import configparser
import sys
import os

class Config:
    """
    Class with config attrs ( from backvenom.conf file )
    """
    def __init__(self) -> None:
        self.CONFIG_PATH = "config/backvenom.conf"
        parser = configparser.ConfigParser()
        self.active = list()  # active services for docker compose
        try:
            with open(self.CONFIG_PATH) as f:
                parser.read(self.CONFIG_PATH)
        except IOError:
            sys.exit("[!] Error opening config file")

        self.LOGGING_PATH = parser.get("config", "LOGGING_PATH")  # used for log file
        self.RCV_BLOCK_SZ = parser.getint("config", "RCV_BLOCK_SZ")  # Socket receive size
        self.DEBUG = parser.get("config", "DEBUG")  # print debug messages?

        self.CERT_FILE = parser.get("certificate", "CERT_FILE")  # cert path
        self.KEY_FILE = parser.get("certificate", "KEY_FILE")  # cert path

        self.MAX_CLIENTS = parser.getint("config", "MAX_CLIENTS")  # Server max clients
        self.BLOCK_SIZE = parser.getint("config", "BLOCK_SIZE")  # AES Stuff

        self.LHOST = parser.get("server", "lhost")  # Server LHOST
        self.LPORT = parser.getint("server", "lport")  # Server LPORT

    @staticmethod
    def getPass():
        return os.environ["BACKVENOM_PASSWORD"]  # used for server/API passwd