import pennylane as qml

def apply_noise(gate_idx, step_idx, config):
    """
    Apply noise channel Λ_{i_j,j} after each Clifford gate.

    This function implements the noise model in the RB protocol:

        S_{i_m} = Π_{j=1}^{m+1} (Λ_{i_j,j} ∘ C_{i_j})

    where:
        - C_{i_j} : Clifford gate at step j
        - Λ_{i_j,j} : noise channel applied after that gate

    The behavior of Λ_{i_j,j} is controlled by the configuration.

    Args:
        gate_idx (int):
            Index i_j of the Clifford gate C_{i_j}
            Used for gate-dependent noise models

        step_idx (int):
            Time step j in the sequence
            Can be used for time-dependent noise

        config (dict):
            Experiment configuration containing:
                - noise_type
                - p_noise (base noise strength)

    """

    # Base depolarizing probability
    p_base = config["p_noise"]

    # ------------------------------------------------------------
    # Case 1: Gate-independent noise
    # ------------------------------------------------------------
    #
    # Λ_{i_j,j} = Λ
    #
    # Same noise channel applied after every gate.
    # This corresponds to the standard RB assumption:
    #
    #     Λ_{i_j,j} = Λ  for all i_j, j
    #
    # In this case, RB theory predicts:
    #
    #     F(m) = A p^m + B   (pure exponential decay)
    #
    if config["noise_type"] == "gate_independent":
        p = p_base

    # ------------------------------------------------------------
    # Case 2: Gate-dependent noise
    # ------------------------------------------------------------
    #
    # Λ_{i_j,j} = Λ_{i_j}
    #
    # Noise depends on which Clifford gate is applied.
    #
    # This violates the ideal RB assumption and leads to:
    #
    #     F(m) = A p^m + B + C(m-1)(q - p^2)p^{m-2}
    #
    # i.e., deviation from exponential decay.
    #
    elif config["noise_type"] == "gate_dependent":
        # Simple example:
        # vary noise strength depending on gate index
        #
        # (modulo used just to create variation pattern)
        p = p_base * (1 + 0.5 * (gate_idx % 3))

    # ------------------------------------------------------------
    # Unsupported noise model
    # ------------------------------------------------------------
    else:
        raise ValueError("Unknown noise type")

    # ------------------------------------------------------------
    # Apply depolarizing channel
    # ------------------------------------------------------------
    #
    # Λ(ρ) = (1 - p)ρ + p * I/d
    #
    # This is a standard noise model used in RB,
    # and under Clifford twirling it remains depolarizing.
    #
    qml.DepolarizingChannel(p, wires=0) # p * I/d + (1-p) * ρ