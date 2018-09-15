"""Plot the snake positions in the cross-shaped maze."""

import math
import matplotlib.pylab as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import numpy as np
import pandas as pd

import parameters as params

# Select the angle: 110, 105, 100, 95
alpha_deg_array = [110, 105, 100, 95]
# Select the color for the plot: 110 b, 105 g, 100 r, 95 c
colors = ['b', 'g', 'r', 'c']

fontsize_large = 32
fontsize_small = 28
line_width = 4

# Parameters for path point calculation
length = 10.0
width = 5.0

# Functions for path point calculation
def deg_to_rad(angle_deg):
    angle_rad = angle_deg*math.pi/180.0
    return angle_rad

def cos_length(length, angle_deg):
    angle_rad = deg_to_rad(angle_deg)
    cos_length = length*math.cos(angle_rad)
    return cos_length

def sin_length(length, angle_deg):
    angle_rad = deg_to_rad(angle_deg)
    sin_length = length*math.sin(angle_rad)
    return sin_length

def mirror_x(points):
    points_mirrored_x = []
    for point in points:
        points_mirrored_x.append([point[0], -point[1]])
    points_mirrored_x.reverse()
    return points_mirrored_x

def mirror_y(points):
    points_mirrored_y = []
    for point in points:
        points_mirrored_y.append([-point[0], point[1]])
    points_mirrored_y.reverse()
    return points_mirrored_y

def mirror_x_y(points):
    points_mirrored_x = mirror_x(points)
    points = points + points_mirrored_x
    points_mirrored_y = mirror_y(points)
    points = points + points_mirrored_y
    return points

def shift_y(points, delta_y):
    points_shifted_y = []
    for point in points:
        points_shifted_y.append([point[0], point[1] + delta_y])
    return points_shifted_y

def print_points(points):
    for i in range(len(points)):
        print points[i]

# Functions for plotting the path
def points_to_tuple(points):
    tuples = []
    for i in range(len(points)):
        tuples.append(tuple(points[i]))
    return tuples

def create_patch_from_points(points, linestyle='dotted'):
    # Will be ignored, is need for CLOSEPOLY
    points.append([0,0])

    verts = points_to_tuple(points)
    nverts = len(verts)
    codes = np.ones(nverts, int) * Path.LINETO
    codes[0] = Path.MOVETO
    codes[-1] = Path.CLOSEPOLY

    path = Path(verts, codes)

    patch = patches.PathPatch(path, linestyle=linestyle, facecolor='none', lw=line_width*2)

    return patch

def plot_patches(patches, xlims, ylims):

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)
    ax.set_xlim(xlims[0], xlims[1])
    ax.set_ylim(ylims[0], ylims[1])

    for patch in patches:
        ax.add_patch(patch)

    filename = "scenario_cross_" + str(alpha_deg) + ".pdf"
    filepath = "/home/christoph/Pictures/" + filename
    plt.savefig(filepath_pdf, bbox_inches='tight')
    plt.show(filepath)

    return

# Functions for plotting snake pos_data
# Create dfs from csv files with snake testing data
def csv_to_df(alpha_deg):
    filename = "testing_scenario_cross_" + str(alpha_deg) + "_df_1.csv"
    filepath = '../data/' + params.session + '/' + filename
    df = pd.DataFrame.from_csv(filepath)

    steps = []
    for index, row in df.iterrows():
        if (row['steps'] == 1.0):
            steps.append(index)

    df = df[steps[0]:steps[1]]
    df = df.reset_index(drop=True)

    return df

def plot_df(df, patch, xlims, ylims, color, alpha_deg):
    fig = plt.figure(figsize=(20, 20))
    ax = fig.add_subplot(111)
    ax.set_xlim(xlims[0], xlims[1])
    ax.set_ylim(ylims[0], ylims[1])
    ax.tick_params(labelsize=fontsize_large*2)

    ax.add_patch(patch)
    plt.plot(df['positions[0]'],
             df['positions[1]'],
             color=color,
             lw=line_width*2)

    fig.tight_layout()

    filename_pdf = params.session + "_testing_positions_scenario_cross_" + str(alpha_deg) + ".pdf"
    filepath_pdf = "../plots/testing/" + filename_pdf
    plt.savefig(filepath_pdf, bbox_inches='tight')
    plt.show(filepath_pdf)

for i in range(len(alpha_deg_array)):
    # Path points calculation
    p01 = [length/2 + cos_length(length, (180-alpha_deg_array[i])),
           length/2 + cos_length(length, (180-alpha_deg_array[i]))]

    p00 = [length/2,
           p01[1] + sin_length(length, (180-alpha_deg_array[i]))]

    p02 = [p01[0] + sin_length(length, (180-alpha_deg_array[i])),
           length/2]

    points_00_02 = [p00, p01, p02]
    points_00_11 = mirror_x_y(points_00_02)
    points_00_11 = shift_y(points_00_11, p00[1])

    # print_points(points_00_11)

    # Plot path points
    patch_middle = create_patch_from_points(points_00_11)
    # patches = [patch_middle]
    # plot_patches(patches, [-20, 20], [-5, 40])

    # Plot snake pos_data
    df = csv_to_df(alpha_deg_array[i])
    plot_df(df, patch_middle, [-19, 19], [-1, 36], colors[i], alpha_deg_array[i])
