import socket
import threading

class Router:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def bind(self):
        self.serverSocket.bind((self.host, self.port))
        self.serverSocket.listen(5)
             
    def run(self):
        print ('Waiting for a connection')
        self.serverSocket.listen(5)
        (self.clientSocket, addr) = self.serverSocket.accept()
        print ('Got a connection from {}'.format(str(addr)))
        while True:
            self.recieveMessage()
            
    def sendMessage(self, message):
        # not working - need to set client to listen
        self.clientSocket.send(message.encode('ascii'))

    def recieveMessage(self):
        (self.clientSocket, addr) = self.serverSocket.accept()
        message = self.clientSocket.recv(1024).decode('ascii')
        
        self.sendMessage("Recieved: " + message)
        print(message)

    def closeSocket(self):
        self.serverSocket.close()

#
'''
USE ORDER
1 make object
2 bind()
3 run ()
4 recieve() 
5 close()

'''