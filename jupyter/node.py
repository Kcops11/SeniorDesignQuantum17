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
from Qwire_final import quantum_function_step_one,quantum_function_step_two,quantum_function_step_three,quantum_function_step_four,quantum_function_step_five



class nodeComputer:
    def __init__(self, router_host, router_port, ip):
        self.router_host = router_host
        self.router_port = router_port
        self.ip = ip
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True  # Flag to control the running of the thread

    def connect(self):
        self.serverSocket = socket.socket()
        self.serverSocket.connect((self.router_host, self.router_port))
        t1 = threading.Thread(target=self.receiveMessage)
        t1.start()

    def receiveMessage(self):
        while self.running:
            try:
                message = self.serverSocket.recv(1024).decode('ascii')
                if message:
                    print(message)
                if message == "quit":
                    break
            except Exception as e:
                print(f"Error receiving message: {e}")
                break
        self.closeSocket()

    def sendMessage(self, message):
        if isinstance(message, tuple):
            message_str = ','.join(map(str, message))
        else:
            message_str = str(message)
        self.serverSocket.send(message_str.encode('ascii'))
        if message_str == "quit":
            self.running = False

    def closeSocket(self):
        self.running = False
        self.serverSocket.close()


    def doWork(self):
        data1 = quantum_function_step_one ()
        data2 = quantum_function_step_two(data1[0], data1[2])
        data3 = quantum_function_step_three(data1[0],data2)
        self.sendMessage(data3[0])
        data4 = quantum_function_step_four(data1[0],data3[0], data3[1])
        data5 = quantum_function_step_five(data1[0],data4,data1[1])
        self.sendMessage(data5)