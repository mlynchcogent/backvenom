#!/usr/bin/env python3

import hashlib
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from venomsrc.config import Config


class Crypto:
    """
    Crypto used methods
    generaterndchars
    generaterndsessid
    sha512_encrypt
    aes_encrypt
    aes_decrypt
    """
    def __init__(self):
        self.config = Config()  # Config vars

    @staticmethod
    def generaterndchars(size: int) -> str:
        """
        Generate random string len() given int
        :size: len of string to generate
        :return: random string
        """
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        chars += chars.lower()
        chars += '1234567890'
        chars += '#$%&/()[]{}-_.:,;'

        out = ''
        for _ in range(size):
            out += chars[random.randint(0, len(chars) - 1)]
        return out

    @staticmethod
    def generaterndsessid(size: int) -> int:
        """
        Generate random number of given size
        @param size: int
        @return: int
        """

        nums = '1234567890'

        out = ''
        for _ in range(size):
            out += nums[random.randint(0, len(nums) - 1)]
        return out

    @staticmethod
    def sha512_encrypt(data: str) -> str:
        """
            sha512 given string
            @data: string to hash
            @return: hashed string
        """
        try:
            data = data.encode()
        except (UnicodeDecodeError, AttributeError):
            pass
        return hashlib.sha512(data).hexdigest()

    def aes_encrypt(self, raw: str, key: str, mode=1, iv='') -> bytes:
        """
        AES Encrypt
        @param raw: string to erncrypt
        @param key: AES Stuff
        @param mode: ECB (1) vs CBC (2)
        @param iv: AES Stuff ( initialization vector )
        @return: Ciphered string
        """
        try:
            key = key.encode('latin_1')
        except:
            pass
        try:
            raw = raw.encode('latin_1')
        except:
            pass
        try:
            iv = iv.encode('latin_1')
        except:
            pass
        key = hashlib.sha256(key).digest()
        if (mode == 1):
            cipher = AES.new(key, AES.MODE_ECB)
        elif (mode == 2):
            cipher = AES.new(key, AES.MODE_CBC, iv)
        x = pad(raw, int(self.config.BLOCK_SIZE))
        return cipher.encrypt(x)

    def aes_decrypt(self, enc, key, mode=1, iv='') -> str:
        """
            AES Decrypt
            @param enc: String to decrypt
            @param key: AES Stuff
            @param mode: ECB (1) vs CBC (2)
            @param iv: AES Stuff ( initialization vector )
            @return: plain text string
        """
        try:
            key = key.encode('latin_1')
        except:
            pass
        try:
            enc = enc.encode('latin_1')
        except:
            pass
        key = hashlib.sha256(key).digest()
        if mode == 1:
            cipher = AES.new(key, AES.MODE_ECB)
        elif mode == 2:
            cipher = AES.new(key, AES.MODE_CBC, iv)
        x = cipher.decrypt(enc)
        return unpad(x, self.config.BLOCK_SIZE)
