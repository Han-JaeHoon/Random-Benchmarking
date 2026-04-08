import matplotlib.pyplot as plt
import os


def plot_and_save(ms, F_list, filename):
    plt.figure()
    plt.plot(ms, F_list, 'o-')
    plt.xlabel("m")
    plt.ylabel("F(m)")
    plt.title("RB Decay")
    plt.savefig(filename)
    plt.close()