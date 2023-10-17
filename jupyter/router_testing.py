# Main file for testing router.py
import time
'''
USE ORDER
1 make object
2 bind()
3 run ()
4 recieve() 
5 close()

'''
from router import Router
from node import nodeComputer

r = Router('127.0.0.1', 5001)

r.bind()
print("1")
r.run()
while(1):
    time.sleep(5)
    r.sendMessage("Hi")

print("Router Done")