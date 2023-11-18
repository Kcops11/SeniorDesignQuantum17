from node import nodeComputer
import random
import time

nodes = []

for i in range(1000):
    host = '127.0.0.1'
    ip = '127.' + '.'.join(str(random.randint(1, 9)) for _ in range(3))
    node = nodeComputer(host, 5001, ip)
    print("Node " + node.ip + " created")
    nodes.append(node)



for n in nodes:
    n.connect()
    print("Node", n.ip, "connected")
    data = n.doWork()
    n.sendMessage(data)
    print("Node", n.ip, "on standby")
    n.sendMessage("quit")
    print("Node", n.ip, "disconnected")

time.sleep(1)