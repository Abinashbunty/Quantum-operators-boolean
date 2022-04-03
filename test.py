from qiskit import QuantumProgram, CompositeGate, QuantumRegister

qubit = input("Enter qubit value")
Q_obj = QuantumProgram()
backend = 'local_qasm_simulator'

qr = Q_obj.create_quantum_register("qr", 3)
cr = Q_obj.create_classical_register("cr", 3)
qc = Q_obj.create_circuit("Circuit", [qr], [cr])

c = -1 # Counter to check iteration number
for ch in qubit:
    c = c + 1
    if(ch=='1'):
        qc.x(c)

    #   The above statement is used for flipping the bits.
    #   If the user wants 1100 as the qubits to be entered,
    #   He can flip the 1st 2 bits by using NOT gate
