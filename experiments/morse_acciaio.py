import sys
import os
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.transformers import ActiveSpaceTransformer
from qiskit_nature.second_q.mappers import JordanWignerMapper
from qiskit_aer import AerSimulator
from qiskit import transpile, QuantumCircuit

def get_steel_energy(distance):
    driver = PySCFDriver(atom=f"Fe 0 0 0; C 0 0 {distance}", basis="sto3g")
    problem = driver.run()
    
    # Riduzione per la GPU (6 elettroni in 6 orbitali)
    transformer = ActiveSpaceTransformer(num_electrons=6, num_spatial_orbitals=6)
    reduced_problem = transformer.transform(problem)
    
    mapper = JordanWignerMapper()
    qubit_op = mapper.map(reduced_problem.hamiltonian.second_q_op())
    
    backend = AerSimulator(method="statevector", device="GPU")
    qc = QuantumCircuit(qubit_op.num_qubits)
    qc.h(range(qubit_op.num_qubits)) 
    qc.save_statevector()
    
    t_qc = transpile(qc, backend)
    result = backend.run(t_qc).result()
    
    electronic_energy = result.get_statevector().expectation_value(qubit_op).real
    return electronic_energy + reduced_problem.nuclear_repulsion_energy

# Scansione distanze tipiche del legame Fe-C (da 1.0 a 3.0 Angstrom)
distances = np.linspace(1.2, 2.8, 10)
print("--- SCANSIONE ENERGETICA ACCIAIO (Fe-C) ---")
print("Distanza (Angstrom) | Energia (Hartree)")
print("---------------------------------------")

for d in distances:
    try:
        e = get_steel_energy(d)
        print(f"{d:.2f} \t\t| {e:.6f}")
    except Exception as e_msg:
        print(f"{d:.2f} \t\t| Errore: {e_msg}")
