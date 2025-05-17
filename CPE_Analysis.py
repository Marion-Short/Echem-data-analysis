#!/usr/bin/env python
# coding: utf-8

# CPE Analysis
# doc and fig label as input, figure and charge as output
def CPE_Analysis(doc, fig_label):
    with open(doc, 'r') as text:
        lines = text.read()
    line_list = lines.splitlines()

    #find the index for the line that starts with 'primary_data' and the data starts 3 lines after that
    for index, line in enumerate(line_list):
        if 'primary_data' in line:
            start = index + 3
    data = line_list[start:]

    #split each string into a list of strings, with space delimiter
    list_of_lists = [s.split(' ') for s in data]
    
    import pandas as pd
    df = pd.DataFrame(list_of_lists)
    
    df.drop([1, 3], axis=1, inplace=True)
    df.dropna(axis=0, inplace=True)
    import numpy as np
    df.replace('', np.nan, inplace=True)
    
    df = df.astype(float)
    # col1: time (s), col2: current (A), col3: potential (V vs AgAg/Cl)
    time_interval1 = df.iloc[0,0]
    df[4] = df[2] * time_interval1
    df[5] = df[4].cumsum() # charge
    df[0] = df[0] / 60 # minutes
    df[2] = (df[2] * 1000) / 0.19 #current density mA cm-2
    
    charge = df.iloc[-1, 3] # cumulative charge (python order, so 3rd column)
    
    # plotting
    import matplotlib.pyplot as plt
    plt.rcParams["font.family"] = "arial"
    fig = plt.figure(fig_label, figsize=(4, 4), linewidth=2)
    ax = fig.add_subplot(1, 1, 1)

    ax.plot(df[0],df[2],linewidth=2, color ='slateblue')

    # Adding labels, title, and custom x-axis tick labels
    ax.set_xlabel('$\it{t}$ (min)', fontsize=14)
    ax.set_ylabel('$\it{J}$ (mA cm$^{-2}$)', fontsize=14)
    ax.tick_params(axis='x', width=2, labelsize=14)
    ax.tick_params(axis='y', direction='out', width=2, labelsize=14, length=5, right=False)

    #Set axis linewidths
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(2)
    fig.tight_layout()
    
    return fig, charge

