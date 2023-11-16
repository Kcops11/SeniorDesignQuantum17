import socket
import threading
'''
USE ORDER
1 make object
2 bind()
3 run ()
4 recieve() 
5 close()

'''
class Router:
    def __init__(self, host, port):
        # just sets a bunch of variables - done automatically 
        self.host = host
        self.port = port
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def bind(self):
        # binds self to port 
        self.serverSocket.bind((self.host, self.port))
        self.serverSocket.listen(1000)
             
    def run(self):
        # waits for a connection from the nodes. Should be placed in a while loop 
        print ('Waiting for a connection')
        self.serverSocket.listen(1000)
        (self.clientSocket, addr) = self.serverSocket.accept()
        print ('Got a connection from {}'.format(str(addr)))
        
        t1 = threading.Thread(target=self.recieveMessage,)
        t1.start()
        
            
    def sendMessage(self, message):
        # this sends a message to the node. To use, sendMessage("HELLOWORLD") will send "HELLOWORLD" to node
        self.clientSocket.send(message.encode('ascii'))

    def recieveMessage(self):
        # this waits for a messaged to be recieved from the node
        while(1):
            (self.clientSocket, addr) = self.serverSocket.accept()
            message = self.clientSocket.recv(1024).decode('ascii')
            print(message)
            
            if message == "quit":
                self.closeSocket()
                t1.join()

    def closeSocket(self):
        # closes port - if you dont do this then it pretty much just runs constantly and is hard to close 
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