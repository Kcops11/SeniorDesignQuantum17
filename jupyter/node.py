import qiskit  # Ensure you have Qiskit installed
import socket
import threading
import time
'''
USAGE - this sends a user input to the connected router



node = nodeComputer('127.0.0.1', 5001)
node.connect()
while(True):
    msg = input("Input message>> ")
    node.connect()
    node.sendMessage(msg)



'''
class nodeComputer:
    def __init__(self, router_host, router_port, ip):
        # init a  bunch of vars - done automatically 
        self.router_host = router_host
        self.router_port = router_port
        self.ip = ip
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        #connects self to router - router should be started first. 
        self.serverSocket = socket.socket()
        self.serverSocket.connect((self.router_host, self.router_port))
        
        t1 = threading.Thread(target=self.recieveMessage,)
        t1.start()

    def recieveMessage(self):
        # waits to recieve message - should be placed in a while loop
        message = self.serverSocket.recv(1024).decode('ascii')
        print(message)
        if message == "quit":
            self.closeSocket()

    def sendMessage(self, message):
        # sends message to router 
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