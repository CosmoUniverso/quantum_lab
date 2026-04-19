import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.transformers import ActiveSpaceTransformer
from qiskit_nature.second_q.mappers import JordanWignerMapper
from qiskit_aer import AerSimulator
from qiskit import transpile, QuantumCircuit

print("--- ANALISI LEGA: INTERAZIONE FERRO-CARBONIO (ACCIAIO) ---")

# Simuliamo un atomo di Ferro e uno di Carbonio a distanza di legame tipica
driver = PySCFDriver(
    atom="Fe 0 0 0; C 0 0 1.8", 
    basis="sto3g"
)
problem = driver.run()

# Selezioniamo gli elettroni di valenza (quelli che decidono la durezza dell'acciaio)
# 6 elettroni in 6 orbitali = 12 qubit. Sicuro per la 3060.
transformer = ActiveSpaceTransformer(num_electrons=6, num_spatial_orbitals=6)
reduced_problem = transformer.transform(problem)

mapper = JordanWignerMapper()
qubit_op = mapper.map(reduced_problem.hamiltonian.second_q_op())

print(f"Qubit per la lega: {qubit_op.num_qubits}")

backend = AerSimulator(method="statevector", device="GPU", cuStateVec_enable=True)

qc = QuantumCircuit(qubit_op.num_qubits)
qc.h(range(qubit_op.num_qubits)) 
qc.save_statevector()

print("La GPU sta calcolando l'energia di legame Fe-C...")
t_qc = transpile(qc, backend)
job = backend.run(t_qc)
energy = job.result().get_statevector().expectation_value(qubit_op).real

total_energy = energy + reduced_problem.nuclear_repulsion_energy

print("\n-----------------------------------")
print(f"Risultato Energia Lega: {total_energy:.6f} Hartree")
print("Se questo valore è più basso del Ferro puro, la lega è stabile.")
print("-----------------------------------")
