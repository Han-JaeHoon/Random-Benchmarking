import numpy as np
from sequence import sample_clifford_sequence
from circuit import run_sequence


def average_sequence_fidelity(m, cliffords, config):
    probs = []

    for _ in range(config["K"]):
        seq, indices = sample_clifford_sequence(m, cliffords)
        p = run_sequence(seq, indices, config)[0]
        probs.append(p)

    return np.mean(probs)