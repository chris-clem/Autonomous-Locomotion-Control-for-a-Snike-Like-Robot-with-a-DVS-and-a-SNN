"""Plot the weights and reward over steps after a training session."""
# Figure 4.2

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

w_l = np.array(h5f['w_l'], dtype=float)
w_r = np.array(h5f['w_r'], dtype=float)
w_i = np.array(h5f['w_i'], dtype=float)
steps = np.array(h5f['python_steps'], dtype = float)
rewards = np.array(h5f['rewards'], dtype = float)

steps_cumulative = np.zeros(steps.size)

sum = 0
for k in range(steps.size):
    sum += steps[k]
    steps_cumulative[k] = sum

ylabels = ['Weights Left Motor Neuron', 'Weights Right Motor Neuron']

data = [w_l, w_r]

def plt_weights_over_steps(index, ylabel, data):
    ax = plt.subplot(index)
    ax.set_ylabel(ylabel, fontsize=fontsize_large)
    ax.set_xlim(0, 1000)
    ax.set_ylim(-5000, 6000)
    ax.tick_params(axis='both', which='both',
                   direction='in', bottom=True,
                   top=True, left=True, right=True,
                   labelsize=fontsize_small)
    plt.grid(linestyle=':')
    for i in range(data.shape[1]):
        for j in range(data.shape[2]):
            plt.plot(w_i, data[:,i,j], lw=line_width)
    for step_cumulative in steps_cumulative:
        plt.axvline(x=step_cumulative, ls='dashed', color='k', lw=line_width)

fig = plt.figure(figsize=(20, 24))

for i in range(len(data)):
    plt_weights_over_steps(311+i, ylabels[i], data[i])

ax1 = plt.subplot(313)
ax1.set_xlabel('Simulation Time [1 step = 50 ms]', fontsize=fontsize_large)
ax1.set_ylabel('Reward', fontsize=fontsize_large)
ax1.set_xlim(0, 1000)
plt.xticks(fontsize=fontsize_small)
plt.yticks(fontsize=fontsize_small)
plt.grid(linestyle=':')
plt.plot(rewards, lw=line_width)
for step_cumulative in steps_cumulative:
    plt.axvline(x=step_cumulative, ls='dashed', color='k', lw=line_width)

fig.tight_layout()

filename_pdf = params.session + '_' + filename + '_weights_reward_over_steps'
filepath_pdf = "../plots/training/" + filename_pdf + ".pdf"
plt.savefig(filepath_pdf, bbox_inches='tight')
plt.show(filepath_pdf)
