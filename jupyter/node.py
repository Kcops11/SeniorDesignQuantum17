import qiskit  # Ensure you have Qiskit installed
import socket
import threading
import time

class nodeComputer:
    def __init__(self, router_host, router_port, ip):
        self.router_host = router_host
        self.router_port = router_port
        self.ip = ip
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.serverSocket = socket.socket()
        self.serverSocket.connect((self.router_host, self.router_port))
        
        t1 = threading.Thread(target=self.recieveMessage,)
        t1.start()

    def recieveMessage(self):
        message = self.serverSocket.recv(1024).decode('ascii')
        print(message)
        if message == "quit":
            self.closeSocket()

    def sendMessage(self, message):
        self.serverSocket.send(message.encode('ascii'))
        if message == "quit":
            self.closeSocket()
            #t1.join()

    def closeSocket(self):
        self.serverSocket.close()

    def doWorkTest(self):
        numbers = [1, 2, 3, 4, 5]
        for n in numbers:
            print("Node " + self.ip + " doing work, step " + str(n))
        
        print("Work is done!")