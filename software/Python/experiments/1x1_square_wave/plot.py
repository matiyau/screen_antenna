#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 03:20:44 2023.

@author: Nishad Mandlik
"""

from matplotlib import pyplot as plt
import pandas as pd

_LOG_FILENAME = "log_20230130_041159"

# df = pd.read_csv(_LOG_FILENAME + ".csv", index_col=0)

cols = ["red", "green", "blue"]

title_sz = 14
axis_label_sz = 14
axis_ticklabel_maj_sz = 12
axis_ticklabel_min_sz = 10
legend_item_sz = 10
legend_title_sz = 12


for col in cols[:1]:
    px = 1/plt.rcParams['figure.dpi']
    fig = plt.figure(figsize=(640*px, 770.83*px))  # create a figure object
    df = pd.read_csv("log_" + col + "_tx.csv", index_col=0)
    j = 1
    lims = (df["ADC Reading"].min(), df["ADC Reading"].max())
    lims_pad = (lims[1] - lims[0])/10
    lims = (lims[0] - lims_pad, lims[1] + lims_pad)
    for i in [50, 100, 200]:
        ax = fig.add_subplot(3, 1, j)
        j += 1
        df_tmp = df[df["Half-Time (us)"] == i]
        (line, ) = ax.plot(df_tmp["Uptime (us)"], df_tmp["ADC Reading"],
                           color=col, linewidth=2, )
        ax.set_xlabel("Time (μs)", fontsize=axis_label_sz)
        ax.set_ylim(*lims)
        ax.set_ylabel("ADC Reading", fontsize=axis_label_sz)
        ax.set_title("Frequency: %.1fkHz " %
                     ((10**3)/(2*i),), fontsize=title_sz)
        ax.set_xticks([500, 1000, 1500])
        ax.tick_params(axis="both", which="major",
                       labelsize=axis_ticklabel_maj_sz)
        ax.tick_params(axis="both", which="minor",
                       labelsize=axis_ticklabel_min_sz)
        ax.grid(True, which="both")

    plt.subplots_adjust(bottom=0.08, top=0.95, hspace=0.65)
    plt.savefig("square_wave_freq_test.svg")
