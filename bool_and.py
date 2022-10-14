from qiskit import QuantumProgram,  ClassicalRegister, QuantumRegister
#from qiskit import available_backends, execute

q = QuantumRegister(2)
c = ClassicalRegister(2)
qc = QuantumCircuit(q, c)

qc.h(q[0])

qc.cx(q[0], q[1])
qc.measure(q, c)
print("Local backends: ", Available_backends({'local': True}))

# Compile and run the Quantum circuit on a simulator backend
job_sim = execute(qc, "local_qasm_simulator")
sim_result = job_sim.result()

print("simulation: ", sim_result)
print(sim_result.get_counts(qc))