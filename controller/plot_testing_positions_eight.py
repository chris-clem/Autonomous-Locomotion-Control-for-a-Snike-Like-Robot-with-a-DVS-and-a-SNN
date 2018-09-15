"""Plot the snake positions in the eight-shaped maze."""

import math
import matplotlib.pylab as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import numpy as np
import pandas as pd

import parameters as params

fontsize_large = 34
fontsize_small = 30
line_width = 4

# Parameters for path point calculation
length = 10.0
width = 5.0
alpha_deg = 45.0
alpha_rad = alpha_deg*math.pi/180.0
cos_length = length*math.cos(alpha_rad)
sin_length = length*math.sin(alpha_rad)

# Parameter for wall point calculation
x = (width/2.0)/math.tan(((180-alpha_deg)/2)*math.pi/180.0)

# Parameters for snake pos_data plot
scenarios = [
             'scenario_eight_0_5',
             'scenario_eight_1_0',
             'scenario_eight_1_5',
             'scenario_eight_2_0',
             'scenario_eight_2_5',
             'scenario_eight_3_0'
            ]
colors = ['b', 'g', 'r', 'c', 'm', 'y']

# Functions for path point calculation
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

def print_points(points):
    for i in range(len(points)):
        print points[i]

# Functions for plotting the path
def points_to_tuple(points):
    tuples = []
    for i in range(len(points)):
        tuples.append(tuple(points[i]))
    return tuples

def create_patch_from_points(points, linestyle='dashed'):
    # Will be ignored, is need for CLOSEPOLY
    points.append([0,0])

    verts = points_to_tuple(points)
    nverts = len(verts)
    codes = np.ones(nverts, int) * Path.LINETO
    codes[0] = Path.MOVETO
    codes[-1] = Path.CLOSEPOLY

    path = Path(verts, codes)

    patch = patches.PathPatch(path, linestyle=linestyle, facecolor='none', lw=line_width)

    return patch

def plot_patches(patches, xlim, ylim):

    fig = plt.figure(figsize=(xlim, ylim), frameon=False)
    ax = fig.add_subplot(111)
    ax.set_axis_off()

    for patch in patches:
        ax.add_patch(patch)

    ax.set_xlim(-xlim, xlim)
    ax.set_ylim(-ylim, ylim)

    filename = "scenario_eight_shaped.pdf"
    filepath = "/home/christoph/Pictures/" + filename
    plt.savefig(filepath, bbox_inches='tight')
    plt.show(filepath)

    return

# Functions for plotting snake pos_data
# Create dfs from csv files with snake testing data
def csv_to_dfs(scenarios):
    # Create filenames from scenarios
    filenames = []
    for scenario in scenarios:
        filenames.append("testing_" + scenario + "_df_1.csv")

    # Create filepaths from filenames
    filepaths = []
    for filename in filenames:
        filepaths.append('../data/' + params.session + '/' + filename)

    # Create DataFrames from filepaths
    dfs = []
    for filepath in filepaths:
        dfs.append(pd.DataFrame.from_csv(filepath))

    # Create steps_array containing indices that mark the beginning of an episode for each df
    steps_array = []
    for df in dfs:
        steps = []
        for index, row in df.iterrows():
            if (row['steps'] == 1.0):
                steps.append(index)
        steps_array.append(steps)

    # Select one succesful episode per df
    for i in range(len(scenarios)):
        dfs[i] = dfs[i][steps_array[i][0]:steps_array[i][1]]
        dfs[i] = dfs[i].reset_index(drop=True)

    return dfs

def plot_df(dfs, patches, xlim, ylim):
    scaling_factor = ylim/20
    fig = plt.figure(figsize=(xlim, ylim))#, frameon=False)
    ax = fig.add_subplot(111)
    # ax.set_axis_off()
    ax.set_xlim(-xlim, xlim)
    ax.set_ylim(-ylim, ylim)
    ax.tick_params(labelsize=fontsize_small*scaling_factor)

    for patch in patches:
        ax.add_patch(patch)

    for i in range(len(scenarios)):
        plt.plot(dfs[i]['positions[0]'],
                 dfs[i]['positions[1]'],
                 color=colors[i],
                 linewidth=line_width*scaling_factor,
                 label=scenarios[i])
    plt.legend(fontsize=fontsize_large*scaling_factor, loc=(0.685, 0.385))

    fig.tight_layout()

    filename_pdf = params.session + "_testing_positions_scenario_eight.pdf"
    filepath_pdf = "../plots/testing/" + filename_pdf
    plt.savefig(filepath_pdf, bbox_inches='tight')
    plt.show(filepath_pdf)

# Path points calculation
p00 = [0.5*length,
       0.5*length]
p01 = [p00[0] + cos_length,
       p00[1] + sin_length]
p02 = [p01[0] + length,
       p01[1] + 0]
p03 = [p02[0] + cos_length,
       p02[1] - sin_length]

points_00_03 = [p00, p01, p02, p03]
points_middle = mirror_x_y(points_00_03)

p16 = [p00[0] - x,
       p00[1] + width/2]
p17 = [p01[0] - x,
       p01[1] + width/2]
p18 = [p02[0] + x,
       p02[1] + width/2]
p19 = [p03[0] + width/2,
       p03[1] + x]

points_16_19 = [p16, p17, p18, p19]
points_outer = mirror_x_y(points_16_19)

p32 = [p00[0] + x,
       p00[1] - width/2]
p33 = [p01[0] + x,
       p01[1] - width/2]
p34 = [p02[0] - x,
       p02[1] - width/2]
p35 = [p03[0] - width/2,
       p03[1] - x]

points_32_35 = [p32, p33, p34, p35]
points_inner = mirror_x_y(points_32_35)

# Plot path points
patch_middle = create_patch_from_points(points_middle, linestyle='dotted')
patch_outer = create_patch_from_points(points_outer, linestyle='solid')
patch_inner = create_patch_from_points(points_inner, linestyle='solid')
patches = [patch_middle, patch_outer, patch_inner]
# plot_patches(patches, p19[0]*1.01, p18[1]*1.01)

# Plot snake pos_data
dfs = csv_to_dfs(scenarios)
plot_df(dfs, patches, p19[0]*1.01, p18[1]*1.01)
