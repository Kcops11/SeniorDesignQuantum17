from qiskit import QuantumCircuit, execute, Aer, transpile, QuantumRegister, ClassicalRegister
from qiskit.visualization import plot_histogram, plot_bloch_multivector, plot_bloch_vector
from qiskit.quantum_info import Statevector, random_statevector, partial_trace
from qiskit.quantum_info.operators import Operator
from qiskit.circuit.library.standard_gates import XGate, ZGate
import sys
import numpy as np

information = random_statevector(2)
print("information is :")
print(information)

def Bell_gen():
    Bell_1 = Statevector.from_label('0')
    Bell_2 = Statevector.from_label('0')
    composite1 = Bell_1.tensor(Bell_2)
    composite2 = information.tensor(composite1)
    Bell_gen = QuantumCircuit(3)
    Bell_gen.initialize(Statevector(composite2),[0,1,2])
    Bell_gen.h(1)
    Bell_gen.cx(1,2)
    simulator = Aer.get_backend('statevector_simulator')
    job = execute(Bell_gen, simulator)
    result = job.result()
    statevector = result.get_statevector()
    print(statevector)
    return statevector

def Teleportation(Bell_pair):
    Teleportation = QuantumCircuit(3)
    Teleportation.initialize(Statevector(Bell_pair),[0,1,2])
    Teleportation.cx(0,1)
    Teleportation.h(0)
    simulator = Aer.get_backend('statevector_simulator')
    job = execute(Teleportation,simulator)
    result = job.result()
    statevector = result.get_statevector()
    return statevector

#Chat GPT part
def Teleportation_measure(Teleported):
    # Create a quantum circuit with 3 qubits
    qreg = QuantumRegister(3)
    creg = ClassicalRegister(2)
    circuit = QuantumCircuit(qreg, creg)

    # Apply the gates and operations as part of the quantum teleportation protocol
    circuit.initialize(Statevector(Teleported), [0,1,2])
    print(circuit)
    # Measure the first 2 qubits
    circuit.measure(qreg[0], creg[0])
    circuit.measure(qreg[1], creg[1])

    # Initialize unmeasured_qubit_sv with |0⟩ state
    unmeasured_qubit_sv = Statevector.from_label('0')

    # Simulate the circuit on the QASM simulator
    simulator = Aer.get_backend('qasm_simulator')
    job = execute(circuit, simulator, shots=1)
    result = job.result()
    counts = result.get_counts()

    # Extract the measured values for the first 2 qubits
    measured_values = next(iter(counts))

    # Define a composite statevector based on the measured outcomes
    composite_sv = Statevector.from_label(measured_values)

    # Apply conditional Z gate if the first qubit was measured as '1'
    if measured_values[0] == '1':
        cz = Operator(ZGate())
        unmeasured_qubit_sv = unmeasured_qubit_sv.evolve(cz)

    # Apply conditional X gate if the second qubit was measured as '1'
    if measured_values[1] == '1':
        cx = Operator(XGate())
        unmeasured_qubit_sv = unmeasured_qubit_sv.evolve(cx)

    # Print the state of the unmeasured qubit
    print(unmeasured_qubit_sv)

def identity(Teleported_receive):
    identity = QuantumCircuit(3)
    identity.initialize(Statevector(Teleported_receive),[0,1,2])
    simulator = Aer.get_backend('statevector_simulator')
    job = execute(identity,simulator)
    result = job.result()
    statevector = result.get_statevector()
    print(statevector)
    return statevector

def xcircuit(Teleported_receive):
    xcircuit = QuantumCircuit(3)
    xcircuit.initialize(Statevector(Teleported_receive),[0,1,2])
    xcircuit.x(2)
    simulator = Aer.get_backend('statevector_simulator')
    job = execute(xcircuit,simulator)
    result = job.result()
    statevector = result.get_statevector()
    print(statevector)
    return statevector

def zcircuit(Teleported_receive):
    zcircuit = QuantumCircuit(3)
    zcircuit.initialize(Statevector(Teleported_receive),[0,1,2])
    zcircuit.z(2)
    simulator = Aer.get_backend('statevector_simulator')
    job = execute(zcircuit,simulator)
    result = job.result()
    statevector = result.get_statevector()
    print(statevector)
    return statevector

def zxcircuit(Teleported_receive):
    zxcircuit = QuantumCircuit(3)
    zxcircuit.initialize(Statevector(Teleported_receive),[0,1,2])
    zxcircuit.z(2)
    zxcircuit.x(2)
    simulator = Aer.get_backend('statevector_simulator')
    job = execute(zxcircuit,simulator)
    result = job.result()
    statevector = result.get_statevector()
    print(statevector)
    return statevector


while True:
    sysinput = sys.stdin.read(1)
    if sysinput == "i":
        Bell_pair = Bell_gen()
        initialization = True
    if sysinput == "t" and initialization == True:
        Teleported = Teleportation(Bell_pair)
        print("Qubit Teleported")
        print(Teleported)
    if sysinput == "m" and initialization == True:
        measured_value = Teleportation_measure(Teleported)
        # if measured_value == '00':
        #     print("identity applied")
        #     identity(Teleported)
        # if measured_value == '01':
        #     print("x applied")
        #     xcircuit(Teleported)
        # if measured_value == '10i':
        #     print("z applied")
        #     zcircuit(Teleported)
        # if measured_value == '11':
        #     print("zx applied")
        #     zxcircuit(Teleported)
        

    