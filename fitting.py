import numpy as np
from scipy.optimize import curve_fit


def rb_model(m, A, p, B):
    return A * (p ** m) + B


def fit_rb_decay(m_list, F_list):

    m_arr = np.array(m_list)
    F_arr = np.array(F_list)

    popt, _ = curve_fit(
        rb_model,
        m_arr,
        F_arr,
        p0=[0.5, 0.99, 0.5],
        bounds=([0, 0, 0], [1, 1, 1])
    )

    return popt  # A, p, B


def compute_error_rate(p, d=2):
    return 1 - p - (1 - p) / d