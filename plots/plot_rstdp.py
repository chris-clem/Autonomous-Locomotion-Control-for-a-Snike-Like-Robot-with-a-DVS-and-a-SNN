"""Plot the rstdp Figure."""
# Figure 2.5

import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

fontsize_large = 32
fontsize_small = 28
line_width_thick = 2
line_width_thin = 2

# Parameters
A_plus = 1.0
A_minus = 1.0
tau_plus = 20.0
tau_minus = 20.0

# STDP function
def fun_stdp(delta_t):
    if delta_t > 0:
        return A_plus * np.exp(-delta_t/tau_plus)
    else:
        return -A_minus * np.exp(delta_t/tau_minus)


pre_spikes =  [    180, 330, 520, 800]
post_spikes = [70, 220, 350, 500]
spike_event = np.vstack((pre_spikes, post_spikes))

trace = 0.
weight = 0.
steps = 1000.
factor = 0.995
traces = []
weights = []

reward = np.zeros(1000)

for i in range(int(steps)):
    if i < 300:
        reward[i] = 0
    else:
        reward[i] = 1 * np.exp((300-i) * 0.01)

index = 0
for i in range(int(steps)):
    trace = factor * trace
    if i in post_spikes:
        for j in pre_spikes:
            if abs(i-j) < 100:
                print i, j, (i-j)
                trace = trace + fun_stdp(i-j)
    # print trace
    traces.append(trace)

for i in range(int(steps)):
    weight = weight + reward[i] * traces[i]

    weights.append(weight)

fig, ax = plt.subplots(4, 1, figsize=(20, 12))

ax1 = plt.subplot(411)
# Set spike colors for each neuron
lineSize = [0.4, 0.4]
lineOffsets = [1, 0.5]
# Set different colors for each neuron
colorCodes = np.array([[1, 0, 0],
                        [0, 1, 0]])
# Event plot
plt.eventplot(spike_event, color=colorCodes, linelengths=lineSize, lineoffsets=lineOffsets, linewidth=4)
plt.xlim(0, 1000)
plt.setp(ax1.get_xticklabels(), fontsize=fontsize_small)
plt.axhline(y=0.8, lw=line_width_thick, color='k')
plt.axhline(y=0.3, lw=line_width_thick, color='k')
plt.setp(ax1.get_yticklabels(), visible=False)
plt.gcf().text(0.045, 0.83, 'pre\nspikes', fontsize=fontsize_large)
plt.gcf().text(0.045, 0.75, 'post\nspikes', fontsize=fontsize_large)
ax1.add_patch(patches.Rectangle((170, 0.2), 60, 1.1, facecolor='none', edgecolor='black', lw=line_width_thin))
ax1.add_patch(patches.Rectangle((320, 0.2), 40, 1.1, facecolor='none', edgecolor='black', lw=line_width_thin))
ax1.add_patch(patches.Rectangle((490, 0.2), 40, 1.1, facecolor='none', edgecolor='black', lw=line_width_thin))
plt.grid()

ax2 = plt.subplot(412)
plt.plot(range(int(steps)), reward, lw=line_width_thick, color='k')
plt.setp(ax2.get_xticklabels(), fontsize=fontsize_small)
plt.setp(ax2.get_yticklabels(), visible=False)
plt.gcf().text(0.045, 0.57, "reward\nr(t)", rotation=0, multialignment='center', fontsize=fontsize_large)
plt.grid()
# plt.arrow(200, 0.9, 80, -0.5, head_width=0.05, head_length=0.1, fc='k', ec='k')
# ax2.add_patch(patches.FancyArrowPatch((200, 0.9), (280, 0.5), arrowstyle='->', lw=line_width_thick))

ax3 = plt.subplot(413, sharex=ax1)
plt.plot(range(int(steps)), traces, lw=line_width_thick, color='k')
plt.setp(ax3.get_yticklabels(), visible=False)
plt.setp(ax3.get_xticklabels(), fontsize=fontsize_small)
plt.gcf().text(0.020, 0.33, "eligibility\ntrace\nc(t)", rotation=0, multialignment='center', fontsize=fontsize_large)
plt.grid()

ax4 = plt.subplot(414)
plt.plot(range(int(steps)), weights, lw=line_width_thick, color='k')
plt.setp(ax4.get_xticklabels(), fontsize=fontsize_small)
plt.setp(ax4.get_yticklabels(), visible=False)
plt.gcf().text(0.045, 0.17, "weight\nw(t)", rotation=0, multialignment='center', fontsize=fontsize_large)
plt.xlabel('time (ms)', fontsize=fontsize_large)

plt.grid(linestyle=':')

filename = "rstdp.pdf"
filepath = "./figures/" + filename
plt.savefig(filepath, bbox_inches='tight')
plt.show()
