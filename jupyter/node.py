import qiskit  # Ensure you have Qiskit installed
import socket
import threading
import time
import sys
from pathlib import Path

# Get the absolute path to the Quantum_Wire directory
current_dir = Path(__file__).resolve().parent

print(current_dir)
quantum_wire_dir = current_dir.parent / 'Quantum_Wire'
print(quantum_wire_dir)

# Add the Quantum_Wire directory to sys.path
sys.path.append(str(quantum_wire_dir))

# Now you can import from Quantum_Wire or any subdirectories within it
from Qwire_final import quantum_function
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

    def doWork(self):
        quantum_function()