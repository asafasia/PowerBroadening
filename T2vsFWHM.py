import numpy as np
from utils import *


T1 = 15 * us
T2 = np.linspace(1*us,2*T1,100)

# %%
fwhms = []
for t2 in T2:

    args = {
        't_max': t_max,
        'sigma': sigma,
        'p': pulse_args['p'],
        'half_lorentzian': pulse_args['half_lorentzian'],
        'T1': T1,
        'T_dephasing': t2
    }



    multi_results = parallel_map(run, detunings, task_args=(A_max, args), progress_bar=True)
    spec_vec = []

    for m in multi_results:
        spec_vec.append(m[-1])

    x = detunings / 1e6
    y = spec_vec
    fwhm = find_FWHM(x, y)
    print(f'FWHM = {fwhm} MHz')
    fwhms.append(fwhm)

# plt.plot(T2 /us, fwhms)
plt.plot(1/T2 /MHz, fwhms,'o')
plt.xlabel('1/T2 [MHz]')
plt.ylabel('FWHM [MHz]')
plt.title('FWHM vs 1/T2')
plt.show()

# %%
# plt.title('Spectroscopy ')
# plt.xlabel('Detuning [MHz]')
# plt.ylabel('Occupation')
#
# plt.plot(detunings / 1e6, spec_vec, label=f'A = {A_max / (2 * np.pi * 1e6)} MHz')

#
#
#
# plt.axvline(x=quantum_limit / 1e6, color='r', )
# plt.axvline(x=-quantum_limit / 1e6, color='r')
#
# plt.axvline(x=-fwhm / 2, color='g', linestyle='--')
# plt.axvline(x=fwhm / 2, color='g', linestyle='--')
#
# print(f'FWHM = {fwhm} MHz')
# print(f'T2 limit = {quantum_limit / 1e6} MHz')
# print()
# plt.legend()
# plt.show()
