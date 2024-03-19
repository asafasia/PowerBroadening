from utils import *

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
plt.title('Population as Function of the Pulse\n in Resonance Frequency and Max Amplitude ')
detuning = 15 * MHz
res = run(detuning, A_max, args)
plt.plot(tlist / us, res, label=f'state, detuning = {detuning/MHz} MHz')
plot_pulse(tlist, args)
plt.xlabel('Time [us]')
plt.ylabel(' Population')
plt.legend()
plt.show()

# %%

multi_results = parallel_map(run, detunings, task_args=(A_max, args), progress_bar=True)
spec_vec = []

for m in multi_results:
    spec_vec.append(m[-1])

# %%
plt.title('Spectroscopy ')
plt.xlabel('Detuning [MHz]')
plt.ylabel('Occupation')

plt.plot(detunings / 1e6, spec_vec, label=f'A = {A_max / (2 * np.pi * 1e6):.0f} MHz')
x = detunings / 1e6
y = spec_vec

fwhm = find_FWHM(x, y)

plt.axvline(x=quantum_limit / 1e6/2, color='r', )
plt.axvline(x=-quantum_limit / 1e6/2, color='r')

plt.axvline(x=-fwhm / 2, color='g', linestyle='--')
plt.axvline(x=fwhm / 2, color='g', linestyle='--')

print(f'FWHM = {fwhm} MHz')
print(f'T2 limit = {quantum_limit / 1e6} MHz')
print()
plt.legend()
plt.show()
