"""Plot the reward Figure."""
# Figure 3.10

import math
import matplotlib.pyplot as plt
import numpy as np

fontsize_large = 32
fontsize_small = 28
line_width = 2

# Parameters
reward_factor = 0.00025
distance = np.linspace(-2.5, 2.5, 1000)
reward = 3*(distance)**3*reward_factor

fig = plt.figure(figsize=(20, 10))

ax1 = plt.subplot(111)
ax1.set_xlabel('Distance to middle [m]', fontsize=fontsize_large)
ax1.set_ylabel('Reward', fontsize=fontsize_large)
plt.xlim(-2.7, 2.7)
plt.ylim(-0.015, 0.015)
plt.xticks(np.arange(-2.5, 3.0, 0.5), fontsize=fontsize_small)
plt.yticks(fontsize=fontsize_small)
plt.grid(linestyle=':')
plt.plot(distance, reward, color='b', label='Reward right', lw=line_width)
plt.plot(distance, -reward, color='g', label='Reward left', lw=line_width)
plt.axvline(x=2.54, color='0.75', label='Wall', linewidth=20)
plt.axvline(x=-2.54, color='0.75', linewidth=20)
plt.axvline(x=2.3, linestyle='--', color='r', label='Reset distance', lw=line_width)
plt.axvline(x=-2.3, linestyle='--', color='r', lw=line_width)
# plt.axhline(y=0., linewidth=0.5, linestyle='-', color='k')
plt.legend(loc='upper center', fontsize=fontsize_large)

fig.tight_layout()

filename = "reward.pdf"
filepath = "./figures/" + filename
plt.savefig(filepath, bbox_inches='tight')
plt.show(filepath)
