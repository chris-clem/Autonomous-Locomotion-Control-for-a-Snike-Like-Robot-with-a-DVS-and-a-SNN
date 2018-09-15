"""Convert hdf5 training data to csv."""

import h5py
import numpy as np
import pandas as pd

import parameters as params

# Load the training data
filename = "training_" + params.train_on
filepath = "../data/" + params.session + '/' + filename
h5f = h5py.File(filepath + '.h5', 'r')

distances = np.array(h5f['distances'], dtype=float)
rewards = np.array(h5f['rewards'], dtype=float)
steps = np.array(h5f['steps'], dtype=float)

vrep_steps = np.array(h5f['vrep_steps'], dtype=float)
travelled_distances = np.array(h5f['travelled_distances'], dtype=float)

df_1 = pd.DataFrame(data=np.array([distances, rewards, steps]).T,
                    columns=['distances', 'rewards', 'steps'])
df_2 = pd.DataFrame(data=np.array([vrep_steps, travelled_distances]).T,
                    columns=['vrep_steps', 'travelled_distances'])

df_1.to_csv(path_or_buf=filepath + "_df_1.csv")
df_2.to_csv(path_or_buf=filepath + "_df_2.csv")
