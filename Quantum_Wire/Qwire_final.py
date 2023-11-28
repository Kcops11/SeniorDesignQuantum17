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

def Entanglement_verification(simulator, Bell_state, debug = False):
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

def random_state(nqubits):
    """Creates a random nqubit state vector"""
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

def information_initialize_to_statevector(init_gate, simulator,debug = False):
    """Transform Initilize object to Statevector"""
    #quantum circuit for getting statevector from initialize objects.
    qc_init = QuantumCircuit(1,global_phase=0)
    qc_init.append(init_gate, [0])
    job_init = execute(qc_init, simulator, shots=1)
    result_init = job_init.result()
    init_statevector = result_init.get_statevector()
    if debug == True:
        print("--------------------------------------------------------")
        print("initial random state\n")
        print(qc_init)
        print(init_statevector.data)
        print("--------------------------------------------------------")
    return init_statevector

def compound_information_zero_states(init_statevector, debug = False):
    """Create compound qubit system using tensor product"""
    statevector_bell = Statevector.from_label('00')
    # Combine the individual statevectors using tensor product
    # Remember that in qiskit we use little endian for qubit. Different with quantum circuit.
    compound_statevector = statevector_bell.tensor(init_statevector)
    if debug == True:
        print("--------------------------------------------------------")
        print("tensor product result\n")
        print(compound_statevector.data)
        print("--------------------------------------------------------")
    return compound_statevector

def Alice_quantum_operation(compound_statevector, simulator, debug = False):
    """Do quantum operation from alice's side"""
    #Set circuit
    qc_Alice_qo = QuantumCircuit(3, 2,global_phase=0)
    qc_Alice_qo.initialize(compound_statevector,[0,1,2])
    # Create Bell_state
    qc_Alice_qo.h(1)
    qc_Alice_qo.cx(1, 2)
    qc_Alice_qo.barrier()
    # Entangle the state to be teleported with Alice's qubit
    qc_Alice_qo.cx(0, 1)
    qc_Alice_qo.h(0)
    job_compound = execute(qc_Alice_qo, simulator, shots=1)
    result_compound = job_compound.result()
    Bell_info_statevector = result_compound.get_statevector()
    if debug == True:
        print("--------------------------------------------------------")
        print("Quantum Circuit _ statevector\n")
        print(qc_Alice_qo)
        print(Bell_info_statevector.data)
        print("--------------------------------------------------------")
    return Bell_info_statevector


def Alice_measure(Bell_info_statevector, simulator, debug = False):
    """Measure quantum information from Alice"""
    #Set circuit
    qc_Alice_measure = QuantumCircuit(3,2,global_phase=0)
    qc_Alice_measure.initialize(Bell_info_statevector,[0,1,2])
    qc_Alice_measure.measure([0, 1], [0, 1])
    job_alice = execute(qc_Alice_measure, simulator, shots=1)
    result_alice = job_alice.result()
    alice_statevector = result_alice.get_statevector()
    alice_measurement_result = list(result_alice.get_counts(qc_Alice_measure).keys())[0]
    if debug == True:
        print("--------------------------------------------------------")
        print("Quantum Circuit _ statevector _ measurement result\n")
        print(qc_Alice_measure)
        print(alice_statevector)
        print(alice_measurement_result)
        print("--------------------------------------------------------")
    return alice_measurement_result , alice_statevector

def Bob_quantum_opertaion(alice_measurement_result, Alice_statevector, simulator, debug = False):
    """Do quantum operation from Bob's side"""
    #Set circuit
    qc_Bob_qo = QuantumCircuit(3, 1,global_phase=0)
    qc_Bob_qo.initialize(Alice_statevector, [0,1,2])
    # Apply corrections to Bob's qubit based on Alice's measurement result
    if alice_measurement_result[0] == '1':
        qc_Bob_qo.x(2)
    if alice_measurement_result[1] == '1':
        qc_Bob_qo.z(2)
    job_bob = execute(qc_Bob_qo, simulator, shots=1)
    result_bob = job_bob.result()
    bob_statevector = result_bob.get_statevector()
    if debug == True:
        print("--------------------------------------------------------")
        print("Quantum Circuit _ statevector\n")
        print(qc_Bob_qo)
        print(bob_statevector)
        print("--------------------------------------------------------")
    return bob_statevector

def Bob_measure(Bob_statevector, inverse_init_gate ,simulator, debug = False):
    """Measure from Bob's side"""
    qc_Bob_measure = QuantumCircuit(3,1,global_phase = 0)
    qc_Bob_measure.initialize(Bob_statevector, [0,1,2])
    qc_Bob_measure.append(inverse_init_gate, [2])
    qc_Bob_measure.measure(2,0)
    job_bob = execute(qc_Bob_measure, simulator, shots=1)
    result_bob = job_bob.result()
    counts = result_bob.get_counts(qc_Bob_measure)
    bob_measurement_result = list(result_bob.get_counts(qc_Bob_measure).keys())[0]
    if debug == True:
        print("--------------------------------------------------------")
        print("Quantum Circuit _ measurement result\n")
        print(qc_Bob_measure)
        print(bob_measurement_result)
        print("--------------------------------------------------------")
        
    return bob_measurement_result



'''How we can use?
    1. Classical channel Setup
    2. Do Step0, Step1, and Step2
    3. Send alice's measured information to router
    4. Router send back "received data. keep proceed."
    5. Do Step3, Step4, Step5
    6. Send bob's measured information to router
    7. Router send back "recieved data. kill this network."
    -> router will get 3 information bits which will be used for histogram.
'''

def Entanglement_verification_debug():
    simulator = Aer.get_backend('statevector_simulator')
    Bell_state = gen_Bell(simulator, False)

    verification = Entanglement_verification(simulator, Bell_state, True)
    print(verification)


def quantum_function_step_one():
    #Step 0. We set simulator as "statevector_simulator"
    simulator = Aer.get_backend('statevector_simulator')

    #Step 1. initialize random qubit (it is our information)
    psi = random_state(1)
    init_gate = Initialize(psi)
    inverse_init_gate = init_gate.gates_to_uncompute()
    init_statevector = information_initialize_to_statevector(init_gate, simulator, False)
    compound_statevector = compound_information_zero_states(init_statevector, False)
    return simulator,inverse_init_gate, compound_statevector

def quantum_function_step_two(simulator,compound_statevector):
    #Step 2. Proceed Alice's quantum operation (not measuring)
    Bell_info_statevector = Alice_quantum_operation(compound_statevector,simulator,False)
    return Bell_info_statevector

def quantum_function_step_three(simulator, Bell_info_statevector):
    #Step 3. Alice Meausre her qubit.
    #Measured outcome also inverted.(little endian) 1st : information, 2nd : Alice's Bell states
    Alice_measurement_result , Alice_statevector = Alice_measure(Bell_info_statevector, simulator, False)
    return Alice_measurement_result, Alice_statevector

def quantum_function_step_four(simulator,Alice_measurement_result, Alice_statevector):
    #Step 4. Bob's quantum operation (not measureing)
    Bob_statevector = Bob_quantum_opertaion(Alice_measurement_result, Alice_statevector, simulator, False)
    return Bob_statevector

def quantum_function_step_five(simulator,Bob_statevector, inverse_init_gate):
    #Step 5. Bob Meausre his qubit.
    Bob_measurement_result = Bob_measure(Bob_statevector, inverse_init_gate, simulator, False)

    return(Bob_measurement_result)

    # data1[0] = simulator
    # data1[1] = inverse_init_gate
    # data1[2] = compound_statevector
    # data2[0] = Bell_info_statevector
    # data3[0] = Alice_measurement_result
    # data3[1] = Alice_statevector
    # data4[0] = Bob_statevector
    # data5[0] = Bob_measurement_result


