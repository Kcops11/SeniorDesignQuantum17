from qiskit import QuantumCircuit, execute, Aer
from qiskit.visualization import plot_histogram
from qiskit.quantum_info import Statevector

# Create an initial quantum circuit
initial_circuit = QuantumCircuit(2)
initial_circuit.h(0)
initial_circuit.cx(0, 1)

# Simulate the initial circuit to get the statevector
simulator = Aer.get_backend('statevector_simulator')
job = execute(initial_circuit, simulator)
result = job.result()
statevector = result.get_statevector()

# Create a new quantum circuit
new_circuit = QuantumCircuit(2)

# Initialize the new circuit with the statevector
new_circuit.initialize(Statevector(statevector), [0, 1])

# You can continue building and running operations on the new circuit
new_circuit.x(0)
new_circuit.measure_all()

# Simulate the new circuit
simulator = Aer.get_backend('qasm_simulator')
job = execute(new_circuit, simulator, shots=1024)
result = job.result()
counts = result.get_counts()

# Print the measurement results
print(counts)
