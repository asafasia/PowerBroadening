import numpy as np
from qutip import *
import matplotlib.pyplot as plt

N = 10  # number of Fock states to consider
a = destroy(N)
GHz = 1e9
us = 1e-6

def Hamiltonian(args):
    def H1_coeff(t, args):
        return np.cos(args['detuning'] * t)

    w0 = args['w0']
    alpha = args['alpha']
    w_rabi = args['w_rabi']
    detuning = args['detuning']

    H_0 = detuning * a.dag() * a + alpha / 2 * a.dag() * a.dag() * a * a
    H_drive = w_rabi * (a + a.dag()) / 2

    H = [H_0, [H_drive, H1_coeff]]
    return H
