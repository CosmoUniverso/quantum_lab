import sys
import os
import time
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from qiskit import transpile, QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.units import DistanceUnit
from qiskit_nature.second_q.mappers import JordanWignerMapper

print("--- SIMULAZIONE STRUTTURA: CLUSTER DIAMANTE (C2) ---")

# 1. Setup Cella Unitaria Diamante (2 atomi di Carbonio)
# Il carbonio ha molti piu' orbitali del N2 o H2
driver = PySCFDriver(
    atom="C 0 0 0; C 1.54 1.54 1.54", # Geometria semplificata diamante
    basis="sto3g",
    unit=DistanceUnit.ANGSTROM
)
problem = driver.run()
mapper = JordanWignerMapper()
qubit_op = mapper.map(problem.hamiltonian.second_q_op())

n_qubits = qubit_op.num_qubits
print(f"Struttura mappata. Qubit necessari: {n_qubits}")

# 2. Setup QPU (RTX 3060)
# A 28+ qubit la memoria video (12GB) e' al limite critico
backend = AerSimulator(
    method="statevector",
    device="GPU",
    cuStateVec_enable=True
)

# 3. Creazione Circuito di Test per Stato Solido
qc = QuantumCircuit(n_qubits)
qc.h(range(n_qubits)) # Sovrapposizione totale
for i in range(0, n_qubits - 1, 2):
    qc.cx(i, i+1)
qc.save_statevector()

print(f"Compilazione in corso per {n_qubits} qubit...")
t_qc = transpile(qc, backend)

print("Lancio su GPU... Monitora la VRAM (nvidia-smi)!")
start = time.time()

try:
    job = backend.run(t_qc)
    result = job.result()
    statevector = result.get_statevector()
    
    # Calcolo valore di aspettativa (energia della struttura)
    energy = statevector.expectation_value(qubit_op)
    
    print("\n-----------------------------------")
    print(f"ANALISI STRUTTURA COMPLETATA")
    print(f"Tempo GPU: {time.time() - start:.4f} s")
    print(f"Energia del Cluster: {energy.real:.6f} Hartree")
    print(f"Memoria stimata occupata: ~{ (2**n_qubits * 16) / 1024**2 :.2f} MB")
    print("-----------------------------------")

except Exception as e:
    print(f"CRASH: La struttura e' troppo complessa per la 3060: {e}")
