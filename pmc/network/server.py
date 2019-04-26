__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-03-10"
__version__ = "0.0.1"

from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM
from select import select
from pmc.network.misc import hostname
from pmc.network.payload import Payload
from pmc.resources.io.serializer import json


class Server:
    def __init__(self):
        self.tcp = TCP(self)
        self.udp = UDP(self)

        self.clients = list()

        self.servers = [
            self.tcp,
            self.udp,
        ]

        self.loop()  # TODO: it should't be necessary but this might have to run on a separate thread

    def loop(self):
        while True:
            readable, writable, exception, = select(self.servers, [], self.servers)

            for s in readable:
                if s == self.tcp:
                    self.tcp.accept()
                    self.tcp.read()
                elif s == self.udp:
                    self.udp.read()
                    self.udp.broadcast()


class TCP(socket):
    def __init__(self, controller, address=hostname(), port=12221):
        super(TCP, self).__init__(AF_INET, SOCK_STREAM)
        self.setblocking(0)
        self.controller = controller
        self.methods = dict()

        self.bind((address, port,))
        self.listen(5)

    def asign(self):
        try: connection, address, = self.accept()
        except (OSError,): pass  # TODO: show error here
        else:
            self.clients.append(ClientObject(self, connection))
            self.write(connection, Payload('accept', '', {'players': len(self.controller.clients),
                                                          'seed': None, 'id': len(self.controller.clients) - 1}))

    def read(self):
        client = self.controller.clients[0]  # TODO: select something here
        try: message = client.connection.recv(2048)
        except (ConnectionResetError,): self.leave(client)
        else:
            if message is not b'':
                payload = Payload.UNPACK(message)
                self.methods[payload['code']](client, payload)

    @staticmethod
    def write(to, payload):
        if type(to) == ClientObject: to = to.connection
        if type(payload) == Payload: payload = payload.PACK()
        to.sendall(payload)

    def broadcast(self, payload):
        for client in self.controller.clients: self.write(client, payload)

    def leave(self, client):
        client.connection.close()
        self.controller.clients.remove(client)


class UDP(socket):
    def __init__(self, controller, address=hostname(), port=12221):
        super(UDP, self).__init__(AF_INET, SOCK_DGRAM)
        self.controller = controller

        self.bind((address, port,))

    def read(self):
        message = self.recvfrom(2048)
        if message is not b'': self.controller.process(json.loadObject(message))

    def write(self, adddress, message): self.sendto(message, adddress)

    def broadcast(self, message):
        for client in self.controller.clients: self.write(client.peer, message)


class ClientObject:
    def __init__(self, server, connection):
        self.server = server
        self.connection = connection
        self.peer = self.connection.getpeername()
        self.local = self.connection.getsockname()
        self.name = None


if __name__ == '__main__': pass
