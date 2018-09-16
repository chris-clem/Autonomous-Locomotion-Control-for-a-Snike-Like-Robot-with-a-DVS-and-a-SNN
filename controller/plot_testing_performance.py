"""Plot the perfomance of a controller."""

import math
import matplotlib.pylab as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import matplotlib.gridspec as gridspec
import numpy as np
import pandas as pd

import parameters as params

fontsize_large = 32
fontsize_small = 28
line_width = 2

# Parameters for snake pos_data plot (uncomment the one you want to plot)

if params.maze == 'eight':
    scenarios = [
                 'scenario_eight_0_5',
                 'scenario_eight_1_0',
                 'scenario_eight_1_5',
                 'scenario_eight_2_0',
                 'scenario_eight_2_5',
                 'scenario_eight_3_0'
                ]
    numbers_of_segments = [16]*len(scenarios)
    axvline_factor = 0.5
    filename_pdf = params.session + "_testing_performance_scenario_eight.pdf"
    colors = ['b', 'g', 'r', 'c', 'm', 'y']
elif params.maze == 'zig_zag':
    scenarios = ['scenario_zig_zag', 'scenario_zig_zag_smooth']
    numbers_of_segments = [16, 20]
    axvline_factor = 1.0
    filename_pdf = params.session + "_testing_performance_scenario_zig_zag.pdf"
    colors = ['b', 'g']
elif params.maze == 'cross':
    scenarios = ['scenario_cross_110', 'scenario_cross_105',
                 'scenario_cross_100', 'scenario_cross_95']
    numbers_of_segments = [12]*len(scenarios)
    axvline_factor = 0.5
    filename_pdf = params.session + "_testing_performance_scenario_cross.pdf"
    colors = ['b', 'g', 'r', 'c']
else:
    raise ValueError('Wrong maze selected')

def csv_to_dfs(scenarios):
    """Create dfs from csv files with snake testing data."""
    # Create filenames_1 from scenarios
    filenames_1 = []
    for scenario in scenarios:
        filenames_1.append("testing_" + scenario + "_df_1.csv")
    # Create filenames_2 from scenarios
    filenames_2 = []
    for scenario in scenarios:
        filenames_2.append("testing_" + scenario + "_df_2.csv")

    # Create filepaths_1 from filenames_1
    filepaths_1 = []
    for filename_1 in filenames_1:
        filepaths_1.append('../data/' + params.session + '/' + filename_1)
    # Create filepaths_2 from filenames_2
    filepaths_2 = []
    for filename_2 in filenames_2:
        filepaths_2.append('../data/' + params.session + '/' + filename_2)

    # Create DataFrames from filepaths
    dfs_1 = []
    for filepath_1 in filepaths_1:
        dfs_1.append(pd.read_csv(filepath_1))
    dfs_2 = []
    for filepath_2 in filepaths_2:
        dfs_2.append(pd.read_csv(filepath_2))

    # Create steps_array containing indices that mark the beginning of an episode for each df
    steps_array = []
    for df_1 in dfs_1:
        steps = []
        for index, row in df_1.iterrows():
            if (row['steps'] == 1.0):
                steps.append(index)
        steps_array.append(steps)

    # Select one succesful episode per df
    for i in range(len(scenarios)):
        dfs_1[i] = dfs_1[i][steps_array[i][0]:steps_array[i][1]]
    dfs_1[i] = dfs_1[i].reset_index(drop=True)

    return dfs_1, dfs_2

def plot_controller_performance(dfs_1, dfs_2):
# def plot_controller_performance(dfs_1):
    """Plot the performance."""

    # Calculate error defined as the mean of absolute value of distances per df
    # Calculate error defined as the mean of absolute value of distances per df
    # Add travelled_distances
    means = []
    errors = []
    travelled_distances = []
    # travelled_distances = [160]
    for df_1 in dfs_1:
        means.append(df_1['distances'].mean())
        errors.append(df_1['distances'].abs().mean())
    for df_2 in dfs_2:
        travelled_distances.append(df_2['travelled_distances'].iloc[0])

    axvlines_array = []
    for i in range(len(scenarios)):
        axvlines=[]
        axvlines.append((dfs_1[i]['steps'].iloc[-2]/numbers_of_segments[i])*axvline_factor)
        for j in range(numbers_of_segments[i]-1):
            axvlines.append(axvlines[0] + (j+1)*(dfs_1[i]['steps'].iloc[-2]/numbers_of_segments[i]))

        axvlines_array.append(axvlines)

    nrows = len(scenarios)
    ncols = 2
    # Create figure
    fig = plt.figure(figsize=(20, 4*nrows))

    fig.text(0.06, 0.5,
             'Distance to middle [m]',
             fontsize=fontsize_large,
             va='center',
             rotation='vertical')

    gs = gridspec.GridSpec(nrows=nrows,
                           ncols=ncols,
                           width_ratios=[5,1])

    axes = []
    for i in range(nrows*ncols):
        axes.append(plt.subplot(gs[i]))

    for i in range(len(scenarios)):
        # Distance to center over travelled distance
        j = i*2
        dfs_1[i].plot(x='steps',
                    y='distances',
                    ax=axes[j],
                    color=colors[i],
                    sharex=axes[0],
                    sharey=axes[0],
                    legend=False,
                    lw=line_width)
        axes[j].set_title("Test on " + scenarios[i], fontsize=fontsize_large)
        axes[j].set_xlabel("Simulation Time [1 step = 50 ms]", fontsize=fontsize_large)
        axes[j].set_ylim(-2,2)
        # axes[j].set_xticks(np.arange(0, dfs_1[i]['distances'].iloc[-1], 10))
        axes[j].tick_params(labelsize=fontsize_small)
        axes[j].set_yticks(np.arange(-2, 3, 1))
        for axvline in axvlines_array[i]:
            axes[j].axvline(x=axvline, color='k', linestyle='dashed', lw=line_width)
        axes[j].grid()
        # Histogram
        dfs_1[i]['distances'].plot.hist(ax=axes[j+1],
                                      color=colors[i],
                                      orientation="horizontal",
                                      sharey=axes[j])
        axes[j+1].set_xlabel("Histogram", fontsize=fontsize_large)
        axes[j+1].set_ylim(-2,2)
        axes[j+1].tick_params(labelsize=fontsize_small)
        axes[j+1].set_xticks(np.arange(0, 1500, 500))
        axes[j+1].set_yticks(np.arange(-2, 3, 1))
        axes[j+1].set_title(('mean = ' + str('{:4.3f}'.format(means[i])) + 'm \n'
                             'e = ' + str('{:4.3f}'.format(errors[i])) + 'm \n'
                             + 'Length = ' + str('{:4.2f}'.format(travelled_distances[i])) + 'm'),
                            loc='left',
                            position=(1.1,0.33),
                            fontsize=fontsize_small)
        axes[j+1].grid()

    plt.subplots_adjust(wspace=0.)
    # fig.tight_layout()

    filepath_pdf = "../plots/testing/" + filename_pdf
    plt.savefig(filepath_pdf, bbox_inches='tight')
    plt.show(filepath_pdf)


dfs_1, dfs_2 = csv_to_dfs(scenarios)
plot_controller_performance(dfs_1, dfs_2)
