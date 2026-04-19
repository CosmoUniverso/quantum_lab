from qiskit_aer import AerSimulator
from qiskit import transpile

class VirtualQPU:
    def __init__(self):
        # Tenta di forzare l'uso della GPU
        sim_check = AerSimulator()
        if 'GPU' in sim_check.available_devices():
            self.backend = AerSimulator(method="statevector", device="GPU")
            print(" VirtualQPU: Inizializzata su RTX 3060 (GPU)")
        else:
            self.backend = AerSimulator(method="statevector", device="CPU")
            print(" VirtualQPU: GPU non trovata, fallback su CPU")

    def run(self, circuit, shots=1024):
        # Il transpiler adatta il tuo circuito logico ai gate fisici del simulatore
        tc = transpile(circuit, self.backend)
        result = self.backend.run(tc, shots=shots).result()

        # Ritorna i conteggi se ci sono misurazioni classiche, altrimenti lo statevector
        if circuit.num_clbits > 0:
            return result.get_counts()
        return result
