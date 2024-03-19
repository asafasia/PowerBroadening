import numpy as np
import qutip

N_dim = 2
GHz = 1e9
MHz = 1e6
us = 1e-6
ns = 1e-9
qubit_args = {
    "qubit_frequency": 5 * GHz * 2 * np.pi,
    "T1": 10 * us,
    "T_dephasing": 5 * us,
}

pulse_args = {
    "drive_amplitude": 5 * MHz * 2 * np.pi,
    "drive_frequency": 5 * GHz * 2 * np.pi,
    "pulse_type": "lorentzian",
    "sigma": 0,
    "t_max": 5 * us,
    "p": 0.01,
    "half_lorentzian": False
}
sweep_args = {
    'detunings': np.linspace(-10 * MHz, 10 * MHz, 101),
    'amplitudes': np.linspace(0 * MHz * 2 * np.pi, 100 * MHz * 2 * np.pi, 50)
}

solver_args = {
    'n_iter': 10000
}

w0 = qubit_args["qubit_frequency"]
A_max = pulse_args["drive_amplitude"]

detunings = sweep_args['detunings']
amplitudes = sweep_args['amplitudes']

n = solver_args['n_iter']
t_max = pulse_args['t_max']

sigma = pulse_args['sigma']

T1 = qubit_args['T1']
T_dephasing = qubit_args['T_dephasing']

gamma1 = 1 / T1
gamma_dephasing = 1 / T_dephasing

gamma2 = gamma1 / 2 + gamma_dephasing
T2 = 1 / gamma2

tlist = np.linspace(-t_max / 2, t_max / 2, n + 1)
psi0 = qutip.basis(N_dim, 0)

quantum_limit = 1 / T2
