import pennylane as qml
from sequence import compute_inverse
from noise import apply_noise

dev = qml.device("default.mixed", wires=1)


@qml.qnode(dev)
def run_sequence(seq, indices, config):

    for j, (C, idx) in enumerate(zip(seq, indices)):
        qml.QubitUnitary(C, wires=0)
        apply_noise(idx, j, config)

    U_inv = compute_inverse(seq)
    qml.QubitUnitary(U_inv, wires=0)

    apply_noise(-1, len(seq), config)

    return qml.probs(wires=0)