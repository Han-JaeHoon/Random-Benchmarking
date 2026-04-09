import matplotlib.pyplot as plt
import os


def plot_and_save(ms, F_list, filename):
    """
    Plot and save the RB decay curve.

    This function visualizes the result of the RB experiment:

        F(m) vs m

    where:
        - m : sequence length
        - F(m) : averaged survival probability

    The plot is used to:
        - verify exponential decay behavior
        - qualitatively assess noise strength
        - compare different noise models (e.g., gate-independent vs gate-dependent)

    Args:
        ms (array-like):
            Sequence lengths (m values)

        F_list (array-like):
            Corresponding averaged fidelities F(m)

        filename (str):
            Path where the plot will be saved

    Output:
        Saves a plot image (e.g., results/rb_decay.png)
    """

    # Create a new figure
    plt.figure()

    # Plot F(m) vs m
    # 'o-' : marker + line for clarity
    plt.plot(ms, F_list, 'o-')

    # Label axes
    plt.xlabel("m")       # sequence length
    plt.ylabel("F(m)")    # survival probability
    plt.ylim(min(0.5, min(F_list)), 1)        # invert y-axis for better visualization of decay 

    # Title indicating this is RB decay
    plt.title("RB Decay")

    # Save figure to file
    plt.savefig(filename)

    # Close figure to free memory (important for repeated runs)
    plt.close()