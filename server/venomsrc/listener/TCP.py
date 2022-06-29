#!/usr/bin/env python3

import venomsrc.globals
from venomsrc.listener.listenerbase import Listener
from venomsrc.listener.exceptions import *
from venomsrc.utils import Utils
import asyncio
from multiprocessing import Process
from threading import Thread

class TCPServer:
    def __init__(self, lhost, lport, payload):
        self.lport = lport
        self.lhost = lhost
        self.payload = payload
        self.utils = Utils()

    async def handle_client(self, reader, writer) -> None:
        """
        Handle client connection
        """
        # enviar a donde sea ( usar self.payload ! )
        self.utils.log(self.utils.INFO, "Received agent!: '" + str(writer._transport.get_extra_info('peername')) + "'", True)

    async def run_server(self) -> None:
        try:
            server = await asyncio.start_server(self.handle_client, self.lhost, self.lport)
        except:
            self.utils.log(self.utils.INFO, "Error starting listener, port: " + str(self.lport), True)
            raise ErrorStartingListener

        async with server:
            self.utils.log(self.utils.INFO, "Starting listener on port " + str(self.lport), True)
            await server.serve_forever()


class TCPListener(Listener):
    """
    TCP Listener
    """
    def __init__(self, lhost, lport, payload):
        super().__init__(lhost, lport, payload)


    def create_asyncioprocess(self):
        server = TCPServer(self.lhost, self.lport, self.payload)
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(server.run_server())
        except ErrorStartingListener:
            raise ErrorStartingListener

    def init(self) -> bool:
        """
        Start TCP Server
        """
        try:
            self.server = Process(target=self.create_asyncioprocess)
        except ErrorStartingListener:
            return False
        try:
            self.daemon = Thread(target=self.server.start, args=())
        except ErrorStartingListener:
            return False

        self.daemon.daemon = True
        self.daemon.start()
        self.uuid = self.es_handler.indexListerner(self.data)
        return True

    def stop(self) -> None:
        """
        Stop TCP Server, remove from globals and BBDD
        """
        self.server.terminate()
        self.server = None
        self.daemon = None
        self.es_handler.removeListener(self)
        venomsrc.globals.listeners.remove(self)