"""Execute the necessary steps to run a trained SNN."""

import h5py
import json
import numpy as np
import os
import signal
import subprocess
import sys
import time

import environment as env
import network as net
import parameters as params

# Read session as command line argument
if len(sys.argv) == 2:
    scenario = sys.argv[1]

    if scenario in params.scenarios:
        params.test_on = scenario

        if scenario in params.scenarios_eight:
            params.maze = 'eight'
        elif scenario in params.scenarios_cross:
            params.maze = 'cross'
        else:
            params.maze = 'zig_zag'
    else:
        sys.exit("Scenario doesn't exist")

# Filepaths for storing data
filename_test_data = "testing_" + params.test_on
filepath_test_data = "../data/" + params.session + '/' + filename_test_data

# Create folder if it doesn't exist
if not os.path.exists("../data/" + params.session + '/'):
    os.makedirs("../data/" + params.session + '/')

# Start roscore and vrep with scenario
path_to_scenario = '~/Documents/bachelor-thesis/Autonomous-Locomotion-Control-for-a-Snike-Like-Robot-with-a-DVS-and-a-SNN/V-REP_scenarios/' + params.train_on + '.ttt'
subprocess.call(["../roscore_vrep.sh", path_to_scenario])
time.sleep(5)

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
