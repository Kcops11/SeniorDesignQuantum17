import socket
import threading
import histogram
import time

class Router:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.messages = []  # List to store messages from nodes

    def bind(self):
        self.serverSocket.bind((self.host, self.port))
        self.serverSocket.listen(1000)  # Listen for connections

    def run(self):
        print('Router is waiting for connections...')
        while True:
            clientSocket, addr = self.serverSocket.accept()
            print(f'Got a connection from {addr[1]}')
            threading.Thread(target=self.handle_client, args=(clientSocket,)).start()

    def handle_client(self, clientSocket):
        while True:
            try:
                message = clientSocket.recv(1024).decode('ascii')
                if not message:
                    break
                if message == "quit":
                    # Optionally, send acknowledgment to client before breaking
                    break
                if message =='finalQuit':
                    histogram.makeHistogramArray(self.messages)
                    #print("I am quitting")
                    break
                else:
                    self.messages.append(message)  # Storing the message
                    # use the below statement if you want to see the array
                    # # warning, large amounts of data
                    # print(f"current message array: {self.messages}")  
            except ConnectionResetError:
                print("Connection reset by peer")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                break
        clientSocket.close()

    def close_socket(self):
        #histogram.makeHistogramArray(self.messages)
        self.serverSocket.close()

    def get_messages(self):
        return self.messages
