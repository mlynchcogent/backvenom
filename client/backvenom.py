#!/usr/bin/env python3

import configparser
import socket
import sys
import os
from json import loads
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style
from venomsrc.banners import banner
from venomsrc.colored import Colors
from venomsrc.config import Config
from venomsrc.crypto import Crypto
from venomsrc.utils import Utils

__version__ = "0.0.1"


class Client:

    def __init__(self, SERVER_HOST: str , PORT: int) -> None:
        """
            Constructor
            :param SERVER_HOST: SRV to Connect
            :param PORT: Remote PORT
        """
        self.auth = {}
        self.path: str
        self.SERVER_HOST = SERVER_HOST
        self.PORT = PORT
        self.CONFIG = Config()
        self.utils = Utils()
        self.crypto = Crypto()
        self.config = Config()
        self.colors = Colors()
        self.module_loaded = False
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.session = PromptSession()  # CMD history
        self.payload_list = dict()
        self.style = Style.from_dict(
            {
                # Default style.
                "": "#ff0066",
                # Prompt.
                "backvenom": "#ffffff underline",
                "parenthesis": "#ffffff",
                "orange": "#ff8000",
                # "module": "",
                # "command": "#00aa00",
                # "host": "#000088 bg:#aaaaff",
                "path": "white",
                "path": "white",
                "red": "red",
                # Make a selection reverse/underlined.
                # (Use Control-Space to select.)
                "selected-text": "reverse underline",
                "listener": "",
                "option": "",
            }
        )

        self.completer = NestedCompleter.from_nested_dict({  # prompt help
            'start': {
                'listener': {
                    'tcp': None,
                    'http': None,
                    'https': None,
                    'icmp': None,
                    'dns': None
                },
            },
            'search': None,
            'generate': None,
            'list': {
                'listeners': None,
                'agents': None,
                'tasks': None
            },
            'stop': {
                'listener': None
            },
            'interact': None,
            'exit': None,
            'help': None,
            'banner': None,
        })
        self.lhost_completer = NestedCompleter.from_nested_dict({
            "127.0.0.1": None,
            "0.0.0.0": None
        }
        )

        self.lport_completer = NestedCompleter.from_nested_dict({
            "8080": None,
            "4444": None
        }
        )

    def cmd_input(self) -> str:
        """
            print command line input
            @return: user command
        """
        return self.session.prompt(HTML(
            "<backvenom>BV</backvenom>"
            "<command> > </command>"
        ), style=self.style, completer=self.completer, auto_suggest=AutoSuggestFromHistory())

    def malware_input(self) -> str:
        """
            print command line input when module loaded
            @return: user command
        """
        return self.session.prompt(HTML(
            "<backvenom>BV</backvenom>"
            " "
            "<path>" + str(self.path.split("/")[0]) + "</path>"
            "<parenthesis>(</parenthesis>"
            "<red>" + "/".join(self.path.split("/")[1:]) + "</red>"
            "<parenthesis>)</parenthesis>"
            "<command>> </command>"
        ), style=self.style)

    def listener_input(self, message: str) -> str:
        return self.session.prompt(HTML(
            (
            "<backvenom>BV</backvenom>"
            "<parenthesis>(</parenthesis>"
            "<Listener>Listener:</Listener>"
            "<orange>" + message + "</orange>"
            "<parenthesis>)</parenthesis>"
            "<command> > </command>")
        ), style=self.style, completer={True: self.lhost_completer, False: self.lport_completer}[message=="LHOST"])

    def payload_input(self) -> str:
        return self.session.prompt(HTML(
            (
            "<backvenom>BV</backvenom>"
            "<parenthesis>(</parenthesis>"
            "<Listener>Listener:</Listener>"
            "<orange>PAYLOAD</orange>"
            "<parenthesis>)</parenthesis>"
            "<command> > </command>")
        ), style=self.style, completer=NestedCompleter.from_nested_dict(self.payload_list))

    # TODO: si no tiene un módulo cargado usa el main en blanco y bv en negro, si hay algo cargado
        # invertirlo

    def end_session(self) -> None:
        """
            Ends server session
            @return: None
        """

        try:
            self._socket.close()
        except:
            pass

        sys.exit("bye!")

    def cmd_poll(self) -> None:
        """
            Generates user interactive cli, send commands to C2 using AES w/ server side generated string
            @param: Socket object
            @return: None
        """

        print("[*]  " + self.colors.OKGREEN + "Connected to server" + self.colors.ENDC)

        while 1:
            if self.module_loaded:
                command = self.malware_input().lower()
            else:
                command = self.cmd_input().lower()

            string_command = command
            if command == '' or command.replace(' ', '') == '':
                continue
            else:
                command = command.split()

            if string_command in ["cls", "clear", "clean"]:
                os.system("clear")

            elif string_command in ["exit", "quit", "q!", "bye"]:
                self.end_session()

            elif string_command in ["banner"]:
                banner(__version__)


            elif command[0] == 'start' and command[1] == 'listener':
                try:
                    ltype = command[2]
                except:
                    print("Specify protocol (tcp)")
                    continue
                lhost = self.listener_input("LHOST")
                lport = self.listener_input("LPORT")
                payload = self.payload_input()
                self.utils.ssend(self._socket, "start listener " + ltype + " " + lhost + " " + lport + " " + payload, self.auth["sess_key"])
                print(self.utils.srecv(self._socket, self.auth["sess_key"]).decode("utf-8"))

            elif command[0] == "use":
                try:
                    self.path = command[1].replace(".py", "")
                except:
                    print("Specify path")
                    continue
                self.utils.ssend(self._socket, "use " + self.path,
                                 self.auth["sess_key"])
                response = self.utils.srecv(self._socket, self.auth["sess_key"]).decode("utf-8")
                if response == "OK":
                    self.module_loaded = True

            elif command[0] == "back":
                self.utils.ssend(self._socket, "back",
                                 self.auth["sess_key"])
                response = self.utils.srecv(self._socket, self.auth["sess_key"]).decode("utf-8")
                if response == "OK":
                    self.module_loaded = False
            elif command[0] == "generate":
                self.utils.ssend(self._socket, "generate",
                                 self.auth["sess_key"])
                response = self.utils.srecv(self._socket, self.auth["sess_key"]).decode("utf-8")
                if response.startswith("ERROR: "):  # TODO: mejorar forma detectar error
                    print(response)
                else:
                    try:
                        with open(input("Insert filename: "), "wb") as f:
                            f.write(response.encode())
                            print("Done!")

                    except Exception as e:
                        print("Error: " + str(e))
            else:
                self.utils.ssend(self._socket, string_command, self.auth["sess_key"])

                try:
                    resp = self.utils.srecv(self._socket, self.auth["sess_key"]).decode("utf-8")
                except:
                    self.utils.log(self.utils.ERROR, "Error receiving data from server", 1)
                    break

                print(resp)

    def handshake(self) -> int:
        """
            Client side handshake
            1. Get random string generated by server
            2. AES it
            3. SHA512 it
            4. Send it
            5. Request and receive sess id and key
            @return: int
        """
        resp = self._socket.recv(self.CONFIG.RCV_BLOCK_SZ)  # receive server random string

        try:
            rnd_str, iv = resp.split(b'\xff')
        except:
            self.utils.log(self.utils.ERROR, '[-] Server returned unexpected response.', True)

        enc_rnd_str = self.crypto.aes_encrypt(rnd_str.decode('utf-8'), self.config.password)
        challenge_sol = Crypto.sha512_encrypt(enc_rnd_str)
        self._socket.send(challenge_sol.encode('utf-8'))  # send challenge
        resp = self._socket.recv(self.config.RCV_BLOCK_SZ).decode('utf-8')  # Server check
        if (resp != 'ACCESS_OK'):
            print(resp)
            return 0
        self._socket.send(b'REQ_SESS_KEYS')
        sess_info = self.utils.srecv(self._socket)  # receive server generated sess id and key
        try:
            sess_id, sess_key = sess_info.split(b"\xff")
        except:
            print('[-] Unexpected data received from server.')
            return 0
        self.auth["sess_id"] = sess_id.decode('utf-8')  # stored sess_id
        self.auth["sess_key"] = sess_key.decode('utf-8')  # stored sess_key

        return 1

    def run(self) -> None:
        """
            Connect to server and start auth challenge
            @return: bool
        """

        try:
            self._socket.connect((self.SERVER_HOST, self.PORT))
        except Exception as e:
            print(str(e))
            sys.exit("[-] Could not connect to C2 server")
        if (not self.handshake()):
            sys.exit('[-] Wrong credentials. Check configuration file.')

        try:
            try:
                self.payload_list = loads(self.utils.srecv(self._socket, self.auth["sess_key"]).decode("utf-8"))
            except:
                self.payload_list = {}
            self.cmd_poll()  # start server interaction
            sys.exit("Bye!")
        except KeyboardInterrupt:
            self.end_session()


if __name__ == "__main__":
    banner(__version__)  # random banner
    config = Config()
    parser = configparser.ConfigParser()
    parser.read(config.CONFIG_PATH)
    client = Client(parser.get("server", "rhost"), parser.getint("server", "rport"))
    client.run()
