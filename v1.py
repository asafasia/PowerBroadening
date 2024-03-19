import numpy as np
from matplotlib import pyplot
import qutip

GHz = 1e9
us = 1e-6

delta = 1 * GHz * 2 * np.pi
eps0 = 1.0 * GHz * 2 * np.pi

A = 0.01 * GHz * 2 * np.pi
omega = 1.0 * GHz * 2 * np.pi
T = 2 * np.pi / omega

tlist = np.linspace(0.0, 1000 * T, 501)
psi0 = qutip.basis(2, 0)

H0 = eps0 / 2.0 * qutip.sigmaz()
H1 = A / 2.0 * qutip.sigmax()

args = {'w': omega}
H = [H0, [H1, lambda t, args: np.sin(args['w'] * t)]]

# noise power spectrum
T1 = 2 * us
gamma1 = 1 / T1


def noise_spectrum(omega):
    return 0.5 * gamma1 * omega / (2 * np.pi) / GHz


# find the floquet modes for the time-dependent hamiltonian
f_modes_0, f_energies = qutip.floquet_modes(H, T, args)

# precalculate mode table
f_modes_table_t = qutip.floquet_modes_table(
    f_modes_0, f_energies, np.linspace(0, T, 500 + 1), H, T, args,
)

# solve the floquet-markov master equation
output = qutip.fmmesolve(H, psi0, tlist, [qutip.sigmax()], [], [noise_spectrum], T, args)

# calculate expectation values in the computational basis
p_ex = np.zeros(tlist.shape, dtype=np.complex128)
for idx, t in enumerate(tlist):
    f_modes_t = qutip.floquet_modes_t_lookup(f_modes_table_t, t, T)
    f_states_t = qutip.floquet_states(f_modes_t, f_energies, t)
    p_ex[idx] = qutip.expect(qutip.num(2), output.states[idx].transform(f_states_t, True))

# For reference: calculate the same thing with mesolve
output = qutip.mesolve(H, psi0, tlist,
                       [np.sqrt(gamma1) * qutip.sigmax()], [qutip.num(2)],
                       args)
p_ex_ref = output.expect[0]

# plot the results
pyplot.plot(tlist / us, np.real(p_ex), 'r--', tlist / us, 1 - np.real(p_ex), 'b--')
pyplot.plot(tlist / us, np.real(p_ex_ref), 'r', tlist / us, 1 - np.real(p_ex_ref), 'b')
pyplot.xlabel('Time [us]')
pyplot.ylabel('Occupation probability')
pyplot.legend(("Floquet $P_1$", "Floquet $P_0$", "Lindblad $P_1$", "Lindblad $P_0$"))
pyplot.show()
