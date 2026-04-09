import numpy as np
from sequence import sample_clifford_sequence
from circuit import run_sequence


def average_sequence_fidelity(m, cliffords, config):
    """
    Compute the averaged sequence fidelity F_seq(m).

    This function implements Step 3 of the RB protocol:

        F_seq(m) = Tr[E_ψ S_m(ρ_ψ)]

    where:

        S_m = (1 / |{i_m}|) Σ S_{i_m}

    In practice, this average is approximated using Monte Carlo sampling:

        F_seq(m) ≈ (1 / K) Σ_{k=1}^K Tr[E_ψ S_{i_m^{(k)}}(ρ_ψ)]

    Procedure:
        1. Sample K random Clifford sequences of length m
        2. For each sequence:
            - Run the noisy quantum circuit S_{i_m}
            - Measure survival probability (probability of |0⟩)
        3. Average the results

    Args:
        m (int):
            Sequence length (number of random Clifford gates)

        cliffords (list):
            List of 1-qubit Clifford matrices (size 24)

        config (dict):
            Experiment configuration, containing:
                - K: number of random sequences
                - noise_type: type of Λ_{i_j,j}
                - p_noise: noise strength

    Returns:
        float:
            Averaged survival probability F_seq(m)
    """

    # Store survival probabilities from each random sequence
    probs = []

    # Monte Carlo sampling over random sequences
    for _ in range(config["K"]):

        # Step 1: Sample a random Clifford sequence i_m
        # seq      : [C1, C2, ..., Cm]
        # indices  : [i_1, i_2, ..., i_m] (used for noise Λ_{i_j,j})
        seq, indices = sample_clifford_sequence(m, cliffords)

        # Step 2: Execute the noisy sequence S_{i_m}
        # run_sequence returns probabilities over computational basis
        # We take probs[0] = survival probability (return to |0⟩)
        p = run_sequence(seq, indices, config)[0]

        # Collect result
        probs.append(p)

    # Step 3: Average over all sampled sequences
    return np.mean(probs)