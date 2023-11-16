from node import nodeComputer
import random
import time

nodes = []
global num_nodes
for i in range(1000):
    host = '127.0.0.1'
    ip = '127.' + '.'.join(str(random.randint(1, 9)) for _ in range(3))
    node = nodeComputer(host, 5001, ip)
    print("Node " + node.ip + " created")
    nodes.append(node)

num_nodes = 0

for n in nodes:
    n.connect()
    print("Node", n.ip, "connected")
    n.doWork()
    print("Node", n.ip, "on standby")
    num_nodes += 1 
    print(f"Num nodes: {num_nodes}")
    time.sleep(10)

