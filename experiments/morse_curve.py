import sys
import os
import time
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.units import DistanceUnit
from qiskit_nature.second_q.mappers import JordanWignerMapper
from qiskit_aer import AerSimulator
from qiskit import transpile, QuantumCircuit

def calculate_energy(distance):
    # Setup molecola alla distanza specifica
    driver = PySCFDriver(
        atom=f"H 0 0 0; H 0 0 {distance}",
        basis="sto3g",
        unit=DistanceUnit.ANGSTROM
    )
    problem = driver.run()
    mapper = JordanWignerMapper()
    qubit_op = mapper.map(problem.hamiltonian.second_q_op())
    
    # Setup Circuito e Backend GPU
    n_qubits = qubit_op.num_qubits
    backend = AerSimulator(method="statevector", device="GPU")
    
    qc = QuantumCircuit(n_qubits)
    qc.h(range(n_qubits)) # Stato di prova
    qc.save_statevector()
    
    t_qc = transpile(qc, backend)
    job = backend.run(t_qc)
    statevector = job.result().get_statevector()
    
    # Energia = Energia Elettronica + Repulsione Nucleare
    electronic_energy = statevector.expectation_value(qubit_op).real
    total_energy = electronic_energy + problem.nuclear_repulsion_energy
    return total_energy

# Range di distanze da scansionare (da 0.3 a 2.5 Angstrom)
distances = np.linspace(0.3, 2.5, 15)
results = []

print("--- GENERAZIONE CURVA DI MORSE (RTX 3060) ---")
print("Distanza (A) | Energia (Hartree)")
print("--------------------------------")

for d in distances:
    try:
        energy = calculate_energy(d)
        results.append((d, energy))
        print(f"{d:.2f}         | {energy:.6f}")
    except Exception as e:
        print(f"{d:.2f}         | ERRORE: {e}")

print("--------------------------------")
print("Scansione completata.")
