from matplotlib import pyplot, pyplot as plt
from utils import run, find_FWHM
from qutip import *
from args import *

# %%

args = {
    't_max': t_max,
    'sigma': sigma,
    'p': pulse_args['p'],
    'half_lorentzian': pulse_args['half_lorentzian'],
    'T1': T1,
    'T_dephasing': T2
}

# %%
matrix = []
fwhm = []
for i, a in enumerate(amplitudes):
    print(f'{i}/{len(amplitudes)}')
    multi_results = parallel_map(run, detunings, task_args=(a, args), progress_bar=True)
    spec_vec = []

    for m in multi_results:
        spec_vec.append(m[-1])

    fwhm.append(find_FWHM(detunings, spec_vec) / 2)
    matrix.append(spec_vec)

# %%
pyplot.plot(detunings / MHz, matrix[-1], label=f'A = {A_max / (2 * np.pi) / MHz:.2f} MHz, p= {args['p']}')
plt.axvline(x=quantum_limit / 1e6/2, color='r', )
plt.axvline(x=-quantum_limit / 1e6/2, color='r')
pyplot.xlabel('Detuning [MHz]')
pyplot.ylabel('Occupation probability')
pyplot.legend()
pyplot.ylim([0, 1])
pyplot.show()

# %%

x, y = np.meshgrid(detunings / MHz, amplitudes / MHz)
# pyplot.title(
#     f'T1 = {T1 / us} us  \n T2 = {T2 / us} us  \n sigma = {sigma / us} us \n eps0 = {w0 / (2 * np.pi) / GHz} GHz \n')
plt.plot(np.array(fwhm) / MHz, amplitudes / MHz / 2 / np.pi,'.g')

pyplot.pcolormesh(x, y / (2 * np.pi), matrix)
plt.axvline(x=quantum_limit / 1e6 / 2, color='r', )
plt.axvline(x=-quantum_limit / 1e6 / 2, color='r')
pyplot.colorbar()
pyplot.xlabel('Detuning [MHz]')
pyplot.ylabel('Amplitude [MHz]')
pyplot.legend(['HWFH', 'T2 limit'])
pyplot.show()
print(' ')

print('#### qubit_args: ####')
# print(
# f'qubit_frequency: {qubit_args["qubit_frequency"] / GHz / (2 * np.pi)} GHz \nT1: {qubit_args["T1"] / us} us \nT dephasing : {qubit_args["T_dephasing"] / us} us \n->T2 = {T2 / us} us ')
print(' ')
print('#### pulse_args: ####')

print(
    f'Rabi Amplitude = {A_max / 2 / np.pi / MHz:.2f} MHz \nLorentzian typical time = {sigma / ns:.2f} ns \ntotal time pulse = {t_max / us:.2f} us')

# %% save
