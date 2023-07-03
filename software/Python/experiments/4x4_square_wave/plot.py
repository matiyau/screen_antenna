#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 04:40:05 2023.

@author: Nishad Mandlik
"""

from matplotlib import pyplot as plt
import pickle

title_sz = 14
axis_label_sz = 14
axis_ticklabel_maj_sz = 12
axis_ticklabel_min_sz = 10
legend_item_sz = 10
legend_title_sz = 12

with open("log_4_good_tx", "rb") as f:
    df_good = pickle.load(f)
df_good = df_good[(df_good["Time (µs)"] > 650) &
                  (df_good["Time (µs)"] <= 7050)]
df_good = df_good.reset_index(drop=True)
df_good["Time (µs)"] = df_good["Time (µs)"] - df_good["Time (µs)"][0]


with open("log_2_good_2_bad_tx", "rb") as f:
    df_bad = pickle.load(f)
df_bad = df_bad[(df_bad["Time (µs)"] > 2187) &
                (df_bad["Time (µs)"] <= 8587)]
df_bad = df_bad.reset_index(drop=True)
df_bad["Time (µs)"] = df_bad["Time (µs)"] - df_bad["Time (µs)"][0]

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(df_bad["Time (µs)"], df_bad["ADC Reading"], color="red", linewidth=2)
ax.set_xlabel("Time (µs)", fontsize=axis_label_sz)
ax.set_ylabel("Relative ADC Reading", fontsize=axis_label_sz)
ax.tick_params(axis='both', which='major', labelsize=axis_ticklabel_maj_sz)
ax.tick_params(axis="both", which="minor", labelsize=axis_ticklabel_min_sz)
plt.grid(True, which="both")
plt.savefig("many_to_1_2_good_2_bad_samp.svg")

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(df_good["Time (µs)"], df_good["ADC Reading"], color="red", linewidth=2)
ax.set_xlabel("Time (µs)", fontsize=axis_label_sz)
ax.set_ylabel("Relative ADC Reading", fontsize=axis_label_sz)
ax.tick_params(axis='both', which='major', labelsize=axis_ticklabel_maj_sz)
ax.tick_params(axis="both", which="minor", labelsize=axis_ticklabel_min_sz)
plt.grid(True, which="both")
plt.savefig("many_to_1_4_good_samp.svg")
