"""Plot the snake positions in the zig-zag-smoothed-shaped maze."""

import math
import matplotlib.pylab as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import numpy as np
import pandas as pd

import parameters as params

fontsize_large = 32
fontsize_small = 28
line_width = 2

filename = 'session_002_2_zig_zag_smooth.csv'

def bezier_csv_to_points(filename_bezier_points):
    filepath = '../V-REP_scenarios/' + filename_bezier_points
    df = pd.read_csv(filepath, header=0, names=['x', 'y'])

    points = []
    for i in range(len(df)):
        points.append([df['x'][i], df['y'][i]])
    return points

def print_points(points):
    for i in range(len(points)):
        print points[i]

def points_to_tuple(points):
    tuples = []
    for i in range(len(points)):
        tuples.append(tuple(points[i]))
    return tuples

def create_patch_from_points(points, linestyle='dotted'):

    verts = points_to_tuple(points)
    nverts = len(verts)
    codes = np.ones(nverts, int) * Path.LINETO
    codes[0] = Path.MOVETO

    path = Path(verts, codes)

    patch = patches.PathPatch(path, linestyle=linestyle, facecolor='none', lw=line_width)

    return patch

def plot_patches(patches, xlim, ylim):

    fig = plt.figure(figsize=(20, 20))
    ax = fig.add_subplot(111)
    ax.set_xlim(-5, xlim)
    ax.set_ylim(-5, ylim)

    for patch in patches:
        ax.add_patch(patch)

    filename = 'scenario_2_zig_zag_smooth.pdf'
    filepath = "/home/christoph/Pictures/" + filename
    plt.savefig(filepath_pdf, bbox_inches='tight')
    plt.show(filepath_pdf)

    return

# Functions for plotting snake pos_data
# Create dfs from csv files with snake testing data
def csv_to_df():
    filename = "testing_scenario_zig_zag_smooth_df_1.csv"
    filepath = '../data/' + params.session + '/' + filename
    df = pd.DataFrame.from_csv(filepath)

    steps = []
    for index, row in df.iterrows():
        if (row['steps'] == 1.0):
            steps.append(index)

    df = df[steps[0]:(steps[1]-1)]
    df = df.reset_index(drop=True)

    return df

def plot_df(df, patch, xlim, ylim):
    fig = plt.figure(figsize=(20, 20))
    ax = fig.add_subplot(111)
    ax.set_xlim(-1, xlim)
    ax.set_ylim(-1, ylim)
    ax.tick_params(labelsize=fontsize_small)

    ax.add_patch(patch)
    plt.plot(df['positions[0]'],
             df['positions[1]'],
             lw=line_width,
             color='g')

    fig.tight_layout()

    filename_pdf = params.session + "_testing_positions_scenario_zig_zag_smooth.pdf"
    filepath_pdf = "../plots/testing/" + filename_pdf
    plt.savefig(filepath_pdf, bbox_inches='tight')
    plt.show(filepath_pdf)

points_middle = bezier_csv_to_points('scenario_zig_zag_smooth.csv')

# print_points(points)
patch_middle = create_patch_from_points(points_middle, linestyle='dotted')
# plot_patches([patch], points[-1][0]*1.1, points[-1][1]*1.1)

# Plot snake pos_data
df = csv_to_df()
plot_df(df, patch_middle, points_middle[-1][0]*1.01, points_middle[-1][1]*1.01)
