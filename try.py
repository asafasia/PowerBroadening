from dataclasses import dataclass
import numpy as np
from matplotlib import pyplot as plt
from qutip import *

N = 4
GHz = 1e9
MHz = 1e6
us = 1e-6
a = destroy(N)


class QubitSimulation:
    def __init__(self, w_rabi, detuning):
        self.w0 = 4.2 * 2 * np.pi * GHz,
        self.alpha = -0.2 * 2 * np.pi * GHz
        self.w_rabi = w_rabi
        self.detuning = detuning
        self.T2 = 0.5e-6

    def _hamiltonian(self):
        H = self.detuning * a.dag() * a + self.alpha/2 * a.dag() * a.dag() * a * a + self.w_rabi * (a.dag() + a)
        return H

    def single_run(self, detuning=None, plot=False):
        H = self._hamiltonian()

        c_ops = [np.sqrt(1 / self.T2) * a.dag() * a]
        # c_ops = []
        e_ops = [a.dag() * a]
        psi0 = basis(N, 0)

        times = np.linspace(0, 10 * us, 1000)

        output = mesolve(H, psi0, times, c_ops, e_ops)

        if plot:
            plt.plot(times * us ** -1, output.expect[0])
            plt.xlabel('Time [us]')
            plt.ylabel('Population')
            plt.ylim([-0.1, 1.1])
            plt.show()

        return output.expect[0]


class Spectroscopy:
    def __init__(self, w_rabi, span, steps):
        self.w_rabi = w_rabi
        self.span = span
        self.steps = steps

    def run(self, plot=False):
        detunings = np.linspace(-self.span, self.span, self.steps)
        results = []

        for i, detuning in enumerate(detunings):
            print(f'Running simulation {i + 1}/{self.steps}')
            sim_data = QubitSimulation(w_rabi, detuning)
            results.append(sim_data.single_run(detuning)[-1])

        if plot:
            plt.plot(detunings / MHz, results)
            plt.xlabel('Detuning [MHz]')
            plt.ylabel('Population')
            plt.ylim([-0.1, 1.1])
            plt.show()
        return results


if __name__ == '__main__':
    w_rabi = 1/2 * 2 * np.pi * MHz
    detuning = -100 * 2 * np.pi * MHz

    # sim_data = QubitSimulation(w_rabi, detuning)
    # sim_data.single_run(plot=True)

    spectroscopy = Spectroscopy(w_rabi=w_rabi, span=200 * MHz, steps=101)
    spectroscopy.run(plot=True)
