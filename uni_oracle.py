from qiskit import QuantumProgram
Q_obj = QuantumProgram() #Quantum object created
backend = 'local_qasm_simulator'

qr = Q_obj.create_quantum_register("qr", 1)
cr = Q_obj.create_classical_register("cr", 1)
qc = Q_obj.create_circuit("not", [qr], [cr])

filename = "input.txt"
file_object = open(filename, "r")

def quantum_circuit_extractor(file_object):
    row1 = file_object.readline().rstrip()
    row1_qubits = row1.split("-")
    row2 = file_object.readline().rstrip()
    row2_qubits = row2.split("-")

    if(((row1_qubits[0]=='0') and (row1_qubits[1]=='1')) and ((row2_qubits[0]=='1') and row2_qubits[1]=='0')):
        qc.x[0]

    return Q_obj