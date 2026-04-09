import numpy as np
import os

from configs import CONFIG
from clifford import get_single_qubit_cliffords
from experiment import average_sequence_fidelity
from fitting import fit_rb_decay, compute_error_rate
from utils import plot_and_save


def main():
    """
    Entry point for the Randomized Benchmarking (RB) experiment.

    This function orchestrates the full RB pipeline:

        Step 1: Generate Clifford group
        Step 2: Construct and execute noisy sequences
        Step 3: Average over random sequences → F_seq(m)
        Step 4: Fit exponential decay → extract p and r

    The output includes:
        - F(m) values for each sequence length m
        - fitted parameters (A, p, B)
        - estimated error rate r
        - saved decay plot
    """

    # ------------------------------------------------------------
    # Prepare output directory
    # ------------------------------------------------------------
    # Ensures that result files (plots, etc.) can be saved
    os.makedirs("results", exist_ok=True)

    # ------------------------------------------------------------
    # Step 1: Generate 1-qubit Clifford group (size = 24)
    # ------------------------------------------------------------
    # These are used to sample random RB sequences
    cliffords = get_single_qubit_cliffords()

    # ------------------------------------------------------------
    # Define sequence length range
    # ------------------------------------------------------------
    # We will evaluate F_seq(m) for m in [m_min, ..., m_max]
    ms = np.arange(CONFIG["m_min"], CONFIG["m_max"] + 1)

    # ------------------------------------------------------------
    # Step 2–3: Run RB experiment (Monte Carlo averaging)
    # ------------------------------------------------------------
    # For each m:
    #   - sample K random sequences
    #   - execute noisy circuit S_{i_m}
    #   - compute survival probability
    #   - average over sequences
    F_list = []

    for m in ms:
        Fm = average_sequence_fidelity(m, cliffords, CONFIG)
        F_list.append(Fm)

        # Print intermediate results for monitoring
        print(f"m={m}, F={Fm}")

    # ------------------------------------------------------------
    # Step 4: Fit exponential decay
    # ------------------------------------------------------------
    # Fit F(m) = A * p^m + B
    # Extract:
    #   - p: depolarizing parameter
    #   - A, B: SPAM-related constants
    A, p, B = fit_rb_decay(ms, F_list)

    # Convert p → average error rate r
    r = compute_error_rate(p)

    # ------------------------------------------------------------
    # Print final results
    # ------------------------------------------------------------
    print("\n===== FIT RESULT =====")
    print("A =", A)
    print("p =", p)
    print("B =", B)
    print("r =", r)

    # ------------------------------------------------------------
    # Save RB decay plot
    # ------------------------------------------------------------
    # Plot: m vs F(m)
    plot_and_save(ms, F_list, f"results/rb_decay_{p:.4f}.png")


# ------------------------------------------------------------
# CLI entry point
# ------------------------------------------------------------
# Allows execution via:
#     python main.py
if __name__ == "__main__":
    main()