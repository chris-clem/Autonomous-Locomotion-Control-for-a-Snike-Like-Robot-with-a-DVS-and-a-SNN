"""Execute the necessary steps to run a trained SNN."""

import h5py
import json
import numpy as np
import signal

import environment as env
import network as net
import parameters as params

# Filepaths for storing data
filename_test_data = "testing_" + params.test_on
filepath_test_data = "../data/" + params.session + '/' + filename_test_data

# Arrays for storing the performance data
distances = []
positions = []
rewards = []
steps = []
terminate_positions = []
travelled_distances = []
vrep_steps = []
terminate_early = False


def handler(signum, frane):
    """Handles CTRL-C to terminate the session early."""
    global terminate_early
    terminate_early = True

signal.signal(signal.SIGINT, handler)

# Create SNN and Environment objects
snn = net.SpikingNeuralNetwork()
env = env.VrepEnvironment()

# Read network weights
# Filepaths for storing data
filename_train_data = "training_" + params.train_on
filepath_train_data = "../data/" + params.session + '/' + filename_train_data
h5f = h5py.File(filepath_train_data + '.h5', 'r')
w_l = np.array(h5f['w_l'], dtype=float)[-1]
w_r = np.array(h5f['w_r'], dtype=float)[-1]

# Set network weights
snn.set_weights(w_l, w_r)

# Initialize environment, get initial state and reward
state, reward = env.reset()

# Simulate for testing_length steps
for i in range(params.testing_length):

    # Run network for 50 ms: Get left and right output spikes
    n_l, n_r = snn.run(state)

    # Perform a step
    # Get state, distance, pos_data, reward, terminate, steps,
    # travelled_distances, vrep_steps
    (state, distance, pos_data, reward, t, step,
     travelled_distances, vrep_steps) = env.step(n_l, n_r)

    # Store distance, position, reward, step
    distances.append(distance)
    positions.append(pos_data)
    rewards.append(reward)
    steps.append(step)

    # Break if CTRL-C
    if terminate_early:
        break

# Save performance data
h5f = h5py.File(filepath_test_data + '.h5', 'w')
h5f.create_dataset('distances', data=distances)
h5f.create_dataset('positions', data=positions)
h5f.create_dataset('rewards', data=rewards)
h5f.create_dataset('steps', data=steps)
h5f.create_dataset('travelled_distances', data=travelled_distances)
h5f.create_dataset('vrep_steps', data=vrep_steps)
h5f.close()
