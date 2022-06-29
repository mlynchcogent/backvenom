#!/usr/bin/env python3
from socket import socket
from venomsrc.malware.malwarebase import MalwareGenerator
from venomsrc.endpoints.raw_server.polls.basepoll import Poll
from venomsrc.colored import Colors

class ModulePoll(Poll):

    def __init__(self, writer: object, reader: object, sess_key: str, malware_generator: MalwareGenerator):
        super().__init__(writer, reader, sess_key)
        self.listeners = malware_generator.listener
        self.info = malware_generator.info
        self.platforms = malware_generator.platforms
        self.requirements = malware_generator.requirements
        self.generate = malware_generator.generate
        self.requirements_dict = dict()
        for i in self.requirements:
            self.requirements_dict[i] = None

        self.colors = Colors()

    def help_cmd(self):
        return """ayuda"""

    async def start(self):
        while 1:
            command, argv, argc, cmd = await self.poll_cmdreceive()
            # argv  command splited
            # argc = len(argv)  total len
            # cmd = argv[0]

            if not command:
                break

            # check for one-word commands
            if command == "help":
                await self.utils.ssend(self.writer, self.help_cmd(), self.sess_key)
                continue

            if command == "back":
                await self.utils.ssend(self.writer, "OK", self.sess_key)
                return

            if command == "info":
                message = "\t" + self.info
                message += "\n\tPlatforms: " + ",".join(self.platforms)
                message += "\n\tListeners: " + ",".join(self.listeners)

                await self.utils.ssend(self.writer, message, self.sess_key)
                continue

            if command == "show options":
                message = "Malware options:\n\n"
                message += "\t" + self.colors.UNDERLINE + "Name\t" + "Value\n\n" + self.colors.ENDC
                for i in self.requirements_dict:
                    message += "\t" + i + "\t" + str(self.requirements_dict[i]) + "\n"

                await self.utils.ssend(self.writer, message, self.sess_key)
                continue

            if command == "generate":
                await self.utils.ssend(self.writer, self.generate(self.requirements_dict), self.sess_key)
                continue

            if cmd == "set":
                if argc != 3:
                    await self.utils.ssend(self.writer, "Use: set <OPTION> <VALUE>", self.sess_key)
                    continue
                if argv[1] in self.requirements_dict:
                    self.requirements_dict[argv[1]] = argv[2]
                    await self.utils.ssend(self.writer, argv[1] + " => " + argv[2], self.sess_key)
                    continue
                else:
                    await self.utils.ssend(self.writer, "Unkown value!", self.sess_key)
                    continue
            else:
                await self.utils.ssend(self.writer, "Command not found. Type 'help'", self.sess_key)
                continue