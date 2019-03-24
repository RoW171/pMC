__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-03-10"
__version__ = "0.0.1"

from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM
from pmc.network.misc import hostname
from pmc.network.payload import Payload
from pmc.resources.io.serializer import json


class Server:
    def __init__(self):
        self.tcp = TCP(self)
        self.udp = UDP(self)


class TCP(socket):
    def __init__(self, controller, address=hostname(), port=12221):
        super(TCP, self).__init__(AF_INET, SOCK_STREAM)
        self.controller = controller
        self.clients = list()
        self.methods = dict()

        self.bind((address, port,))
        self.listen(5)

    def asign(self):
        try: connection, address, = self.accept()
        except (OSError,): pass  # TODO: show error here
        else: self.clients.append(ClientObject(self, connection, address))

    def read(self):
        client = self.clients[0]  # TODO: select something here
        try: message = client.connection.recv(2048)
        except (ConnectionResetError,): self.leave(client)
        else:
            if message is not b'':
                payload = Payload.UNPACK(message)
                self.methods[payload['code']](client, payload)

    @staticmethod
    def write(to, payload):
        if type(to) == ClientObject: to = to()
        if type(payload) == Payload: payload = payload.PACK()
        to.sendall(payload)

    def broadcast(self, payload):
        for client in self.clients: self.write(client, payload)

    def leave(self, client): pass


class UDP(socket):
    def __init__(self, controller, address=hostname(), port=12221):
        super(UDP, self).__init__(AF_INET, SOCK_DGRAM)
        self.controller = controller

        self.bind((address, port,))

    def read(self):
        message = self.recvfrom(2048)
        if message is not b'':
            message = json.loadObject(message)

    def write(self, adddress, message): self.sendto(message, adddress)

    def broadcast(self):
        for client in self.controller.tcp.clients:
            pass


class ClientObject:
    def __init__(self, server, connection, address):
        self.server = server
        self.connection = connection
        self.address = address
        self.name = None


if __name__ == '__main__': pass
