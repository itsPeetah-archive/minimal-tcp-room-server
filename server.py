from socket import *
from threading import Thread

# Settings ======================================================
# Network
defaultHostname = "localhost"
defaultPort = 42069


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
            Thread(target=ServerMethods.newConnectionHandler,
                   args=[newSocket, clientAddress]).start()

    @staticmethod
    def addClientToRoom(sock, addr, room):
        pass

    @staticmethod
    def removeClient(sock, addr):
        pass


class ServerMethods:

    @staticmethod
    def newConnectionHandler(sock, addr):
        pass

    @staticmethod
    def clientListener(sock, addr):
        pass

    @staticmethod
    def clientSpeaker(sock, addr):
        pass


def main(server_hostname, server_port, backlog=50):
    TCPServer.init(server_hostname, server_port, backlog)
    TCPServer.start()


if __name__ == "__main__":
    main(defaultHostname, defaultPort)
