from atexit import register
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from time import sleep

from numpy import broadcast

# Settings ======================================================
# Network
defaultHostname = "localhost"
defaultPort = 42069
# Misc
UTF8 = "utf-8"


class TCPServer:
    socket = None
    rooms = {}
    clients = {}

    @staticmethod
    def init():
        TCPServer.socket = socket(AF_INET, SOCK_STREAM)
        TCPServer.socket.bind((defaultHostname, defaultPort))

    @staticmethod
    def start(backlog=50):
        TCPServer.socket.listen(backlog)

        while True:
            newSocket, clientAddress = TCPServer.socket.accept()
            Thread(target=TCPServer.newConnectionHandler,
                   args=[newSocket, clientAddress]).start()

    @staticmethod
    def newConnectionHandler(sock: socket, addr):
        room = sock.recv(2048).decode(UTF8)
        id = TCPServer.addClientToRoom(sock, addr, room)

        # Build send message function
        def sendMessage(msg): return TCPServer.broadcast(
            sock, addr, room, id, msg)

        def clientListener():
            TCPServer.registerClientForBroadcasting(sock, addr, room)
            try:
                while True:
                    msg = sock.recv(2048).decode(UTF8)
                    Thread(target=sendMessage, args=(msg)).start()
            except:
                TCPServer.removeClient(sock, addr)

        sock.send(str(id).encode(UTF8))
        sleep(1)
        Thread(target=clientListener).start()

    @staticmethod
    def addClientToRoom(sock, addr, room):
        if room not in TCPServer.rooms:
            TCPServer.rooms[room] = [(sock, addr)]
            return 0
        else:
            TCPServer.rooms[room].append((sock, addr))
            # Not sure about thread safety, I'm going to look for the right element
            for i, t in enumerate(TCPServer.rooms[room]):
                if t[0] == sock:
                    return i
            # Should not be needed
            return i

    @staticmethod
    def registerClientForBroadcasting(sock, addr, room):
        # TCPServer.clients[sock]
        pass

    @staticmethod
    def removeClient(sock, addr):
        pass

    @staticmethod
    def broadcast(sock, addr, room, id, msg):
        pass


def main(server_hostname, server_port, backlog=50):
    TCPServer.init(server_hostname, server_port, backlog)
    TCPServer.start()


if __name__ == "__main__":
    main(defaultHostname, defaultPort)
