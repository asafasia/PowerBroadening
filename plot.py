from utils import load_from_json
import numpy as np
import matplotlib.pyplot as plt

dict = load_from_json('data/data_star.json')

data = dict['data']

metadata = dict['metadata']

x = data['x']
y = data['y']
matrix = data['matrix']

# %%

x, y = np.meshgrid(x, y)

plt.pcolormesh(x/1e6, y/1e9, matrix)
plt.colorbar()
plt.xlabel('Detuning [MHz]')
plt.ylabel('Amplitude [GHz]')
plt.title('Lorentzian Pulse')
plt.show()

# %%




