from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit,execute, Aer, IBMQ
from numpy import pi
from qiskit.quantum_info import Statevector, random_statevector
from qiskit.visualization import array_to_latex
from IPython.display import display, Math, Latex

def decode(qc, qubit, cr1, cr2):

    qc.z(qubit).c_if(cr1, 1) #if cr1 is 1 apply Z gate
    qc.x(qubit).c_if(cr2, 1) #if cr2 is 1 apply x gate, look at table above

qreg_q = QuantumRegister(9, 'q')
creg_c = ClassicalRegister(4, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)
circuit.h(qreg_q[1])
circuit.reset(qreg_q[3])
circuit.reset(qreg_q[4])
circuit.reset(qreg_q[5])
circuit.reset(qreg_q[6])
circuit.h(qreg_q[7])
circuit.h(qreg_q[8])
circuit.cx(qreg_q[1], qreg_q[2])
circuit.ry(pi / 2, qreg_q[3])
circuit.ry(pi / 2, qreg_q[5])
circuit.cx(qreg_q[3], qreg_q[4])
circuit.cx(qreg_q[5], qreg_q[6])
circuit.ry(pi / 2, qreg_q[4])
circuit.ry(pi / 2, qreg_q[6])
circuit.cx(qreg_q[4], qreg_q[3])
circuit.cx(qreg_q[6], qreg_q[5])
circuit.ry(pi / 2, qreg_q[3])
circuit.ry(pi / 2, qreg_q[5])
circuit.barrier(qreg_q[0], qreg_q[1], qreg_q[2], qreg_q[3], qreg_q[4], qreg_q[5], qreg_q[6])
circuit.cx(qreg_q[1], qreg_q[3])
circuit.cx(qreg_q[1], qreg_q[4])
circuit.cx(qreg_q[3], qreg_q[1])
circuit.cx(qreg_q[4], qreg_q[1])
circuit.barrier(qreg_q[0], qreg_q[1], qreg_q[2], qreg_q[3], qreg_q[4], qreg_q[5], qreg_q[6], qreg_q[7], qreg_q[8])
circuit.cx(qreg_q[2], qreg_q[5])
circuit.cx(qreg_q[2], qreg_q[6])
circuit.cx(qreg_q[5], qreg_q[2])
circuit.cx(qreg_q[6], qreg_q[2])
circuit.barrier(qreg_q[0], qreg_q[1], qreg_q[2], qreg_q[3], qreg_q[4], qreg_q[5], qreg_q[6], qreg_q[7], qreg_q[8])
circuit.cx(qreg_q[1], qreg_q[3])
circuit.cx(qreg_q[2], qreg_q[5])
circuit.ccx(qreg_q[3], qreg_q[7], qreg_q[1])
circuit.ccx(qreg_q[5], qreg_q[8], qreg_q[2])
circuit.cx(qreg_q[2], qreg_q[5])
circuit.cx(qreg_q[1], qreg_q[3])
circuit.barrier(qreg_q[0], qreg_q[1], qreg_q[2], qreg_q[3], qreg_q[4], qreg_q[5], qreg_q[6], qreg_q[7], qreg_q[8])
circuit.measure(qreg_q[7], creg_c[0])
circuit.measure(qreg_q[8], creg_c[1])
circuit.barrier(qreg_q[0], qreg_q[1], qreg_q[2], qreg_q[3], qreg_q[4], qreg_q[5], qreg_q[6], qreg_q[7], qreg_q[8])
circuit.cx(qreg_q[0], qreg_q[1])
circuit.h(qreg_q[0])
circuit.measure(qreg_q[0], creg_c[2])
circuit.measure(qreg_q[1], creg_c[3])
decode(circuit, 2, 2, 3)

print(circuit)
