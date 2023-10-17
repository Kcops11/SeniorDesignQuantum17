import qiskit  # Ensure you have Qiskit installed
import socket

class nodeComputer:
    def __init__(self, router_host, router_port):
        self.router_host = router_host
        self.router_port = router_port
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.serverSocket = socket.socket()
        self.serverSocket.connect((self.router_host, self.router_port))

    def recieveMessage(self):
        message = self.serverSocket.recv(1024).decode('ascii')
        print(message)
        if message == "quit":
            self.closeSocket()

    def sendMessage(self, message):
        self.serverSocket.send(message.encode('ascii'))
        if message == "quit":
            self.closeSocket()

    def closeSocket(self):
        self.serverSocket.close()

