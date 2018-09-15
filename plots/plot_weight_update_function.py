"""Plot the weight update function Figure."""

import math
import matplotlib.pyplot as plt
import numpy as np

fontsize_large = 32
fontsize_small = 28
line_width = 1

def stdp(t):
    t = float(t)
    tau = 20.0
    if t > 0.:
        return 1.0*math.exp(-t/tau)
    if t <= 0.:
        return -1.0*math.exp(t/tau)

time = [0.1*(x-1000.) for x in range(2000)]
dw = []

for t in time:
	dw.append(stdp(t))

fig = plt.figure(figsize=(10, 5))

ax1 = plt.subplot(111)
ax1.set_xlabel(r'$\Delta t$ [ms]', fontsize=fontsize_large)
ax1.set_ylabel(r'$\Delta w$', fontsize=fontsize_large)
ax1.set_xlim([-100,100])

plt.setp(ax1.get_xticklabels(), fontsize=fontsize_small)
plt.setp(ax1.get_yticklabels(), fontsize=fontsize_small)
plt.grid(linestyle=':')
plt.plot(time, dw, lw=line_width, color='k')

fig.tight_layout()

filename = "weight_update_function.pdf"
filepath = "./figures/" + filename
plt.savefig(filepath, bbox_inches='tight')
plt.show(filepath)
