"""Convert hdf5 testing data to csv."""

import h5py
import numpy as np
import pandas as pd

import parameters as params

# Load the testing data
filename = "testing_" + params.test_on
filepath = "../data/" + params.session + '/' + filename
h5f = h5py.File(filepath + '.h5', 'r')

distances = np.array(h5f['distances'], dtype=float)
positions = np.array(h5f['positions'], dtype=float)
rewards = np.array(h5f['rewards'], dtype=float)
steps = np.array(h5f['steps'], dtype=float)

vrep_steps = np.array(h5f['vrep_steps'], dtype=float)
travelled_distances = np.array(h5f['travelled_distances'], dtype=float)

df_1 = pd.DataFrame(data=np.array([distances, positions[:,0], positions[:,1], rewards, steps]).T,
                    columns=['distances', 'positions[0]', 'positions[1]','rewards', 'steps'])

df_2 = pd.DataFrame(data=np.array([vrep_steps, travelled_distances]).T,
                    columns=['vrep_steps', 'travelled_distances'])

df_1.to_csv(path_or_buf=filepath + "_df_1.csv")
df_2.to_csv(path_or_buf=filepath + "_df_2.csv")
