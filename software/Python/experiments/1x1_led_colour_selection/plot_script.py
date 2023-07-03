#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 06:34:37 2022

@author: Nishad Mandlik
"""

from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import pandas as pd
from pathlib import Path


title_sz = 14
axis_label_sz = 14
axis_ticklabel_maj_sz = 12
axis_ticklabel_min_sz = 10
legend_item_sz = 10
legend_title_sz = 12

ambient = True

leds = ["Inolux HV-5RGB25", "Kingbright WP154A4SUREQBFZGC",
        "Kingbright WP154A4SEJ3VBDZGC-CA"]

leds_df = {}

for led in leds:
    data_filepath = Path("./plot_data/" + led + " (w amb).csv")
    leds_df[led] = pd.read_csv(data_filepath)

for led in leds[2:]:
    df = leds_df[led]
    df = df[df["Distance (cm)"] <= 30]
    df = df[df["Distance (cm)"] >= 10]
    fig = plt.figure()  # create a figure object
    ax = fig.add_subplot(1, 1, 1)
    for col in df.columns[1:]:
        if not ((col == "Red-Red") or (col == "Green-Red") or
                (col == "Blue-Red") or (col == "Blue-Blue")):
            continue
        (line, ) = ax.plot(df["Distance (cm)"], df[col], linewidth=2)
        line.set_label(col.replace("-", " → "))
    ax.set_xlabel("Distance (cm)", fontsize=axis_label_sz)
    ax.set_ylabel("Rx Voltage (mv)", fontsize=axis_label_sz)
    # ax.set_title(led, fontsize='32')
    ax.set_xticks(np.arange(10, 35, 5))
    ax.tick_params(axis="both", which="major", labelsize=axis_ticklabel_maj_sz)
    ax.tick_params(axis="both", which="minor", labelsize=axis_ticklabel_min_sz)
    ax.legend(fontsize=legend_item_sz)
    plt.grid(True, which="both")
    # plt.subplots_adjust(top=0.93,
    #                     bottom=0.15,
    #                     left=0.11,
    #                     right=0.98,
    #                     hspace=0.2,
    #                     wspace=0.2)
    plt.savefig("init_tests_best_led_best_cols.svg")

fig = plt.figure()  # create a figure object
ax = fig.add_subplot(1, 1, 1)

i = 0
df = leds_df[leds[i]]
df = df[df["Distance (cm)"] <= 30]
df = df[df["Distance (cm)"] >= 10]
for col in df.columns[1:3]:
    (line, ) = ax.plot(df["Distance (cm)"], df[col], linewidth=2)
    line.set_label("LED " + str(i+1) + ": " + col.replace("-", " → "))

i = 1
df = leds_df[leds[i]]
df = df[df["Distance (cm)"] <= 30]
df = df[df["Distance (cm)"] >= 10]
for col in df.columns[2:3]:
    (line, ) = ax.plot(df["Distance (cm)"], df[col], linewidth=2)
    line.set_label("LED " + str(i+1) + ": " + col.replace("-", " → "))

i = 2
df = leds_df[leds[i]]
df = df[df["Distance (cm)"] <= 30]
df = df[df["Distance (cm)"] >= 10]
for col in df.columns[1:3]:
    (line, ) = ax.plot(df["Distance (cm)"], df[col], linewidth=2)
    line.set_label("LED " + str(i+1) + ": " + col.replace("-", " → "))
ax.set_xlabel("Distance (cm)", fontsize=axis_label_sz)
ax.set_ylabel("Rx Voltage (mv)", fontsize=axis_label_sz)
# ax.set_title("Best Responses", fontsize='32')
ax.set_xticks(np.arange(10, 35, 5))
ax.tick_params(axis="both", which="major", labelsize=axis_ticklabel_maj_sz)
ax.tick_params(axis="both", which="minor", labelsize=axis_ticklabel_min_sz)
ax.legend(fontsize=legend_item_sz)
plt.grid(True, which="both")
# plt.subplots_adjust(top=0.93,
#                     bottom=0.15,
#                     left=0.11,
#                     right=0.98,
#                     hspace=0.2,
#                     wspace=0.2)
plt.savefig("init_tests_best5_resps.svg")


# i = 0
# led = leds[i]
# df_w_amb = pd.read_csv("./plot_data/" + led + " (w amb).csv")
# df_wo_amb = pd.read_csv("./plot_data/" + led + " (wo amb).csv")

# fig = plt.figure()  # create a figure object
# ax = fig.add_subplot(1, 1, 1)

# for col in df_w_amb.columns[1:3]:
#     (line, ) = ax.plot(df_w_amb["Distance (cm)"][1:], df_w_amb[col][1:])
#     line.set_label(col + " (w amb)")

# for col in df_w_amb.columns[1:3]:
#     (line, ) = ax.plot(df_wo_amb["Distance (cm)"][1:], df_wo_amb[col][1:])
#     line.set_label(col + " (w/o amb)")

# ax.set_xlabel("Distance (cm)", fontsize=axis_label_sz)
# ax.set_ylabel("Rx Voltage (mv)", fontsize=axis_label_sz)
# ax.set_title(led, fontsize='20')
# ax.tick_params(axis="both", which="major", labelsize=14)
# ax.tick_params(axis="both", which="minor", labelsize=axis_ticklabel_maj_sz)
# ax.legend()
# plt.grid(True, which="both")
# plt.subplots_adjust(top=0.93,
#                     bottom=0.15,
#                     left=0.11,
#                     right=0.98,
#                     hspace=0.2,
#                     wspace=0.2)


# data_filepath = Path("./plot_data/Best Responses (330, 1k).csv")
# df = pd.read_csv(data_filepath)

# fig = plt.figure()  # create a figure object
# ax = fig.add_subplot(1, 1, 1)

# for col in df.columns[1:]:
#     (line, ) = ax.plot(df["Distance (cm)"][0:], df[col][0:])
#     line.set_label(col)
# ax.set_xlabel("Distance (cm)", fontsize=axis_label_sz)
# ax.set_ylabel("Rx Voltage (mv)", fontsize=axis_label_sz)
# ax.set_title("Best Responses", fontsize='20')
# ax.tick_params(axis="both", which="major", labelsize=14)
# ax.tick_params(axis="both", which="minor", labelsize=axis_ticklabel_maj_sz)
# ax.legend(fontsize=legend_item_sz)
# plt.grid(True, which="both")
# plt.subplots_adjust(top=0.93,
#                     bottom=0.15,
#                     left=0.11,
#                     right=0.98,
#                     hspace=0.2,
#                     wspace=0.2)


# data_filepath = Path(
#     "./plot_data/Kingbright WP154A4SEJ3VBDZGC-CA (w ampl).csv")
# df = pd.read_csv(data_filepath)

# fig = plt.figure()  # create a figure object
# ax = fig.add_subplot(1, 1, 1)

# for v in df["Reverse Bias Voltage (V)"].unique():
#     tmp_df = df[df["Reverse Bias Voltage (V)"] == v]
#     (line, ) = ax.plot(tmp_df["Distance (cm)"],
#                        tmp_df["Op-Amp Output Voltage (mV)"])
#     line.set_label(str(v) + "V")
# ax.set_xlabel("Distance (cm)", fontsize=axis_label_sz)
# ax.set_ylabel("Op-Amp Output (mv)", fontsize=axis_label_sz)
# ax.set_title("Effect of Reverse-Bias on Rx LED", fontsize='20')
# ax.tick_params(axis="both", which="major", labelsize=14)
# ax.tick_params(axis="both", which="minor", labelsize=axis_ticklabel_maj_sz)
# ax.legend(fontsize=legend_item_sz)
# plt.grid(True, which="both")
# plt.subplots_adjust(top=0.93,
#                     bottom=0.15,
#                     left=0.11,
#                     right=0.98,
#                     hspace=0.2,
#                     wspace=0.2)

data_filepath = Path(
    "./plot_data/Kingbright WP154A4SEJ3VBDZGC-CA (ampl, bias, mult Rx).csv")
df = pd.read_csv(data_filepath)


for v in df["Bias"].unique():
    if not (v == 3):
        continue
    fig = plt.figure()  # create a figure object
    ax = fig.add_subplot(1, 1, 1)
    tmp_df = df[df["Bias"] == v]
    tmp_df = tmp_df[(tmp_df["Distance"] >= 10) & (tmp_df["Distance"] <= 30)]

    (line, ) = ax.plot(tmp_df["Distance"],
                       tmp_df["1(R) - R"]/1.9, linewidth=2, color="red")
    line.set_label("Red → Red")

    (line, ) = ax.plot(tmp_df["Distance"],
                       (tmp_df["1(RG) - R"] - tmp_df["1(R) - R"])/3.8, linewidth=2,
                       color="green")
    line.set_label("Green → Red")

    (line, ) = ax.plot(tmp_df["Distance"],
                       tmp_df["1(RG) - R"]/1.9, linewidth=2, color="purple")
    line.set_label("(Red+Green) → Red")

    # for col in tmp_df.columns[2:]:
    #     (line, ) = ax.plot(tmp_df["Distance"],
    #                        tmp_df[col], linewidth=3)
    #     line.set_label(col.replace("-", "→"))
    ax.set_xlabel("Distance (cm)", fontsize=axis_label_sz)
    # ax.set_ylabel(
    #     "Rx Voltage [Excess over ambient conditions] (mv)", fontsize="28")
    # ax.set_title("Rx Bias Voltage: %d V" % v, fontsize='32')
    ax.set_ylabel("Rx Voltage (mv)", fontsize=axis_label_sz)
    ax.set_xticks(np.arange(10, 35, 5))
    ax.tick_params(axis="both", which="major", labelsize=axis_ticklabel_maj_sz)
    ax.tick_params(axis="both", which="minor", labelsize=axis_ticklabel_min_sz)
    ax.legend(fontsize=legend_item_sz)
    plt.grid(True, which="both")
    # plt.subplots_adjust(top=0.93,
    #                     bottom=0.15,
    #                     left=0.11,
    #                     right=0.98,
    #                     hspace=0.2,
    #                     wspace=0.2)
    plt.savefig("init_tests_txR_txG_interference.svg")


# data_filepath = Path(
#     "./plot_data/Kingbright WP154A4SEJ3VBDZGC-CA (adjacent Rx).csv")
# df = pd.read_csv(data_filepath)

# fig = plt.figure()  # create a figure object
# ax = fig.add_subplot(1, 1, 1)

# for col in df.columns[1:]:
#     (line, ) = ax.plot(df["Bias"], df[col])
#     line.set_label(col)
# ax.set_xlabel("Rx Bias Voltage (V)", fontsize=axis_label_sz)
# ax.set_ylabel(
#     "Rx Voltage [Excess over ambient conditions] (mv)", fontsize=axis_label_sz)
# ax.set_title("Effect of Tx on adjacent Rx", fontsize='20')
# ax.tick_params(axis="both", which="major", labelsize=14)
# ax.tick_params(axis="both", which="minor", labelsize=axis_ticklabel_maj_sz)
# ax.legend(fontsize=legend_item_sz)
# plt.grid(True, which="both")
# plt.subplots_adjust(top=0.93,
#                     bottom=0.15,
#                     left=0.11,
#                     right=0.98,
#                     hspace=0.2,
#                     wspace=0.2)


# data_filepath = Path(
#     "./plot_data/Kingbright WP154A4SEJ3VBDZGC-CA (adjacent Rx var Intensity).csv")
# df = pd.read_csv(data_filepath)

# fig = plt.figure()  # create a figure object
# ax = fig.add_subplot(1, 1, 1)

# for v in df["Bias"].unique():
#     tmp_df = df[df["Bias"] == v]
#     (line, ) = ax.plot(tmp_df["Tx Current"],
#                        tmp_df["Rx Voltage"])
#     line.set_label(str(v) + "V")
# ax.set_xlabel("Tx Current (mA)", fontsize=axis_label_sz)
# ax.set_ylabel(
#     "Rx Voltage [Excess over ambient conditions] (mv)", fontsize=axis_label_sz)
# ax.set_title("Adjacent LEDs [Tx: Red; Rx: Red]", fontsize='20')
# ax.tick_params(axis="both", which="major", labelsize=14)
# ax.tick_params(axis="both", which="minor", labelsize=axis_ticklabel_maj_sz)
# ax.legend(fontsize=14, title_fontsize=16, title="Reverse Bias")
# plt.grid(True, which="both")
# plt.subplots_adjust(top=0.93,
#                     bottom=0.15,
#                     left=0.11,
#                     right=0.98,
#                     hspace=0.2,
#                     wspace=0.2)


# data_filepath = Path(
#     "./plot_data/Kingbright WP154A4SEJ3VBDZGC-CA (Rx and Tx in same LED).csv")
# df = pd.read_csv(data_filepath)

# fig = plt.figure()  # create a figure object
# ax = fig.add_subplot(1, 1, 1)

# for col in df.columns[1:]:
#     if (col == "B - G"):
#         continue
#     (line, ) = ax.plot(df["Bias"][1:], df[col][1:])
#     line.set_label(col)
# ax.set_xlabel("Rx Bias Voltage (V)", fontsize=axis_label_sz)
# ax.set_ylabel(
#     "Rx Voltage [Excess over ambient conditions] (mv)", fontsize=axis_label_sz)
# ax.set_title("Tx and Rx in same LED", fontsize='20')
# ax.tick_params(axis="both", which="major", labelsize=14)
# ax.tick_params(axis="both", which="minor", labelsize=axis_ticklabel_maj_sz)
# ax.legend(fontsize=legend_item_sz)
# plt.grid(True, which="both")
# plt.subplots_adjust(top=0.93,
#                     bottom=0.15,
#                     left=0.11,
#                     right=0.98,
#                     hspace=0.2,
#                     wspace=0.2)

# fig = plt.figure()  # create a figure object
# ax = fig.add_subplot(1, 1, 1)

# for col in df.columns[1:]:
#     if (col == "B - G" or col == "G - R"):
#         (line, ) = ax.plot(df["Bias"][1:], df[col][1:])
#         line.set_label(col)
# ax.set_xlabel("Rx Bias Voltage (V)", fontsize=axis_label_sz)
# ax.set_ylabel(
#     "Rx Voltage [Excess over ambient conditions] (mv)", fontsize=axis_label_sz)
# ax.set_title("Tx and Rx in same LED", fontsize='20')
# ax.tick_params(axis="both", which="major", labelsize=14)
# ax.tick_params(axis="both", which="minor", labelsize=axis_ticklabel_maj_sz)
# ax.legend(fontsize=legend_item_sz)
# plt.grid(True, which="both")
# plt.subplots_adjust(top=0.93,
#                     bottom=0.15,
#                     left=0.11,
#                     right=0.98,
#                     hspace=0.2,
#                     wspace=0.2)


# data_filepath = Path(
#     "./plot_data/Kingbright WP154A4SEJ3VBDZGC-CA (int g on-off, amb vlt).csv")
# df = pd.read_csv(data_filepath)

# fig = plt.figure()  # create a figure object
# ax = fig.add_subplot(1, 1, 1)

# for col in df.columns[1:]:
#     (line, ) = ax.plot(df["Bias"][1:], df[col][1:])
#     line.set_label(col)
# ax.set_xlabel("Rx Bias Voltage (V)", fontsize=axis_label_sz)
# ax.set_ylabel(
#     "Rx Voltage [Excess over ambient conditions] (mv)", fontsize=axis_label_sz)
# ax.set_title("Rx Voltage in Ambient Conditions", fontsize='20')
# ax.tick_params(axis="both", which="major", labelsize=14)
# ax.tick_params(axis="both", which="minor", labelsize=axis_ticklabel_maj_sz)
# ax.legend(fontsize=14, title_fontsize=16, title="Internal Green Tx")
# plt.grid(True, which="both")
# plt.subplots_adjust(top=0.93,
#                     bottom=0.15,
#                     left=0.11,
#                     right=0.98,
#                     hspace=0.2,
#                     wspace=0.2)


data_filepath = Path(
    "./plot_data/Kingbright WP154A4SEJ3VBDZGC-CA (int g on-off, exc vlt).csv")
df = pd.read_csv(data_filepath)

for v in df["Bias"].unique():
    if not (v == 1):
        continue
    tmp_df = df[df["Bias"] == v]
    tmp_df = tmp_df[(tmp_df["Distance"] >= 10) &
                    (tmp_df["Distance"] <= 30)]

    fig = plt.figure()  # create a figure object
    ax = fig.add_subplot(1, 1, 1)
    (line, ) = ax.plot(tmp_df["Distance"],
                       tmp_df["Off"]/16, linewidth=3)
    line.set_label("Green On")
    (line, ) = ax.plot(tmp_df["Distance"],
                       tmp_df["On"]/16, linewidth=3)
    line.set_label("Green Off")
    ax.set_xlabel("Distance (cm)", fontsize=axis_label_sz)
    ax.set_ylabel(
        "Rx Voltage [Excess over ambient conditions] (mv)", fontsize=axis_label_sz)
    ax.set_ylabel(
        "Rx Voltage (mv)", fontsize=axis_label_sz)
    # ax.set_title("Excess Rx voltage over ambient conditions (RB: %dV)" %
    #              v, fontsize='32')

    ax.set_ylabel("Rx Voltage (mv)", fontsize=axis_label_sz)
    # ax.set_title(
    #     "Interference due to other colours in Rx LED (Sensor: Red)", fontsize='32')
    ax.set_xticks(np.arange(10, 35, 5))
    ax.tick_params(axis="both", which="major", labelsize=axis_ticklabel_maj_sz)
    ax.tick_params(axis="both", which="minor", labelsize=axis_ticklabel_min_sz)
    ax.legend(fontsize=legend_item_sz)
    plt.grid(True, which="both")
    # plt.subplots_adjust(top=0.93,
    #                     bottom=0.15,
    #                     left=0.11,
    #                     right=0.98,
    #                     hspace=0.2,
    #                     wspace=0.2)

    plt.savefig("init_tests_txR_rxG_interference.svg")


# data_filepath = Path(
#     "./plot_data/Kingbright WP154A4SEJ3VBDZGC-CA (Rx and Var Current Tx in same LED).csv")
# df = pd.read_csv(data_filepath)

# fig = plt.figure()  # create a figure object
# ax = fig.add_subplot(1, 1, 1)

# for v in df["Bias"].unique():
#     tmp_df = df[df["Bias"] == v]
#     (line, ) = ax.plot(tmp_df["Tx Current"],
#                        tmp_df["Green Tx"])
#     line.set_label("%d V" % v)
#     ax.set_xlabel("Current (mA)", fontsize=axis_label_sz)
#     ax.set_ylabel(
#         "Rx Voltage [Excess over ambient conditions] (mV)", fontsize=axis_label_sz)
#     ax.set_title("Red Rx and Variable Current Green Tx in same LED",
#                  fontsize='20')
#     ax.tick_params(axis="both", which="major", labelsize=14)
#     ax.tick_params(axis="both", which="minor", labelsize=axis_ticklabel_maj_sz)
#     ax.legend(fontsize=14, title_fontsize=16, title="Bias Voltage")
#     plt.grid(True, which="both")
#     plt.subplots_adjust(top=0.93,
#                         bottom=0.15,
#                         left=0.11,
#                         right=0.98,
#                         hspace=0.2,
#                         wspace=0.2)


# data_filepath = Path(
#     "./plot_data/Kingbright WP154A4SEJ3VBDZGC-CA (Rx and Var Duty Cycle Tx in same LED).csv")
# df = pd.read_csv(data_filepath)

# fig = plt.figure()  # create a figure object
# ax = fig.add_subplot(1, 1, 1)

# for v in df["Bias"].unique():
#     tmp_df = df[df["Bias"] == v]
#     (line, ) = ax.plot(tmp_df["Tx Duty Cycle"],
#                        tmp_df["Green Tx"])
#     line.set_label("%d V" % v)
#     ax.set_xlabel("Duty Cycle (%)", fontsize=axis_label_sz)
#     ax.set_ylabel(
#         "Rx Voltage [Excess over ambient conditions] (mV)", fontsize=axis_label_sz)
#     ax.set_title("Red Rx and Variable Duty Cycle Green Tx in same LED",
#                  fontsize='20')
#     ax.tick_params(axis="both", which="major", labelsize=14)
#     ax.tick_params(axis="both", which="minor", labelsize=axis_ticklabel_maj_sz)
#     ax.legend(fontsize=14, title_fontsize=16, title="Bias Voltage")
#     plt.grid(True, which="both")
#     plt.subplots_adjust(top=0.93,
#                         bottom=0.15,
#                         left=0.11,
#                         right=0.98,
#                         hspace=0.2,
#                         wspace=0.2)


# data_filepath = Path(
#     "./plot_data/Kingbright WP154A4SEJ3VBDZGC-CA (Rx and Var Current Tx in same LED).csv")
# df = pd.read_csv(data_filepath)

# fig = plt.figure()  # create a figure object
# ax = fig.add_subplot(1, 1, 1)


# tmp_df = df[df["Bias"] == 2]
# (line, ) = ax.plot(tmp_df["Tx Current"], tmp_df["Green Tx"], color="green")
# line.set_label("Green")
# (line, ) = ax.plot(tmp_df["Tx Current"], tmp_df["Blue Tx"], color="blue")
# line.set_label("Blue")
# ax.set_xlabel("Current (mA)", fontsize=axis_label_sz)
# ax.set_ylabel(
#     "Rx Voltage [Excess over ambient conditions] (mV)", fontsize=axis_label_sz)
# ax.set_title("Red Rx and Variable Current Green/Blue Tx in same LED (Bias: 2V)",
#              fontsize='20')
# ax.tick_params(axis="both", which="major", labelsize=14)
# ax.tick_params(axis="both", which="minor", labelsize=axis_ticklabel_maj_sz)
# ax.legend(fontsize=14, title_fontsize=16, title="Tx Colour")
# plt.grid(True, which="both")
# plt.subplots_adjust(top=0.93,
#                     bottom=0.15,
#                     left=0.11,
#                     right=0.98,
#                     hspace=0.2,
#                     wspace=0.2)


# data_filepath = Path(
#     "./plot_data/Kingbright WP154A4SEJ3VBDZGC-CA (Rx and Var Duty Cycle Tx in same LED).csv")
# df = pd.read_csv(data_filepath)

# fig = plt.figure()  # create a figure object
# ax = fig.add_subplot(1, 1, 1)


# tmp_df = df[df["Bias"] == 2]
# (line, ) = ax.plot(tmp_df["Tx Duty Cycle"], tmp_df["Green Tx"], color="green")
# line.set_label("Green")
# (line, ) = ax.plot(tmp_df["Tx Duty Cycle"], tmp_df["Blue Tx"], color="blue")
# line.set_label("Blue")
# ax.set_xlabel("Duty Cycle (%)", fontsize=axis_label_sz)
# ax.set_ylabel(
#     "Rx Voltage [Excess over ambient conditions] (mV)", fontsize=axis_label_sz)
# ax.set_title("Red Rx and Variable Current Green/Blue Tx in same LED (Bias: 2V)",
#              fontsize='20')
# ax.tick_params(axis="both", which="major", labelsize=14)
# ax.tick_params(axis="both", which="minor", labelsize=axis_ticklabel_maj_sz)
# ax.legend(fontsize=14, title_fontsize=16, title="Tx Colour")
# plt.grid(True, which="both")
# plt.subplots_adjust(top=0.93,
#                     bottom=0.15,
#                     left=0.11,
#                     right=0.98,
#                     hspace=0.2,
#                     wspace=0.2)
