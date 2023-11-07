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
    print("Node", n.router_host, "connected")
    n.doWorkTest()
    print("Node", n.router_host, "on standby")

