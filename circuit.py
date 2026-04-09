import pennylane as qml
from sequence import compute_inverse
from noise import apply_noise

# Use a mixed-state simulator since we include noise channels (Λ)
# default.qubit cannot simulate general quantum channels
dev = qml.device("default.mixed", wires=1)


@qml.qnode(dev)
def run_sequence(seq, indices, config):
    """
    Execute a single randomized benchmarking (RB) sequence.

    This function implements the noisy sequence operator:

        S_{i_m} = Π_{j=1}^{m+1} (Λ_{i_j,j} ∘ C_{i_j})

    where:
        - C_{i_j} : randomly sampled Clifford gates
        - Λ_{i_j,j} : noise channel (possibly gate- and time-dependent)

    The circuit structure is:

        |0> → C1 → Λ1 → C2 → Λ2 → ... → Cm → Λm → C_inv → Λ_{m+1} → measurement

    Args:
        seq (list): list of Clifford unitary matrices [C1, C2, ..., Cm]
        indices (list): indices of sampled Cliffords (i_j), used for Λ_{i_j,j}
        config (dict): experiment configuration (noise type, strength, etc.)

    Returns:
        probs (array): measurement probabilities in computational basis
                       probs[0] = survival probability
    """

    # Apply forward sequence: C_j followed by noise Λ_{i_j,j}
    # This corresponds to (Λ_{i_j,j} ∘ C_{i_j}) in the paper
    for j, (C, idx) in enumerate(zip(seq, indices)):
        # Apply Clifford gate C_{i_j}
        qml.QubitUnitary(C, wires=0)

        # Apply noise channel Λ_{i_j,j}
        # Depends on gate index (i_j) and time step (j)
        apply_noise(idx, j, config)

    # Compute and apply the inverse Clifford:
    # C_{m+1} = (C_m ... C_1)^(-1)
    # Ensures that the ideal (noise-free) circuit is identity
    U_inv = compute_inverse(seq)
    qml.QubitUnitary(U_inv, wires=0)

    # Apply final noise channel Λ_{m+1}
    # Included in the product definition of S_{i_m}
    apply_noise(-1, len(seq), config)

    # Measure in computational basis
    # Survival probability = probability of returning to |0>
    return qml.probs(wires=0)