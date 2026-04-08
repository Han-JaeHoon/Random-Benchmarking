import numpy as np
import os

from configs import CONFIG
from clifford import get_single_qubit_cliffords
from experiment import average_sequence_fidelity
from fitting import fit_rb_decay, compute_error_rate
from utils import plot_and_save


def main():

    os.makedirs("results", exist_ok=True)

    cliffords = get_single_qubit_cliffords()

    ms = np.arange(CONFIG["m_min"], CONFIG["m_max"] + 1)

    F_list = []
    for m in ms:
        Fm = average_sequence_fidelity(m, cliffords, CONFIG)
        F_list.append(Fm)
        print(f"m={m}, F={Fm}")

    A, p, B = fit_rb_decay(ms, F_list)
    r = compute_error_rate(p)

    print("\n===== FIT RESULT =====")
    print("A =", A)
    print("p =", p)
    print("B =", B)
    print("r =", r)

    plot_and_save(ms, F_list, "results/rb_decay.png")


if __name__ == "__main__":
    main()