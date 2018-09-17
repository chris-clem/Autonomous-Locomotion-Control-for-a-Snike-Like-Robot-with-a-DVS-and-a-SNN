"""Plot the radius lif Figure."""
# Figure 2.3

import math
import matplotlib.pyplot as plt
import numpy as np

fontsize_large = 24
fontsize_small = 20
line_width_thick = 2
line_width_thin = 2

# First, plot the external input current
t_end = 2000
t_ref = 50
time_ref = 0
alpha = 5
beta = 0.015
spikes_in = [950, 1160, 1190, 1220, 1250, 1280, 1500, 1530, 1560, 1590, 1680]
time_step = [x for x in range(0, t_end, 1)]
ext_current = [0 for x in range(0, t_end, 1)]
synaptic_current = [0 for x in range(0, t_end, 1)]
LIF_output = [0 for x in range(0, t_end, 1)]
spikes_out =[]

def cal_external_input(t):
    t_1 = 100
    t_2 = 200
    t_3 = 350
    t_4 = 700

    if t < t_1:
        ext_i = 0
    elif t_1 <= t <= t_2:
        ext_i = 0.45
    elif t_2 < t < t_3:
        ext_i = 0
    elif t_3 <= t <= t_4:
        ext_i = 0.7
    else:
        ext_i = 0

    return ext_i

def cal_lif_output(t, i):
    global time_ref
    dvdt = -0.05*LIF_output[t-1] + i*0.1
    res = LIF_output[t-1] + dvdt
    if res > 1:
        spikes_out.append(t)
        res = 0
        time_ref = t
    if ((t - time_ref) < t_ref) and (t > t_ref):
        res = 0
    return res

def calcResult(t):
    res = 0.000
    for s in spikes_in:
        if s<=t:
            res += 0.3 * math.exp(beta*(s-t))
    return res

for t in range(0, t_end):
    synaptic_current[t] = calcResult(t)

for t in range(0, t_end):
    ext_current[t] = cal_external_input(t)
    LIF_output[t] = cal_lif_output(t, ext_current[t]+synaptic_current[t])

for t in range(0, t_end):
    LIF_output[t] = LIF_output[t] - 1.5

fig, ax = plt.subplots(figsize=(20, 10))
plt.plot(time_step, ext_current, lw=line_width_thick)
plt.plot(time_step, LIF_output, lw=line_width_thick)
plt.plot(time_step, synaptic_current, lw=line_width_thick)

plt.eventplot(spikes_in, color='k', linelengths=0.2, lineoffsets=1, lw=line_width_thick)
plt.eventplot(spikes_out, color='k', linelengths=0.3, lineoffsets=-2, lw=line_width_thick)

ax.arrow(0, -2.15, 1960, 0, head_width=0.1, head_length=40, fc='k', ec='k')
# ax.arrow(0, -1.6, 1940, 0, head_width=0.1, head_length=60, fc='k', ec='k')
ax.arrow(900, 0.9, 900, 0, head_width=0.1, head_length=40, fc='k', ec='k')
plt.axhline(-0.5, ls='--', c='grey', lw=line_width_thin)
plt.axhline(0, ls='-', c='k', lw=line_width_thick)
plt.axhline(-1.6, ls='-', c='k', lw=line_width_thin)

for s in spikes_in:
    plt.axvline(s, ymin=0.25, ymax=0.9, ls='--', c='grey', lw=line_width_thin)

plt.gcf().text(0.18, 0.85, "external injected current $i_0(t)$", rotation=0, multialignment='center', fontsize=fontsize_large)
plt.gcf().text(0.48, 0.85, "presynaptic spike train & synaptic current $i_j(t)$", rotation=0, multialignment='center', fontsize=fontsize_large)
plt.gcf().text(0.2, 0.52, "LIF membrane potential $u(t)$", rotation=0, multialignment='center', fontsize=fontsize_large)
plt.gcf().text(0.1, 0.5, "$V_{th}$", rotation=0, multialignment='center', fontsize=fontsize_large)
plt.gcf().text(0.085, 0.27, "$V_{reset}$", rotation=0, multialignment='center', fontsize=fontsize_large)
plt.gcf().text(0.42, 0.23, "output spike train", rotation=0, multialignment='center', fontsize=fontsize_large)
plt.gcf().text(0.85, 0.13, "time", rotation=0, multialignment='center', fontsize=fontsize_large)
plt.gcf().text(0.85, 0.13, "time", rotation=0, multialignment='center', fontsize=fontsize_large)
plt.gcf().text(0.15, 0.85, "A.", rotation=0, multialignment='center', fontsize=fontsize_large, fontweight='bold')
plt.gcf().text(0.45, 0.85, "B.", rotation=0, multialignment='center', fontsize=fontsize_large, fontweight='bold')
plt.gcf().text(0.15, 0.52, "C.", rotation=0, multialignment='center', fontsize=fontsize_large, fontweight='bold')
plt.gcf().text(0.15, 0.23, "D.", rotation=0, multialignment='center', fontsize=fontsize_large, fontweight='bold')

plt.setp(ax.get_yticklabels(), visible=False)
plt.setp(ax.get_xticklabels(), visible=False)
plt.subplots_adjust(left=0.125, bottom=0.1, right=0.9, top=0.9,
                wspace=0.2, hspace=0.2)
plt.grid('off')

filename = "lif.pdf"
filepath = "./figures/" + filename
plt.savefig(filepath, bbox_inches='tight')
plt.show()
