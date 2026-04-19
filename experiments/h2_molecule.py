import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.qpu import VirtualQPU
from qiskit_nature.units import DistanceUnit
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import JordanWignerMapper

# 1. Definiamo la geometria della molecola di Idrogeno (H2)
# La distanza tipica di legame è circa 0.735 Angstrom
driver = PySCFDriver(
    atom="H 0 0 0; H 0 0 0.735",
    basis="sto3g",
    charge=0,
    spin=0,
    unit=DistanceUnit.ANGSTROM,
)

print("Calcolo degli integrali chimici classici (PySCF)...")
problem = driver.run()

# 2. Otteniamo l'Hamiltoniana (l'operatore dell'energia)
hamiltonian = problem.hamiltonian.second_q_op()

# 3. Mappiamo i Fermioni (elettroni) sui Qubit
mapper = JordanWignerMapper()
qubit_op = mapper.map(hamiltonian)

print("\n--- RISULTATO MAPPATURA ---")
print(f"Numero di qubit necessari per H2: {qubit_op.num_qubits}")
print("Operatore di Qubit generato con successo.")

# Inizializziamo la QPU per assicurarci che sia tutto pronto per il VQE
qpu = VirtualQPU()
