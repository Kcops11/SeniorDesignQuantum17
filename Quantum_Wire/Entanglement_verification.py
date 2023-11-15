import numpy as np
from numpy import append, array, sqrt
from numpy.random import random
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, BasicAer, IBMQ
from qiskit import Aer
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from qiskit import *
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram
from qiskit.extensions import Initialize
from qiskit.quantum_info import Statevector, random_statevector

def gen_Bell(simulator, debug = False):
    statevector_bell = Statevector.from_label('00')
    qc_gen_Bell = QuantumCircuit(2,global_phase = 0)
    qc_gen_Bell.initialize(statevector_bell,[0,1])
    qc_gen_Bell.h(0)
    qc_gen_Bell.cx(0, 1)
    job_gen_Bell = execute(qc_gen_Bell, simulator, shots=1)
    result_gen_Bell = job_gen_Bell.result()
    Bell_statevector = result_gen_Bell.get_statevector()
    if debug == True:
        print("--------------------------------------------------------")
        print("Quantum Circuit _ statevector\n")
        print(qc_gen_Bell)
        print(Bell_statevector.data)
        print("--------------------------------------------------------")
    return Bell_statevector

def entanglement_verification(simulator, Bell_state, debug = False):
    #Make compound quantum states using Bell state twice and two zero quantum state.
    statevector_zeros = Statevector.from_label('00')
    tensor_bell_statevector = Bell_state.tensor(Bell_state)
    #print(tensor_bell_statevector)
    compound_statevector = statevector_zeros.tensor(tensor_bell_statevector)
    #print(compound_statevector.data)
    qc_CSWAP_verification = QuantumCircuit(6,2,global_phase=0)
    qc_CSWAP_verification.initialize(compound_statevector,[0,1,2,3,4,5])
    qc_CSWAP_verification.h(5)
    qc_CSWAP_verification.h(4)
    qc_CSWAP_verification.cx(0,2)
    qc_CSWAP_verification.cx(1,3)
    qc_CSWAP_verification.barrier()
    qc_CSWAP_verification.ccx(4,2,0)
    qc_CSWAP_verification.ccx(5,3,1)
    qc_CSWAP_verification.barrier()
    qc_CSWAP_verification.h(5)
    qc_CSWAP_verification.h(4)
    qc_CSWAP_verification.cx(0,2)
    qc_CSWAP_verification.cx(1,3)
    qc_CSWAP_verification.measure(4,0)
    qc_CSWAP_verification.measure(5,1)
    job_verification = execute(qc_CSWAP_verification, simulator, shots=10000)
    result_job_verification = job_verification.result().get_counts()
    if debug == True:
        print("--------------------------------------------------------")
        print("Quantum Circuit _ statevector\n")
        print(qc_CSWAP_verification)
        print(result_job_verification)
        print("--------------------------------------------------------")
    return result_job_verification



#Step 0. We set simulator as "statevector_simulator"
simulator = Aer.get_backend('statevector_simulator')

Bell_state = gen_Bell(simulator, False)

verification = entanglement_verification(simulator, Bell_state, False)
print(verification)


