# Main file for testing cluster computer

from router import Router
from node import nodeComputer

node = nodeComputer('127.0.0.1', 5001)


print("A")
node.connect()
print("B")

while(True):
    msg = input("Input message>> ")
    node.sendMessage(msg)
print("C")


print("Node Done")