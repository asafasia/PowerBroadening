import json
import numpy as np
from matplotlib import pyplot as plt
from qutip import *
from args import *


def save_to_json(dict, filename):
    with open(filename, 'w') as f:
        json.dump(dict, f)


def load_from_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)


def gaussian(t, args):
    sigma = args['sigma']
    return np.exp(-t ** 2 / (2 * sigma ** 2))


def lorentzian(t, args):
    sigma = args['sigma']
    p = args['p'] / 2
    t_max = args['t_max']
    if p:
        sigma = t_max / np.sqrt((1 / p) ** 2 - 1)

    return 1 / (1 + (t / sigma) ** 2) ** (1 / 2) - 2*p


def lorentzian_half(t, args):
    return (lorentzian(t, args) - 2 * lorentzian(t, args) * np.heaviside(t, 0.5))


# def H1_coeff(t, args):
#     if args['half_lorentzian']:
#         return np.sin(args['w'] * t) * lorentzian_half(t, args)
#     else:
#         return np.sin(args['w'] * t) * lorentzian_half(t, args)


def Hamiltonian(detuning, amplitude):
    H0 = -detuning * destroy(N_dim).dag() * destroy(N_dim)
    H1 = amplitude / 2.0 * (destroy(N_dim) + destroy(N_dim).dag())

    return [H0, [H1, lorentzian_half]]


def plot_pulse(tlist, args):
    if args['half_lorentzian']:
        pulse = lorentzian_half(tlist, args)
    else:
        pulse = lorentzian(tlist, args)
    plt.plot(tlist / us, pulse, label='pulse')


def run(detuning, amplitude, args):
    args['w'] = w0 - detuning
    T1 = args['T1']
    T_dephasing = args['T_dephasing']

    H = Hamiltonian(detuning, amplitude)

    c_opts = []

    if T1 != 0:
        c_opts.append(np.sqrt(1 / T1) * qutip.destroy(2))

    if T_dephasing != 0:
        c_opts.append(np.sqrt(1 / T_dephasing) * qutip.sigmaz())

    output = qutip.mesolve(H, psi0, tlist,
                           c_opts,
                           [qutip.num(2)],
                           args)

    return output.expect[0]


def find_FWHM(x, y):
    try:
        # Step 2: Identify the Peak
        peak_value = np.max(y)
        peak_index = np.argmax(y)

        # Step 3: Determine the Half Maximum
        half_max = peak_value / 2

        left_index = np.where(y[:peak_index] < half_max)[0][-1]
        # Find the right side of the peak
        right_index = np.where(y[peak_index:] < half_max)[0][0] + peak_index

        fwhm = x[right_index] - x[left_index]
    except:
        fwhm = 0

    return fwhm
