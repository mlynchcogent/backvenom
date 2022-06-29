#!/usr/bin/env python3
from abc import ABC, abstractmethod
from venomsrc.listener.exceptions import InvalidPort
import venomsrc.globals
from venomsrc.database.elastic import ElasticHandler
from venomsrc.utils import Utils

class Listener(ABC):
    """
    Listeners inherit from this class, SHOULD HAVE defined abstract methods
    """

    def __init__(self, *args):
        self.lport = args[1]
        self.lhost = args[0]
        self.payload = args[-1]
        self.data = {
            "lhost": self.lhost,
            "lport": self.lport,
            "payload": self.payload,
            "category": str(self)
        }
        self.es_handler = ElasticHandler()
        if not self.lport.isnumeric():
            raise InvalidPort("Invalid port!")
        # check if is valid payload for type

        venomsrc.globals.listeners.append(self)



    def __str__(self) -> str:
        """
        Return child class name called from str()
        """
        return self.__class__.__name__

    @abstractmethod
    def init(self) -> bool:
        """ Send lport and lhost to payload handler instance
        then send to elastic info
        """
        pass

    @abstractmethod
    def stop(self):
        pass