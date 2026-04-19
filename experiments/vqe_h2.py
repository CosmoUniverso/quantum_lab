import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.units import DistanceUnit
from qiskit_nature.second_q.mappers import JordanWignerMapper
from qiskit_nature.second_q.circuit.library import UCCSD, HartreeFock
from qiskit_algorithms import VQE
from qiskit_algorithms.optimizers import SLSQP
from qiskit.primitives import StatevectorEstimator # Estimator di base, solo CPU

# 1. Setup Molecola
driver = PySCFDriver(atom="H 0 0 0; H 0 0 0.735", basis="sto3g", unit=DistanceUnit.ANGSTROM)
problem = driver.run()
mapper = JordanWignerMapper()
qubit_op = mapper.map(problem.hamiltonian.second_q_op())

# 2. Setup Ansatz
init_state = HartreeFock(problem.num_spatial_orbitals, problem.num_particles, mapper)
ansatz = UCCSD(problem.num_spatial_orbitals, problem.num_particles, mapper, initial_state=init_state)

# 3. Setup QPU (Reference CPU per isolare il bug)
estimator = StatevectorEstimator()

# 4. Esecuzione VQE
optimizer = SLSQP(maxiter=50)
vqe = VQE(estimator, ansatz, optimizer)

print("Lancio VQE diagnostico (CPU Reference)...")
try:
    result = vqe.compute_minimum_eigenvalue(qubit_op)
    
    nuclear_repulsion = problem.nuclear_repulsion_energy
    total_energy = result.eigenvalue.real + nuclear_repulsion

    print("\n-----------------------------------")
    print("      DIAGNOSTICA SUPERATA")
    print("-----------------------------------")
    print(f"Energia Elettronica: {result.eigenvalue.real:.6f}")
    print(f"Repulsione Nucleare: {nuclear_repulsion:.6f}")
    print(f"ENERGIA TOTALE:      {total_energy:.6f} Hartree")
    print(f"Target Teorico:      -1.137306 Hartree")
    print("-----------------------------------")
except Exception as e:
    print(f"Errore Critico: {e}")
