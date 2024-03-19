import matplotlib.pyplot as plt

from utils import *

args = {
    't_max': t_max,
    'sigma': sigma,
    'p': pulse_args['p'],
    'half_lorentzian': pulse_args['half_lorentzian'],
    'T1': T1,
    'T_dephasing': T2
}


# %%
def run_p(p, args):
    args['p'] = p
    multi_results = parallel_map(run, detunings, task_args=(A_max, args))
    spec_vec = []
    for m in multi_results:
        spec_vec.append(m[-1])

    return spec_vec


matrix = []
ps = np.linspace(1e-2, 1e-3, 30)
fwhms = []
for i, p in enumerate(ps):
    print(f'{i}/{len(ps)}')
    spec_vec = run_p(p, args)
    fwhm = find_FWHM(detunings, spec_vec)
    matrix.append(spec_vec)
    fwhms.append(fwhm)

# %%
fwhms = np.array(fwhms)
x, y = np.meshgrid(detunings / MHz, ps)
plt.ylim([ps[-1], ps[0]])
plt.pcolormesh(x, y, matrix, shading='auto')
plt.plot(fwhms / MHz/2, ps, color='g')
plt.colorbar()
plt.axvline(x=quantum_limit / 1e6, color='r', )
plt.axvline(x=-quantum_limit / 1e6, color='r')
plt.yscale('log')

plt.show()
