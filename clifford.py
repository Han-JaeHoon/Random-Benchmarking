import numpy as np


def canonicalize(U):
    """
    Remove global phase from a unitary matrix.

    In quantum mechanics, two unitaries that differ only by a global phase
    represent the same physical operation. For example:
        U and e^{iθ}U are equivalent.

    This function normalizes a matrix by dividing out its global phase,
    so that equivalent Clifford elements are treated as identical.

    Method:
        - Find the first non-zero entry in U
        - Extract its phase
        - Divide the entire matrix by that phase

    Args:
        U (np.ndarray): 2x2 unitary matrix

    Returns:
        np.ndarray: phase-normalized unitary
    """
    for i in range(U.shape[0]):
        for j in range(U.shape[1]):
            if not np.isclose(U[i, j], 0):
                phase = U[i, j] / np.abs(U[i, j])
                return U / phase
    return U


def get_single_qubit_cliffords():
    """
    Generate the full single-qubit Clifford group (24 elements).

    The Clifford group is defined as the set of unitaries that map
    Pauli operators to Pauli operators under conjugation:

        C P C† ∈ {±X, ±Y, ±Z}

    It forms a finite group of size 24 for a single qubit.

    Construction method:
        - Start from generators: H (Hadamard), S (Phase)
        - Use group closure by repeatedly multiplying generators
        - Use a queue-based breadth-first search (BFS)
        - Remove duplicates using canonicalization (global phase removed)

    This guarantees:
        - Complete enumeration of the group
        - No duplicates up to global phase

    Returns:
        list of np.ndarray: list of 24 unique Clifford matrices
    """

    # Identity
    I = np.eye(2, dtype=complex)

    # Hadamard gate
    # Maps X ↔ Z, fundamental Clifford generator
    H = (1/np.sqrt(2))*np.array([[1,1],[1,-1]], dtype=complex)

    # Phase gate (S)
    # Maps X → Y → -X, generates rotations around Z axis
    S = np.array([[1,0],[0,1j]], dtype=complex)

    # Queue for BFS-style group generation
    queue = [I]

    # List of unique Clifford elements (after canonicalization)
    unique = []

    while queue:
        # Pop a candidate unitary
        U = queue.pop()

        # Remove global phase to compare properly
        Uc = canonicalize(U)

        # If already discovered, skip
        if any(np.allclose(Uc, V) for V in unique):
            continue

        # Otherwise, add to the Clifford set
        unique.append(Uc)

        # Generate new elements via left and right multiplication
        # This explores the full group closure
        for G in [H, S]:
            queue.append(G @ U)  # left multiplication
            queue.append(U @ G)  # right multiplication

    # The single-qubit Clifford group must have exactly 24 elements
    assert len(unique) == 24

    return unique