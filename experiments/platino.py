import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.transformers import ActiveSpaceTransformer
from qiskit_nature.second_q.mappers import JordanWignerMapper
from qiskit_aer import AerSimulator
from qiskit import transpile, QuantumCircuit

print("--- STRESS TEST EXTREME: 28 QUBIT SULLA RTX 3060 ---")

# Aumentiamo la risoluzione spaziale del Carbonio/Diamante
driver = PySCFDriver(atom="C 0 0 0; C 0 0 1.54", basis="6-31g")
problem = driver.run()

# TRUCCO: Impostiamo 14 orbitali spaziali. 
# In Jordan-Wigner, Qubit = 2 * orbitali_spaziali. 14 * 2 = 28 Qubit.
transformer = ActiveSpaceTransformer(num_electrons=4, num_spatial_orbitals=14)
reduced_problem = transformer.transform(problem)

mapper = JordanWignerMapper()
qubit_op = mapper.map(reduced_problem.hamiltonian.second_q_op())
n_qubits = qubit_op.num_qubits

print(f"Target Qubit: {n_qubits} (Memoria stimata: 4GB)")

backend = AerSimulator(
    method="statevector", 
    device="GPU", 
    cuStateVec_enable=True,
    blocking_enable=True, # Forza la GPU a gestire i blocchi di memoria
    blocking_qubits=20
)

# Creiamo un circuito con molti gate per non far finire il calcolo troppo in fretta
qc = QuantumCircuit(n_qubits)
for _ in range(5): # Ripetiamo lo strato di gate per dare lavoro
    qc.h(range(n_qubits))
    for i in range(n_qubits - 1):
        qc.cx(i, i+1)
qc.save_statevector()

print("Compilazione in corso (la CPU lavorera' molto qui)...")
t_qc = transpile(qc, backend)

print(f"LANCIO SU GPU: Ora guarda nvidia-smi!")
start = time.time()
try:
    job = backend.run(t_qc)
    result = job.result()
    print("-----------------------------------")
    print(f"TEMPO DI CALCOLO: {time.time() - start:.2f} secondi")
    print("CONTROLLA IL PICCO DI MEMORIA SU NVIDIA-SMI")
    print("-----------------------------------")
except Exception as e:
    print(f"Crash: {e}")
