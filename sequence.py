import numpy as np

def sample_clifford_sequence(m, cliffords):
    indices = np.random.choice(len(cliffords), size=m)
    return [cliffords[i] for i in indices], indices


def compute_inverse(sequence):
    U = np.eye(2, dtype=complex)
    for C in sequence:
        U = C @ U
    return U.conj().T