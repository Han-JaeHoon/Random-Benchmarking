# Randomized Benchmarking (RB) Implementation

## Overview

This repository implements the Randomized Benchmarking (RB) protocol described in:

> Magesan, Gambetta, Emerson  
> *Scalable and Robust Randomized Benchmarking of Quantum Processes* (PRL, 2011)

The goal of this project is to faithfully reproduce the RB protocol at the level of both:
- experimental procedure
- theoretical interpretation

The implementation follows the paper step-by-step and supports:
- noiseless simulation
- gate-independent noise
- gate-dependent noise

This codebase is designed not only to reproduce RB results but also to serve as a foundation for further research, including extensions toward correlated noise estimation and Pauli channel learning.

---

## What This Repository Does

This project implements the full RB pipeline:

1. Generate random Clifford sequences
2. Construct quantum circuits with noise
3. Measure survival probabilities
4. Average over random sequences
5. Fit exponential decay to extract noise parameters

The implementation preserves the structure of the original protocol:

$$
S_{i_m} = \prod_{j=1}^{m+1} (\Lambda_{i_j,j} \circ C_{i_j})
$$

and computes:

$$
F_{\mathrm{seq}}(m) = \mathrm{Tr}[E_\psi S_m(\rho_\psi)]
$$

---

## Project Structure

```

rb_project/
│
├── main.py                # Entry point (CLI execution)
├── configs.py             # Experiment configuration
│
├── clifford.py            # 1-qubit Clifford group (24 elements)
├── sequence.py            # Sequence generation and inverse computation
├── noise.py               # Noise model Λ_{i_j,j}
├── circuit.py             # Quantum circuit (QNode)
│
├── experiment.py          # Step 1–3 (RB experiment loop)
├── fitting.py             # Step 4 (curve fitting)
├── utils.py               # Plotting utilities
│
└── results/               # Output directory

````

---

## Installation

Install required dependencies:

```bash
pip install pennylane numpy scipy matplotlib
````

---

## How to Run

From the project root:

```bash
python main.py
```

---

## Expected Output

### Terminal Output

```
m=1, F=...
m=2, F=...
...
===== FIT RESULT =====
A = ...
p = ...
B = ...
r = ...
```

### Saved Output

```
results/rb_decay.png
```

---

## How to Verify Correctness

### 1. Noiseless Case

Set:

```python
p_noise = 0
```

Expected:

* F(m) ≈ 1 for all m
* No decay

---

### 2. Gate-Independent Noise

Expected:

* Smooth exponential decay
* Good fit to:

$$ F(m) = A p^m + B $$

---

### 3. Gate-Dependent Noise

Expected:

* Deviation from pure exponential
* Visible curvature in residuals

This corresponds to the correction term:

$$ (q - p^2) \neq 0 $$

---

## Theoretical Background

### Motivation

Quantum Process Tomography (QPT):

* scales exponentially
* sensitive to SPAM errors

Randomized Benchmarking solves this by:

* sampling random Clifford sequences
* averaging over sequences
* extracting a single decay parameter

---

### Clifford Twirling

The RB protocol relies on the fact that the Clifford group forms a unitary 2-design.

This implies:

$$ \frac{1}{K} \sum_C C^\dagger \Lambda C = \Lambda_{\text{dep}} $$

where:

$$ \Lambda_{\text{dep}}(\rho) = p \rho + (1 - p)\frac{I}{d} $$

Thus, arbitrary noise is effectively reduced to a depolarizing channel.

---

### Measured Quantity

RB measures:

$$ F(m) = \mathrm{Tr}[E_\psi S_m(\rho_\psi)] $$

which experimentally corresponds to:

> Probability of returning to the initial state after applying a random sequence and its inverse.

---

### Exponential Decay Model

For gate-independent noise:

$$ F(m) = A p^m + B $$

where:

* $p$ : depolarizing parameter
* $A, B$ : SPAM-related constants

---

### Error Rate

$$ r = 1 - p - \frac{1 - p}{d} $$

For 1 qubit $(d=2)$:

$$ r = \frac{1 - p}{2} $$

---

### Gate-Dependent Noise

If noise depends on the gate:

$$ \Lambda_{i_j,j} \neq \Lambda $$

then:

$$ F(m) = A p^m + B + C(m-1)(q - p^2)p^{m-2} $$

This leads to deviations from exponential decay.

---

## Implemented Features

* Exact 1-qubit Clifford group (24 elements)
* Random sequence generation
* Exact inverse gate construction
* Noise insertion after each gate
* Support for:

  * gate-independent noise
  * gate-dependent noise
* Monte Carlo averaging over sequences
* Curve fitting to extract:

  * decay parameter $p$
  * error rate $r$
* Plot generation

---

## Design Principles

* Faithful implementation of the original RB protocol
* Modular separation of components
* Reproducible experiments via configuration
* Clear mapping between theory and code

---

## Future Work

### 1. Noise Model Extensions

* time-dependent noise
* correlated multi-qubit noise

---

### 2. Higher-Order Fitting

* include correction term explicitly
* estimate $q - p^2$

---

### 3. Multi-Qubit RB

* extend Clifford group
* include entangling gates (CNOT)

---

### 4. Pauli Channel Estimation

Move beyond RB:

$$ E(P_j) = \lambda(j) P_j $$

RB measures a single parameter $p$, whereas full noise learning requires estimating all $\lambda(j)$.

---

### 5. Connection to Surface Code Protocol

This implementation serves as a stepping stone toward:

* correlated noise estimation
* stabilizer-based protocols
* Walsh-Hadamard reconstruction

---

## Summary

This repository implements the full Randomized Benchmarking protocol from first principles and verifies its behavior under different noise models.

It provides both:

* a faithful reproduction of the original method
* a structured platform for further research in quantum noise characterization
