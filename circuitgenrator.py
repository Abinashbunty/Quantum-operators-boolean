from qiskit import QuantumProgram
Q_obj = QuantumProgram() #Quantum object created
backend = 'local_qasm_simulator' #Backend is chosen

def no_of_qubits():
    m = int(input("Enter the number of qubits involved: "))
    return m

def qubit_declaration(m):
    qr = Q_obj.create_quantum_register("qr", m)
    cr = Q_obj.create_classical_register("cr", m)
    qc = Q_obj.create_circuit(None, [qr], [cr])

def file_name_input():
    filename = input("Enter name of the file: ")
    return filename

def create_file_object():
    access_mode = input("Enter file mode")
    Q_obj = open(file_name_input(), access_mode)
    return Q_obj


def quantum_circuit_extractor(file_object):
    #row1 = file_object.readline().rstrip()
    #row1_qubits = row1.split("-")
    #row2 = file_object.readline().rstrip()
    #row2_qubits = row2.split("-")

    # for i in range(pow(2, m)):
    #     row[i] = file_object.readline().rstrip()
    #     row_qubits[i] = row[i].split("-")
    #
    #     if(m==1):
    #         if (((row1_qubits[0] == 0) and (row1_qubits[1] == 1)) and (
    #                 (row2_qubits[0] == '1') and row2_qubits[1] == '0')):
    #             qc.x[0]
    #
    #     elif(m==4):
    #         if(row_qubits[i][0].count("1")%2==0):
    #             if(row_qubits[i][1]==1):
    #                 qc.cx(qc.cx(qr[0], qr[1]), qc.cx(qr[2], qr[3]))



    return Q_obj