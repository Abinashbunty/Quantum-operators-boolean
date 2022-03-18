from qiskit import  QuantumProgram

Q_program = QuantumProgram()
backend = 'local_qasm_simulator'

qr = Q_program.create_quantum_register("qr", 3)
cr = Q_program.create_classical_register("cr", 3)
qc = Q_program.create_circuit("half_adder", [qr], [cr])

# Not gate on qubit 0
qc.x(qr[0])

# Not gate on qubit 1
qc.x(qr[1])

# Toffoli gate from qubit 0,1 to qubit 2
qc.ccx(qr[0], qr[1], qr[2])

# CNOT (Controlled-NOT) gate from qubit 0 to qubit 1
qc.cx(qr[0], qr[1])

# measure gate from qr to cr
qc.measure(qr, cr)

result = Q_program.execute(name_of_circuits="half_adder", backend=backend, shots=1024, seed=1)
print(result)
print(result.get_data("half_adder"))
