import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, BasicAer, IBMQ
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from qiskit import *
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram
from qiskit.extensions import Initialize
def random_state(nqubits):
    """Creates a random nqubit state vector"""
    from numpy import append, array, sqrt
    from numpy.random import random
    real_parts = array([])
    im_parts = array([])
    for amplitude in range(2**nqubits):
        real_parts = append(real_parts, (random()*2)-1)
        im_parts = append(im_parts, (random()*2)-1)
    # Combine into list of complex numbers:
    amps = real_parts + 1j*im_parts
    # Normalise
    magnitude_squared = 0
    for a in amps:
        magnitude_squared += abs(a)**2
    amps /= sqrt(magnitude_squared)
    return amps
# specify a random state

psi = random_state(1)

# Create a quantum circuit with 3 qubits
qc = QuantumCircuit(3, 2)
qc2 = QuantumCircuit(3, 1)
# Initialize the state to be teleported
init_gate = Initialize(psi)
qc.append(init_gate, [0])

# Prepare an entangled Bell pair between Alice and Bob
qc.h(1)
qc.cx(1, 2)

# Entangle the state to be teleported with Alice's qubit
qc.cx(0, 1)
qc.h(0)

# Measurement on Alice's qubits
qc.barrier()
qc.measure([0, 1], [0, 1])

# Print the circuit and execute to obtain Alice's measurement result
print("Measurement outcomes for Alice's qubits:")
print(qc)

simulator = BasicAer.get_backend('statevector_simulator')
job = execute(qc, simulator, shots=1)
result = job.result()
print(result.get_statevector())
statevector = result.get_statevector()
alice_measurement_result = list(result.get_counts(qc).keys())[0]

# Display Alice's measurement result and wait for user input
print("Alice's measured information:", alice_measurement_result)
input("Press Enter to continue and apply corrections to Bob's qubit")

qc2.initialize(statevector, range(3))
# Apply corrections to Bob's qubit based on Alice's measurement result
if alice_measurement_result[0] == '1':
    qc2.x(2)
if alice_measurement_result[1] == '1':
    qc2.z(2)

# Print the complete circuit
print("Complete Quantum Circuit:")
inverse_init_gate = init_gate.gates_to_uncompute()
qc2.append(inverse_init_gate, [2])
print(qc2)

# Measure Bob's qubit
qc2.measure(2, 0)

# Simulate the circuit
job = execute(qc2, simulator, shots=1)
result = job.result()
counts = result.get_counts(qc2)
print("Measurement outcomes for Bob's qubit:")
print(counts)