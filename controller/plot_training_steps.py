"""Plot steps per episode after a training session."""
# Figure 4.1

import numpy as np
import h5py
import parameters as params
import matplotlib.pyplot as plt
from matplotlib import gridspec

fontsize_large = 32
fontsize_small = 28
line_width = 2

# Load the training data
filename = "training_" + params.train_on
filepath_h5f = "../data/" + params.session + '/' + filename + '.h5'
h5f = h5py.File(filepath_h5f, 'r')

vrep_steps = np.array(h5f['vrep_steps'], dtype = float)

fig = plt.figure(figsize=(20, 10))

ax1 = plt.subplot(111)
ax1.set_xlabel('Epsiode', fontsize=fontsize_large)
ax1.set_ylabel('Steps', fontsize=fontsize_large)
plt.xticks(np.arange(0, 6, 1), fontsize=fontsize_small)
plt.yticks(fontsize=fontsize_small)
plt.grid(linestyle=':')
plt.plot(vrep_steps, lw=line_width)

fig.tight_layout()

filename_pdf = params.session + '_' + filename + '_steps'
filepath_pdf = "../plots/training/" + filename_pdf + ".pdf"
plt.savefig(filepath_pdf, bbox_inches='tight')
plt.show(filepath_pdf)
