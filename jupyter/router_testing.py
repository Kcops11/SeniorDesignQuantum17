# Main file for testing router.py

from router import Router
from clustercomputer import QuantumClusterComputer

r = Router('', 5001)

r.start
r.handle_connection()
r.broadcast()