import numpy as np


def sample_clifford_sequence(m, cliffords):
    """
    Sample a random sequence of Clifford gates.

    This corresponds to selecting a random sequence i_m:

        i_m = (i_1, i_2, ..., i_m)

    where each i_j is uniformly sampled from the Clifford group.

    In RB, this ensures:
        - uniform sampling over Clifford group
        - realization of Clifford twirling effect

    Args:
        m (int):
            Sequence length (number of Clifford gates)

        cliffords (list):
            List of available Clifford matrices (size = 24 for 1 qubit)

    Returns:
        seq (list):
            List of sampled Clifford matrices [C1, C2, ..., Cm]

        indices (np.ndarray):
            Corresponding indices [i_1, i_2, ..., i_m]
            Used for noise model Λ_{i_j,j}
    """

    # Randomly sample indices i_j ∈ {0, ..., 23}
    indices = np.random.choice(len(cliffords), size=m)

    # Map indices to actual Clifford matrices
    seq = [cliffords[i] for i in indices]

    return seq, indices


def compute_inverse(sequence):
    """
    Compute the inverse Clifford for a given sequence.

    In RB, the final gate is chosen such that:

        C_{m+1} = (C_m ... C_1)^(-1)

    so that the ideal (noise-free) circuit satisfies:

        C_{m+1} C_m ... C_1 = I

    This ensures that:
        - any deviation from identity is due to noise only
        - survival probability directly reflects accumulated noise

    Procedure:
        1. Compute the total unitary U = C_m ... C_1
        2. Return U^{-1} = U† (since Clifford gates are unitary)

    Args:
        sequence (list):
            List of Clifford matrices [C1, C2, ..., Cm]

    Returns:
        np.ndarray:
            Inverse unitary matrix C_{m+1}
    """

    # Initialize as identity
    U = np.eye(2, dtype=complex)

    # Compute product U = C_m ... C_1
    # (note: left multiplication accumulates correctly)
    for C in sequence:
        U = C @ U

    # Return inverse U† (Hermitian conjugate)
    return U.conj().T