"""Execute the necessary steps to train a SNN."""

import h5py
import json
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
        params.train_on = scenario

        if scenario in params.scenarios_eight:
            params.maze = 'eight'
        elif scenario in params.scenarios_cross:
            params.maze = 'cross'
        else:
            params.maze = 'zig_zag'
    else:
        sys.exit("Scenario doesn't exist")

# Filepaths for storing data
filename = "training_" + params.train_on
filepath = "../data/" + params.session + '/' + filename

# Create folder if it doesn't exist
if not os.path.exists("../data/" + params.session + '/'):
    os.makedirs("../data/" + params.session + '/')

# Start roscore and vrep with scenario
path_to_scenario = '~/Documents/bachelor-thesis/Autonomous-Locomotion-Control-for-a-Snike-Like-Robot-with-a-DVS-and-a-SNN/V-REP_scenarios/' + params.train_on + '.ttt'
subprocess.call(["../roscore_vrep.sh", path_to_scenario])
time.sleep(5)

# Arrays for storing the training data
weights_l = []
weights_r = []
weights_i = []
distances = []
positions = []
rewards = []
steps = []
python_steps = []
parameters = {}
terminate_early = False

def handler(signum, frane):
    """Handles CTRL-C to terminate the session early."""
    global terminate_early
    terminate_early = True

signal.signal(signal.SIGINT, handler)

# Create SNN and Environment objects
snn = net.SpikingNeuralNetwork()
env = env.VrepEnvironment()

# Initialize environment, get initial state and reward
state, reward = env.reset()

# Simulate for training_length steps
for i in range(params.training_length):

    # Run network for 50 ms: Get left and right output spikes, get weights
    n_l, n_r, weights = snn.simulate(state, reward)
    w_l = weights[0]
    w_r = weights[1]

    # Perform a step
    # Get state, distance, pos_data, reward, terminate, steps,
    # travelled_distances, vrep_steps
    (state, distance, pos_data, reward, t, step,
     travelled_distances, vrep_steps) = env.step(n_l, n_r)

    # Save weights every 100 simulation steps
    if i % 100 == 0:
        weights_l.append(w_l)
        weights_r.append(w_r)
        weights_i.append(i)

    # Store distance, position, reward, step
    distances.append(distance)
    positions.append(pos_data)
    rewards.append(reward)
    steps.append(step)

    # Save # steps after the training resets
    if t:
        python_steps.append(step)
        # Print training information to the console
        print "step:\t", i
        print "python_steps:\n", python_steps
        print "vrep_steps:\n", vrep_steps
        print "travelled_distances:\n", travelled_distances

    # Break if CTRL-C
    if terminate_early:
        break

# Save training parameters as a json
try:
    print "saving params"
    parameters = params.params_dict
    print parameters
    # Save to single json file
    json_data = json.dumps(parameters, indent=4, sort_keys=True)
    print "converted to json"
    with open(filepath + '.json', 'w') as file:
        file.write(json_data)
except:
    print "saving parameters failed"
    pass

# Save training data as h5f
h5f = h5py.File(filepath + '.h5', 'w')
h5f.create_dataset('w_l', data=weights_l)
h5f.create_dataset('w_r', data=weights_r)
h5f.create_dataset('w_i', data=weights_i)
h5f.create_dataset('distances', data=distances)
h5f.create_dataset('positions', data=positions)
h5f.create_dataset('rewards', data=rewards)
h5f.create_dataset('steps', data=steps)
h5f.create_dataset('python_steps', data=python_steps)
h5f.create_dataset('vrep_steps', data=vrep_steps)
h5f.create_dataset('travelled_distances', data=travelled_distances)
h5f.close()
