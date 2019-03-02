__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-03-02"
__version__ = "0.0.1"

from pmc.resources.io.serializer import json
from datetime import datetime


class Payload:
    def __init__(self, code, message, args=None):
        self.code = code
        self.message = message
        self.time = datetime.now()
        if args is None: args = dict()
        self.args = args

    def __repr__(self): return '------\n\'{}\': {}\ntime: {}\n------'.format(self.code, self.message, self.time)

    __str__ = __repr__

    def PACK(self): return json.dumpObject(self.__dict__)

    @staticmethod
    def UNPACK(payload): return Payload('', '').__dict__.update(json.loadObject(payload))


if __name__ == '__main__': pass
