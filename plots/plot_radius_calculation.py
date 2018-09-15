"""Plot the radius calculation Figure."""

import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.gridspec as gridspec
import numpy as np

fontsize_large = 32
fontsize_small = 28
line_width_thick = 2
line_width_thin = 2

t_end = 25
time_step = [x for x in range(0, t_end, 1)]

n_l = [0 for x in range(0, t_end, 1)]
n_r = [0 for x in range(0, t_end, 1)]
m_l = [0 for x in range(0, t_end, 1)]
m_r = [0 for x in range(0, t_end, 1)]
a = [0 for x in range(0, t_end, 1)]
c = [0 for x in range(0, t_end, 1)]
turn_pre_new_array = [0 for x in range(0, t_end, 1)]
radius_array = [0 for x in range(0, t_end, 1)]

n_max = 25.
turn_pre_old = 0.
turn_pre_new = 0.
r_min = 2.

def output_spikes(t):
    delta_t = 1

    n_l = 0 + 1*(t/delta_t)
    n_r = 25 - 1*(t/delta_t)

    return n_l, n_r

def radius(t):
    global turn_pre_old
    global turn_pre_new

    n_l, n_r = output_spikes(t)

    m_l = n_l/n_max
    m_r = n_r/n_max
    a = m_r - m_l
    c = math.sqrt((m_l**2 + m_r**2)/2.0)
    turn_pre_old = turn_pre_new
    turn_pre_new = c*a + (1-c)*turn_pre_old

    if abs(turn_pre_new) < 0.001:
        radius = 0
    else:
        radius = r_min/(turn_pre_new)

    return n_l, n_r, m_l, m_r, a, c, turn_pre_new, radius

for t in range(0, t_end):
    n_l[t], n_r[t], m_l[t], m_r[t], a[t], c[t], turn_pre_new_array[t], radius_array[t]  = radius(t)

nrows = 4
ncols = 1

fig, axes = plt.subplots(nrows, ncols, figsize=(20, 5*(nrows+1)), sharex=True)

gs = gridspec.GridSpec(nrows=nrows,
                       ncols=ncols,
                       height_ratios=[1, 1, 1, 2])

axes = []
for i in range(nrows*ncols):
    axes.append(plt.subplot(gs[i]))

axes[0].set_ylim(-1, 26)
axes[0].plot(time_step, n_l, lw=line_width_thick, label='$n_l(t)$')
axes[0].plot(time_step, n_r, lw=line_width_thick, label='$n_r(t)$')

axes[1].set_ylim(-1.1, 1.1)
axes[1].plot(time_step, m_l, lw=line_width_thick,label='$m_l(t)$')
axes[1].plot(time_step, m_r, lw=line_width_thick, label='$m_r(t)$')
axes[1].plot(time_step, a, lw=line_width_thick, label='$a(t)$')

axes[2].set_ylim(-1.1, 1.1)
axes[2].plot(time_step, c, lw=line_width_thick, label='$c(t)$')
axes[2].plot(time_step, turn_pre_new_array, lw=line_width_thick, label='$turn_{pre}(t)$')

axes[3].set_ylim(min(radius_array)-1, max(radius_array)+1)
axes[3].set_xlabel('steps', fontsize=fontsize_large)
axes[3].plot(time_step, radius_array, lw=line_width_thick, label='$radius(t)$', color='k')

for ax in axes:
    ax.tick_params(labelsize=fontsize_small)
    ax.legend(loc='best', fontsize=fontsize_large)
    ax.grid()

fig.tight_layout()

filename = "radius_calculation.pdf"
filepath = "./figures/" + filename
plt.savefig(filepath, bbox_inches='tight')
plt.show(filepath)
