"""Plot the snn input sample Figure."""

import numpy as np
import matplotlib.pyplot as plt

im = np.flipud(np.array([[15, 65, 0, 0,  7],
                         [9, 40, 0, 7,  0],
                         [5, 41, 20,  2,  0],
                         [0,  0,  0,  0,  0],
                         [0,  0,  0,  0,  0],
                         [0, 43, 0,  0,  0],
                         [3, 44, 15, 0,  0],
                         [10, 63, 0, 8, 0]]).T)

fig = plt.figure(figsize=(20, 10))
plt.imshow(im, alpha=0.5, interpolation='nearest')
plt.axis('off')

fig.tight_layout()

filename = "snn_input_sample.pdf"
filepath = "./figures/" + filename
plt.savefig(filepath, bbox_inches='tight')
plt.show(filepath)
