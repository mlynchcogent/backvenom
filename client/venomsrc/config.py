#!/usr/bin/env python3
import configparser
import sys


class Config:

    def __init__(self) -> None:
        """
        Object with config attrs ( from backvenom.conf file )
        """
        self.CONFIG_PATH = "config/backvenom.conf"
        parser = configparser.ConfigParser()

        try:
            with open(self.CONFIG_PATH) as f:
                parser.read(self.CONFIG_PATH)
        except IOError:
            sys.exit("[!] Error opening config file")

        self.LOGGING_PATH = parser.get("config", "LOGGING_PATH")
        self.RCV_BLOCK_SZ = parser.getint("config", "RCV_BLOCK_SZ")
        self.DEBUG = parser.get("config", "DEBUG")
        self.password = parser.get("login", "password")
        self.BLOCK_SIZE = parser.getint("config", "BLOCK_SIZE")
