import numpy as np
from scipy.optimize import curve_fit


def rb_model(m, A, p, B):
    """
    Exponential decay model used in Randomized Benchmarking.

    Corresponds to the zeroth-order (gate-independent noise) model:

        F(m) = A * p^m + B

    where:
        - p : depolarizing parameter (decay rate)
        - A, B : constants absorbing SPAM errors and edge effects

    Args:
        m (array-like):
            Sequence lengths

        A, p, B (float):
            Fit parameters

    Returns:
        array-like:
            Predicted F(m) values
    """
    return A * (p ** m) + B


def fit_rb_decay(m_list, F_list):
    """
    Fit RB data to extract decay parameter p.

    This implements Step 4 of the RB protocol:

        Fit F_seq(m) to:
            F(m) = A p^m + B

    Input data comes from Step 3:

        F_seq(m) = average survival probability

    Procedure:
        - Convert input lists to numpy arrays
        - Perform non-linear least squares fitting
        - Extract parameters (A, p, B)

    Args:
        m_list (list or array):
            Sequence lengths

        F_list (list or array):
            Corresponding averaged fidelities F_seq(m)

    Returns:
        tuple:
            (A, p, B)

    Notes:
        - Initial guess p ≈ 1 is important for convergence
        - Bounds enforce physically meaningful values (0 ≤ A, p, B ≤ 1)
    """

    # Convert inputs to numpy arrays for fitting
    m_arr = np.array(m_list)
    F_arr = np.array(F_list)

    # Perform non-linear curve fitting
    popt, _ = curve_fit(
        rb_model,
        m_arr,
        F_arr,
        p0=[0.25, 0.5, 0.25],        # initial guess
        bounds=([0, 0, 0], [1, 1, 1])  # physical constraints
    )

    # popt = (A, p, B)
    return popt # p = 1 - p_base * (4/3)


def compute_error_rate(p, d=2):
    """
    Convert RB decay parameter p to average error rate r.

    From RB theory:

        F_avg = p + (1 - p) / d
        r = 1 - F_avg

    Combining:

        r = 1 - p - (1 - p)/d

    For single qubit (d = 2):

        r = (1 - p) / 2

    Args:
        p (float):
            Decay parameter from RB fitting

        d (int):
            Hilbert space dimension (default: 2 for 1 qubit)

    Returns:
        float:
            Average error rate r
    """
    return 1 - p - (1 - p) / d