import numpy as np

def canonicalize(U):
    for i in range(U.shape[0]):
        for j in range(U.shape[1]):
            if not np.isclose(U[i, j], 0):
                phase = U[i, j] / np.abs(U[i, j])
                return U / phase
    return U


def get_single_qubit_cliffords():
    I = np.eye(2, dtype=complex)
    H = (1/np.sqrt(2))*np.array([[1,1],[1,-1]], dtype=complex)
    S = np.array([[1,0],[0,1j]], dtype=complex)

    queue = [I]
    unique = []

    while queue:
        U = queue.pop()
        Uc = canonicalize(U)

        if any(np.allclose(Uc, V) for V in unique):
            continue

        unique.append(Uc)

        for G in [H, S]:
            queue.append(G @ U)
            queue.append(U @ G)

    assert len(unique) == 24
    return unique