import numpy as np
from qutip import *
import matplotlib.pyplot as plt
from main import *

args_s = {
    'w0': 4.2 * 2 * np.pi * GHz,
    'alpha': 0.2 * 2 * np.pi * GHz,
    'w_rabi': 0.1 * 2 * np.pi * GHz,  # drive frequency
    'detuning': 0.0 * 2 * np.pi * GHz  # drive detuning
}

# Define the collapse operators
c_ops = []

# Define expectation operators
e_ops = [a.dag() * a]

# Define the initial state
psi0 = basis(N, 0)

# Define the time vector
t = np.linspace(0, 0.04 * us, 1000)

H = Hamiltonian(args_s)
# Solve the master equation
output = mesolve(H, psi0, t, c_ops, e_ops, args=args_s)

# Plot the results
plt.plot(t, output.expect[0])
plt.xlabel('Time (us)')
plt.ylim([-0.1, 1.3])
plt.ylabel('State Occupation Probability')
plt.show()
