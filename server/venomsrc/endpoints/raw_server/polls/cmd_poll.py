#/usr/bin/env python3

from json import loads
import venomsrc.listener.TCP

from venomsrc.listener.exceptions import *
import venomsrc.globals
from venomsrc.colored import Colors
from venomsrc.utils import Utils

from venomsrc.endpoints.raw_server.polls.basepoll import Poll
from venomsrc.endpoints.raw_server.polls.module_poll import ModulePoll

class CMD(Poll):
    """
    Handle client commands from raw_server
    """

    def __init__(self, writer: object, reader: object, sess_key: str):
        super().__init__(writer, reader, sess_key)

    def my_import(self, module):
        mod = __import__(module)
        components = module.split('.')
        for comp in components[1:]:
            mod = getattr(mod, comp)
        return mod

    def help_cmd(self) -> str:
        """
        return formatted help message to send
        """
        help = ""
        help += "\n"
        help += (self.colors.UNDERLINE + "Core commands" + self.colors.ENDC + "\n")
        help += (
                    self.colors.BOLD + "\tcomand" + self.colors.ENDC + self.colors.BOLD + "\t\tDescription" + self.colors.ENDC + "\n")
        help += ("\tinteract\tinteract with agents by ID" + "\n")
        help += ("\tbanner\t\tprint random banner" + "\n")
        help += ("\tlist\t\tlist <listeners | agents | tasks>" + "\n")
        help += ("\texit\t\tEnd current client agents   " + "\n")

        help += ("\n" + self.colors.UNDERLINE + "Generators" + self.colors.ENDC + "\n")
        help += (
                    self.colors.BOLD + "\tcomand" + self.colors.ENDC + self.colors.BOLD + "\t\tDescription" + self.colors.ENDC + "\n")
        help += ("\tuse\t\tUse module" + "\n")
        help += ("\tsearch\t\tEnd current search <text>" + "\n")

        help += ("\n" + self.colors.UNDERLINE + "Listener commands" + self.colors.ENDC + "\n")
        help += (
                    self.colors.BOLD + "\tcomand" + self.colors.ENDC + self.colors.BOLD + "\t\tDescription" + self.colors.ENDC + "\n")
        help += ("\tstart\t\tstart listener <ICMP | DNS | TCP | HTTP | HTTPS> <optional>" + "\n")
        help += ("\tstop\t\tstop listener <id>" + "\n")
        help += "\n"

        return help

    async def start(self) -> None:
        """
        receive commands from client
        @param: self.reader: async socket object
        @param: self.writer: async socket object
        @param: sess_id: sess_id -> access sess info w/ globals
        @return: None
        """
        while 1:
            command, argv, argc, cmd = await self.poll_cmdreceive()
            if command == "UnicodeError":
                await self.utils.ssend(self.writer, "[!] Decode Error!: " + str(argv), self.sess_key)  # if command returns UnicodeError uses 2 arg as debug message
                continue

            if not command:
                break

            # check for one-word commands
            if command == "help":
                await self.utils.ssend(self.writer, self.help_cmd(), self.sess_key)
                continue

            if cmd == "start":
                if argc <= 1:
                    await self.utils.ssend(self.writer, "Use: start listener <proto> <port>", self.sess_key)
                    continue

                if argv[1] == "listener":
                    try:
                        proto = argv[2]
                        lhost = argv[3]
                        lport = argv[4]
                        payload = argv[5]
                    except:
                        await self.utils.ssend(self.writer, "Invalid options",
                                               self.sess_key)
                        continue
                    if proto == "tcp":

                        tcp_handle = venomsrc.listener.TCP.TCPListener(lhost, lport, payload)

                        if not tcp_handle.init():
                            await self.utils.ssend(self.writer, "Cant start listener!",
                                                   self.sess_key)
                            self.utils.log(self.utils.ERROR, "Cant start listener: " + str(lport), 1)
                            continue

                        await self.utils.ssend(self.writer, "Started TCP Listener\n", self.sess_key)
                        continue

                    else:
                        await self.utils.ssend(self.writer, "Invalid proto", self.sess_key)
                        continue
                else:
                    await self.utils.ssend(self.writer, argv[1], self.sess_key)
                    continue

            elif cmd == "stop":
                if argc < 2:
                    await self.utils.ssend(self.writer, "Use: stop listener <id>", self.sess_key)
                    continue

                if argv[1] == "listener":
                    if argc < 2:
                        await self.utils.ssend(self.writer, "Use: list listener <UUID>", self.sess_key)
                        continue

                    for i in venomsrc.globals.listeners:
                        if i.uuid.__str__() == argv[2]:
                            i.stop()
                            await self.utils.ssend(self.writer, "OK!", self.sess_key)
                            break
                    await self.utils.ssend(self.writer, "UUID Not found", self.sess_key)
                    continue

                else:
                    await self.utils.ssend(self.writer, "Use: stop listener <id>", self.sess_key)
                    continue

            elif cmd == "list":

                if argc < 2:
                    await self.utils.ssend(self.writer, "Available: listeners, sessions etc", self.sess_key)
                    continue

                if argv[1] == "listeners":
                    message = "PROTOCOL\tPAYLOAD\t\tPORT\t\tUUID\n\n"
                    listener_list = Utils.currentListeners()
                    for listener in listener_list:
                            message += listener + "\t" + listener_list[listener]["payload"] + "\t" + listener_list[listener]["lport"] + "\t\t" + listener_list[listener]["UUID"] + "\n"
                    await self.utils.ssend(self.writer, message, self.sess_key)
                    continue

                elif argv[1] == "agents":
                    # code to list agents
                    continue

                elif argv[1] == "tasks":
                    # code to list tasks
                    continue
                else:
                    await self.utils.ssend(self.writer, "Available: listeners, agents etc", self.sess_key)
                    continue

            elif cmd == "interact":
                await self.utils.ssend(self.writer, " ", self.sess_key)
                continue
            elif cmd == "use":
                try:
                    malware_module = self.my_import("modules.malware." + argv[1].replace("/", ".").replace(".py", ""))
                except ModuleNotFoundError:
                    await self.utils.ssend(self.writer, "Module not found!", self.sess_key)
                    # code to generate malware?., TODO: nope, we are using modules!
                    continue

                except NameError as e:
                    await self.utils.ssend(self.writer, "Check module: " + str(e), self.sess_key)
                    # code to generate malware?., TODO: nope, we are using modules!
                    continue

                except Exception as e:
                    await self.utils.ssend(self.writer, "Error importing!: " + str(e), self.sess_key)
                    continue

                try:
                    module_handler = malware_module.Generator()
                except Exception as e:
                    await self.utils.ssend(self.writer, "Malware class seems to be not defined: " + str(e), self.sess_key)
                    continue

                await self.utils.ssend(self.writer, "OK", self.sess_key)

                module_poll = ModulePoll(self.writer, self.reader, self.sess_key, module_handler)
                await module_poll.start()

                continue

            elif cmd == "search":
                tosearch = argv[1]
                message = "\n"

                for module in loads(self.utils.getPayloads()):
                    if tosearch in module:
                        message += module + "\n"

                await self.utils.ssend(self.writer, message, self.sess_key)
                continue

            else:
                await self.utils.ssend(self.writer, "Command not found. Type 'help'", self.sess_key)
                continue