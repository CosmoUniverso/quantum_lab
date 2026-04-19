# Quantum-Material-Lab-GPU (QMat-GPU)
**License:** AGPL-3.0
**Author:** CosmoUniverso
**Environment:** WSL2 • Ubuntu • NVIDIA CUDA • Python 3.11

---

# IT Descrizione

**Quantum-Material-Lab-GPU** è un ambiente di ricerca dedicato alla simulazione di:
- chimica quantistica,
- fisica dello stato solido,
- scienza dei materiali su GPU consumer.

Il progetto utilizza:
- **PySCF** per i calcoli *ab initio*,
- **Qiskit Nature** per la mappatura fermionica,
- **Active Space Transformer** per ridurre sistemi complessi,
- **Qiskit Aer + cuQuantum** per la simulazione quantistica accelerata su GPU.

L’obiettivo è studiare materiali reali (Diamante, Acciaio Fe–C, superfici di Platino) entro i limiti di una GPU RTX 3060, raggiungendo fino a **26–28 qubit** in modo stabile.

## Installazione (WSL2)

conda create -n qpu python=3.11
conda activate qpu
pip install qiskit qiskit-aer-gpu qiskit-nature qiskit-algorithms pyscf
GPU Setup
bash
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64
export CUQUANTUM_ROOT=$CONDA_PREFIX
Licenza
Questo progetto è distribuito sotto licenza GNU Affero General Public License v3.0 (AGPL-3.0).

# US Description
Quantum-Material-Lab-GPU is a research environment for:

quantum chemistry,

solid-state physics,

GPU‑accelerated materials simulation.

The framework integrates:

PySCF for ab initio calculations,

Qiskit Nature for fermionic mapping,

Active Space Transformer for orbital reduction,

Qiskit Aer + cuQuantum for GPU‑accelerated quantum simulation.

The goal is to explore real materials (Diamond, Fe–C steel, Platinum surfaces) within the constraints of an RTX 3060 GPU, achieving stable simulations up to 26–28 qubits.

Installation (WSL2)
bash
conda create -n qpu python=3.11
conda activate qpu
pip install qiskit qiskit-aer-gpu qiskit-nature qiskit-algorithms pyscf
GPU Setup
bash
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64
export CUQUANTUM_ROOT=$CONDA_PREFIX
License
This project is released under the GNU Affero General Public License v3.0 (AGPL-3.0).
