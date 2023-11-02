from router import Router



r = Router('127.0.0.1', 5001)
r.bind()
print("Router Open")
r.run()
print("Router Open")