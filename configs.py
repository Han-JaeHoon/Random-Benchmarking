"""
Experiment configuration for Randomized Benchmarking (RB).

This file defines all high-level parameters controlling the experiment.
The goal is to make the entire RB pipeline reproducible and easily configurable
without modifying core logic in other modules.

Each parameter here directly corresponds to a component of the RB protocol.
"""

CONFIG = {

    # ------------------------------------------------------------
    # Noise model type: defines Λ_{i_j,j}
    # ------------------------------------------------------------
    #
    # "gate_independent":
    #     Λ_{i_j,j} = Λ
    #     Same noise channel applied after every gate.
    #     This corresponds to the standard RB assumption.
    #
    # "gate_dependent":
    #     Λ_{i_j,j} = Λ_{i_j}
    #     Noise depends on which Clifford gate is applied.
    #     This introduces deviations from ideal exponential decay.
    #
    "noise_type": "gate_independent",


    # ------------------------------------------------------------
    # Noise strength (depolarizing parameter)
    # ------------------------------------------------------------
    #
    # Used inside the noise channel:
    #
    #     Λ(ρ) = (1 - p)ρ + p * I / d
    #
    # where:
    #     p = p_noise
    #
    # Increasing p_noise leads to faster decay in F(m).
    #
    "p_noise": 0.01,


    # ------------------------------------------------------------
    # Number of random sequences (Monte Carlo samples)
    # ------------------------------------------------------------
    #
    # For each sequence length m, we average over K random sequences:
    #
    #     F_seq(m) ≈ (1/K) Σ Tr[E S_{i_m}(ρ)]
    #
    # Larger K:
    #     - smoother decay curve
    #     - more accurate estimate of p
    #
    # Smaller K:
    #     - noisier results
    #
    "K": 100,


    # ------------------------------------------------------------
    # Sequence length range
    # ------------------------------------------------------------
    #
    # We evaluate F(m) for:
    #
    #     m = m_min, ..., m_max
    #
    # This determines the RB decay curve.
    #
    # Larger m_max:
    #     - better visibility of exponential decay
    #     - but lower signal (F(m) → B)
    #
    "m_min": 1,
    "m_max": 50,
}