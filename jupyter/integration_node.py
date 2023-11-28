from node import nodeComputer
import random
import time

nodes = []
global counter

for i in range(1000):
    host = '127.0.0.1'
    ip = '127.' + '.'.join(str(random.randint(1, 9)) for _ in range(3))
    node = nodeComputer(host, 5001, ip)
    print("Node " + node.ip + " created")
    nodes.append(node)

counter = 0

for n in nodes:
    counter = counter + 1
    n.connect()
    print("Node", n.ip, "connected")
    n.doWork()
    #print("Node", n.ip, "on standby")
    #print(counter)
    if(counter > 998):
        n.sendMessage("finalQuit")
    else:
        n.sendMessage("quit")
    print("Node", n.ip, "disconnected")


time.sleep(1)