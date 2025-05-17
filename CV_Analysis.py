#!/usr/bin/env python
# coding: utf-8

# CV analysis
# Input text file and figure label and output figure and charges

def CV_Analysis(doc, fig_label):
    import pandas as pd
    # Open document and save all the lines in a list
    with open(doc, 'r', encoding='latin1') as text:
        lines = text.read()
    line_list = lines.splitlines()

    #find the index for the line that starts with 'primary_data' and the data starts 3 lines after that
    start_indicies = []
    for index, line in enumerate(line_list):
        if 'primary_data' in line:
            start_indicies.append(index)


    end_indicies = []
    for index, line in enumerate(line_list):
        if 'QR=QR' in line:
            end_indicies.append(index)
            
    CV1_start = start_indicies[1] + 3
    CV2_end = end_indicies[2] - 4
    CV1 = line_list[CV1_start:CV2_end]

    CV2_start = start_indicies[2] + 3
    CV2 = line_list[CV2_start:]

    #split each string into a list of strings, with space delimiter
    CV1_lists = [s.split(' ') for s in CV1]
    CV2_lists = [s.split(' ') for s in CV2]
    df1 = pd.DataFrame(CV1_lists)
    df2 = pd.DataFrame(CV2_lists)
    
    df1.drop([2, 3], axis=1, inplace=True)
    df2.drop([2, 3], axis=1, inplace=True)
    df2 = df2.dropna(axis=0)
    
    # Find time interval to calculate charge passed
    E_steps = []
    scanrates = []
    for line in line_list:
        if 'E step' in line:
            E_steps.append(line)
        elif 'Scanrate' in line:
            scanrates.append(line)

    E_chars = E_steps[1].split('=')
    E_step = float(E_chars[1])

    S_chars = scanrates[1].split('=')
    scanrate = float(S_chars[1])

    time_interval = E_step / scanrate
    
    df1 = df1.astype(float)
    df1[2] = df1[1] * time_interval
    df1[3] = df1[2].cumsum()
    df1[1] = (df1[1] * 1000) / 0.19 #current density

    df2 = df2.astype(float)
    df2[2] = df2[1] * time_interval
    df2[3] = df2[2].cumsum()
    df2[1] = (df2[1] * 1000) / 0.19
    
    # Charges passed
    charges = []
    charges.append(df1.iloc[-1, 3])
    charges.append(df2.iloc[-1, 3])
    
    # Plotting
    import matplotlib.pyplot as plt
    plt.rcParams["font.family"] = "arial"
    fig = plt.figure(fig_label, figsize=(4, 4), linewidth=2)
    ax = fig.add_subplot(1, 1, 1)

    ax.plot(df1[0],df1[1],linewidth=2, label='1', color ='slateblue')
    ax.plot(df2[0],df2[1],linewidth=2, label='2', color='purple')

    # Adding labels, title, and custom x-axis tick labels
    ax.set_xlabel('$\it{E}$ (V vs Ag/AgCl)', fontsize=14)
    ax.set_ylabel('$\it{J}$ (mA cm$^{-2}$)', fontsize=14)
    ax.tick_params(axis='x', width=2, labelsize=14)
    ax.tick_params(axis='y', direction='out', width=2, labelsize=14, length=5, right=False)
    ax.legend(fontsize='large', edgecolor='white', framealpha=0, loc='best')#(0.23, 0.9), ncols=2, columnspacing=1.0)

    #Set axis linewidths
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(2)
    fig.tight_layout()
    
    return fig, charges

