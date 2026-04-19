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

print("--- TEST N2: ACCESSO DIRETTO CUDA ---")

# 1. Setup Molecola
driver = PySCFDriver(atom="N 0 0 0; N 0 0 1.098", basis="sto3g", unit=DistanceUnit.ANGSTROM)
problem = driver.run()
mapper = JordanWignerMapper()
qubit_op = mapper.map(problem.hamiltonian.second_q_op())

# 2. Creiamo un circuito manuale da 20 qubit per forzare la GPU
qc = QuantumCircuit(20)
qc.h(range(20)) # Mettiamo tutto in sovrapposizione
qc.save_statevector() # Istruzione specifica per simulatori

# 3. Setup Backend Diretto
backend = AerSimulator(
    method="statevector",
    device="GPU",
    cuStateVec_enable=True
)

print("Compilazione e invio forzato alla GPU...")
t_qc = transpile(qc, backend)

start = time.time()
try:
    # Eseguiamo il calcolo del vettore di stato puro
    job = backend.run(t_qc)
    result = job.result()
    statevector = result.get_statevector()
    
    # Calcoliamo l'energia "a mano" (Expectation Value)
    # Questo e' quello che fa il VQE internamente
    energy = statevector.expectation_value(qubit_op)
    
    print("\n-----------------------------------")
    print(f"SUCCESSO DIRETTO SU GPU")
    print(f"Tempo di calcolo: {time.time() - start:.4f} s")
    print(f"Energia Elettronica: {energy.real:.6f}")
    print(f"Energia Totale: {energy.real + problem.nuclear_repulsion_energy:.6f}")
    print("-----------------------------------")
    
except Exception as e:
    print(f"Fallimento totale: {e}")
