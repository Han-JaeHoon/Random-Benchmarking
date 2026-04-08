import pennylane as qml

def apply_noise(gate_idx, step_idx, config):
    p_base = config["p_noise"]

    if config["noise_type"] == "gate_independent":
        p = p_base

    elif config["noise_type"] == "gate_dependent":
        p = p_base * (1 + 0.5 * (gate_idx % 3))

    else:
        raise ValueError("Unknown noise type")

    qml.DepolarizingChannel(p, wires=0)