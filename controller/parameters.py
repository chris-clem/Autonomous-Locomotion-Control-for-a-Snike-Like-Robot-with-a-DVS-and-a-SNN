"""Saves all simulation parameters in one place."""

# Session to store/ load weights in case of training/ testing
session = "session_001"
train_on = "scenario_eight_2_0"
test_on = "scenario_zig_zag_smooth"
# Select maze to train/ test on: eight, zig_zag, cross for reset condition in environment
maze = 'zig_zag'
# Add the scenario the controller is tested on
comment = "Final Parameters"


# Other
training_length = 15000
testing_length = 5000
maze_width = 5.0
reset_distance = 2.3
reset_steps = 500
# ROS publication rate motor speed
rate = 20.

# SNN Input
dvs_resolution = [128, 128]
crop_top = 0
crop_bottom = 48
# SNN Input Resolution = # input neurons
resolution = [dvs_resolution[0]/8,
              (dvs_resolution[1]-crop_top-crop_bottom)/8]

# Network Simulation (time values in ms)
sim_time = 50.0
t_refrac = 2.
time_resolution = 0.1
iaf_params = {}
iaf_params_hidden = {}
poisson_params = {}
# Max. Poisson Neuron Firing Frequency
max_poisson_freq = 300.
# # DVS Events for Max. Poisson Neuron Firing Frequency
max_spikes = 15.

# R-STDP parameters
# Maximum Synapse Value
w_max = 10000.
# Minimum Synapse Value
w_min = -w_max
# Maximum Initial Random Synapse Value
w0_max = 201.
# Minimum Initial Random Synapse Value
w0_min = 200.
# Time Constant of Reward Signal
tau_n = 200.
# Time Constant of Eligibility Trace
tau_c = 1000.
# Reward Factor scaling the Reward Signal
reward_factor = 0.00025
# Constant scaling Strength of Potentiation
A_plus = 1.
# Constant scaling Strength of Depression
A_minus = 1.

# Snake Turning Model
turn_pre = 0.
# Maximum Input Activity
n_max = sim_time//t_refrac
# Minimum Turning Radius
r_min = 2.

# For creating the json with the parameters
params_dict = {}
params_dict.update({k:v for k,v in locals().copy().iteritems()
                    if k[:2] != '__'
                    and k != 'params_dict'
                    and k != 'np'
                    and k!= 'path'
                    and k != 'math'})
