"""Communicates with V-REP."""

import math
import numpy as np
from numpy.linalg import norm
import rospy
from std_msgs.msg import Int8MultiArray, Float32, Bool, String, Float32MultiArray
from geometry_msgs.msg import Transform
import sys
import time

import parameters as params

# Because ROS isn't installed with Anaconda
sys.path.append('/usr/lib/python2.7/dist-packages')


class VrepEnvironment():
    """Includes everything necessary to communicate with V-REP."""

    def __init__(self):
        """Inits class VrepEnvironment with parameters from parameter.py."""

        # Set up ROS Subscriber and Publisher
        # DVS data Subscriber
        self.dvs_sub = rospy.Subscriber('dvsData',
                                        Int8MultiArray,
                                        self.dvs_callback)
        self.dvs_data = np.array([0, 0])
        self.resize_factor = [params.dvs_resolution[0]//params.resolution[0],
                              (params.dvs_resolution[1]
                               - params.crop_bottom
                               - params.crop_top)
                              //params.resolution[1]]

        # Position data Subscriber
        self.pos_sub = rospy.Subscriber('transformData',
                                        Transform,
                                        self.pos_callback)
        self.pos_data = []

        # Distances Subscriber
        self.distances_sub = rospy.Subscriber('distances',
                                              Float32MultiArray,
                                              self.distances_callback)
        self.distances = []

        # Travelled distance Subscriber
        self.travelled_distance_sub = rospy.Subscriber('travelledDistance',
                                                       Float32,
                                                       self.travelled_distance_callback)
        self.travelled_distances = []

        # V-REP steps Subscriber
        self.steps_sub = rospy.Subscriber('steps',
                                          Float32,
                                          self.steps_callback)
        self.vrep_steps = []

        # Reset Publisher
        self.reset_pub = rospy.Publisher('resetRobot', Bool, queue_size=1)

        # Radius Publisher
        self.radius_pub = rospy.Publisher('turningRadius', Float32, queue_size=1)
        self.steps = 0

        # Initialize values for the turning model, distance and reward calculation
        self.turn_pre = params.turn_pre
        self.radius = 0
        self.radius_buffer = 0

        self.distance = 0

        self.reward = 0
        self.state = []

        if params.maze == 'zig_zag':
            self.positive_direction = True
        else:
            self.positive_direction = False

        self.terminate = False

        # Initialize ROS node
        rospy.init_node('rstdp_controller')
        self.rate = rospy.Rate(params.rate)

    def dvs_callback(self, msg):
        """Store incoming DVS data."""
        self.dvs_data = msg.data
        return

    def pos_callback(self, msg):
        """Store incoming position data."""
        self.pos_data = np.array([msg.translation.x, msg.translation.y])
        return

    def distances_callback(self, msg):
        """Store incoming distances to inner and outer wall."""
        self.distances = msg.data
        return

    def travelled_distance_callback(self, msg):
        """Store incoming travelled distance."""
        self.travelled_distances.append(msg.data)
        return

    def steps_callback(self, msg):
        """Store incoming vrep_steps."""
        self.vrep_steps.append(msg.data)
        return

    def reset(self):
        """Reset the model after an episode terminated."""

        self.radius_pub.publish(0.0)
        self.turn_pre = 0.0

        # Change starting direction
        if params.maze != 'zig_zag':
            self.positive_direction = not self.positive_direction

        # Publish travel direction
        self.reset_pub.publish(Bool(self.positive_direction))
        time.sleep(1)

        # Return initial state and reward
        return np.zeros((params.resolution[0], params.resolution[1]), dtype=int), 0.

    def calculate_and_publish_radius(self, n_l, n_r):
        """Calculates the values for the snake turning model."""
        # Normalize left and right output spikes
        m_l = n_l/params.n_max
        m_r = n_r/params.n_max
        # Calculate steering angle
        a = m_r - m_l
        # Calculate c
        c = math.sqrt((m_l**2 + m_r**2)/2.0)

        # Smooth turn_pre
        self.turn_pre = c*a + (1-c)*self.turn_pre

        # Calculate the radius
        if abs(self.turn_pre) < 0.001:
            self.radius = 0
        else:
            self.radius = params.r_min/self.turn_pre

        # Publish mean turning radius every 5 steps
        if (self.steps % 5 != 0):
            self.radius_buffer = self.radius_buffer + self.radius
        else:
            self.radius = self.radius_buffer/5
            self.radius_buffer = 0

        self.radius_pub.publish(self.radius)
        self.rate.sleep()

        return a, c

    def calculate_reward(self, distance):
        """Calculates the reward value."""
        return 3*(distance)**3*params.reward_factor

    def step(self, n_l, n_r):
        """Performs all necessary steps."""
        # Increment steps
        self.steps += 1

        # Snake turning model
        a, c = self.calculate_and_publish_radius(n_l, n_r)

        # Calculate distance to center
        self.distance = params.maze_width/2 - self.distances[0]

        # Set reward signal
        if self.positive_direction is True:
            self.reward = self.calculate_reward(self.distance)
        else:
            self.reward = -self.calculate_reward(self.distance)

        # Resize DVS frame
        self.state = self.getState()

        # Reset conditions
        # Condition 1: distance to middle greater than reset_distance
        if (abs(self.distance) > params.reset_distance):
            print "reset_distance reached: ", abs(self.distance)
            self.terminate = True

        # Condition 2: Starting area/ End of maze reached
        if params.maze == 'eight':
            # Condition 2 for eight-shaped maze
            # Boundaries of starting area
            top_condition = self.pos_data[1] < 7.5
            bottom_condition = self.pos_data[1] > 2.5
            left_condition = self.pos_data[0] > -1
            right_condition = self.pos_data[0] < 1

            if (self.steps > params.reset_steps and
                left_condition and
                right_condition and
                bottom_condition and
                top_condition):
                print "starting area reached"
                self.terminate = True
        elif params.maze == 'zig_zag':
            # Condition 2 for zig-zag-shaped maze
            if (self.pos_data[0] > 147.0):
                print "End of maze reached: ", self.pos_data[0], self.steps
                self.terminate = True
        elif params.maze == 'cross':
            # Condition 2 for cross-shaped maze
            # Boundaries of starting area
            top_condition = self.pos_data[1] < 2.5
            bottom_condition = self.pos_data[1] > -2.5
            left_condition = self.pos_data[0] > -0.5
            right_condition = self.pos_data[0] < 0.5

            if (self.steps > params.reset_steps and
                left_condition and
                right_condition and
                bottom_condition and
                top_condition):
                print "starting area reached, steps: ", self.steps
                self.terminate = True
        else:
            raise ValueError('Wrong maze selected')

        t = self.terminate
        n = self.steps

        # Check if a reset condition was met
        if t is True:
            self.steps = 0
            self.reset()
            self.terminate = False

        # Return state, distance, pos_data, reward, terminate, steps,
        # travelled_distances, vrep_steps
        return (self.state, self.distance, self.pos_data, self.reward, t, n,
                self.travelled_distances, self.vrep_steps)

    def getState(self):
        """Preprocesses the DVS data."""
        new_state = np.zeros((params.resolution[0], params.resolution[1]), dtype=int)
        for i in range(len(self.dvs_data)//2):
            try:
                if params.crop_bottom <= self.dvs_data[i*2+1] < (params.dvs_resolution[1]-params.crop_top):
                    idx = ((self.dvs_data[i*2])//self.resize_factor[0],
                           (self.dvs_data[i*2+1]-params.crop_bottom)//self.resize_factor[1])
                    new_state[idx] += 1
            except:
                pass
        return new_state
