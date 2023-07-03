#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 03:34:44 2023.

@author: Nishad Mandlik
"""

from math import ceil
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import pickle
import sys

lgt_luxes = [282]  # , "dark", "outdoor"]
dist = 10

title_sz = 14
axis_label_sz = 14
axis_ticklabel_maj_sz = 12
axis_ticklabel_min_sz = 10
legend_item_sz = 10
legend_title_sz = 12


def get_resent_bytes_Ber(n_bytes, Ber):
    n_err_bytes = round((Ber * n_bytes)/100)
    n_resent_bytes = 0
    if (n_err_bytes > 0):
        n_resent_bytes = get_resent_bytes_Ber(n_err_bytes, Ber)
    elif (n_err_bytes == n_bytes):
        return float("inf")
    return n_bytes + 1 + n_resent_bytes


def get_total_bytes(n_chunks, Ber, cer):
    n_err_chunks = round((cer * n_chunks)/100)
    n_resent_bytes = 0
    if ((n_err_chunks == 0) or ((n_err_chunks == 1) and (n_chunks == 1))):
        n_resent_bytes = get_resent_bytes_Ber(64, Ber)
    elif (n_err_chunks == n_chunks):
        return float("inf")
    else:
        n_resent_bytes = get_total_bytes(n_err_chunks, Ber, cer)
    n_orig_bytes = 64 * n_chunks
    n_crc_bytes = n_chunks
    return (n_orig_bytes + n_crc_bytes + n_resent_bytes)


def get_throughput_kbps(tick_freq_khz, trgt, sub_data):
    n_bytes_thrt = len(sub_data["Tx"])
    n_bytes_prac = get_total_bytes(
        round(n_bytes_thrt/64), sub_data["BER"], sub_data["CER"])
    total_ticks = (n_bytes_prac * 8 * 2) * (255/trgt)
    if (total_ticks == float("inf")):
        return 0
    total_ticks = ceil(total_ticks)
    total_time_ms = total_ticks / tick_freq_khz
    thrpt = (n_bytes_thrt * 8)/total_time_ms
    return thrpt


# sys.exit(0)

# -----------------------------------------------------------------------------


for lux in lgt_luxes:
    data_filename = "data_" + str(lux) + "lux"

    with open(data_filename + "_" + str(dist) + "cm.pkl", "rb") as f:
        data = pickle.load(f)

    tick_freqs_khz = [round(1000/i, 1) for i in data]

    # data.pop(90)

    ber_trgts = [30, 120, 255]  # np.arange(30, 256, 45)
    ber_vals = {k: [data[i][k]["bER"]
                    for i in [333, 166, 111, 100]] for k in ber_trgts}

    thrpt_trgts = [30, 120, 255]  # np.arange(30, 256, 45)
    thrpt_vals = {k: [get_throughput_kbps(
        round(1000/i, 1), k, data[i][k]) for i in list(data.keys())]
        for k in thrpt_trgts}

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    for tick_tm_us in data:
        if (tick_tm_us < 100):
            continue
        tick_freq_khz = round(1000/tick_tm_us, 1)
        if (tick_freq_khz not in [3.0, 6.0, 9.0, 10.0]):
            continue
        thrpts = np.array([[k, get_throughput_kbps(tick_freq_khz, k, v)]
                           for (k, v) in data[tick_tm_us].items()]).T

        ax.plot(thrpts[0], thrpts[1], linewidth=2, label=str(tick_freq_khz))

    # ax.set_title(
    #     "Performance under varying target values (Indoor Ambient Light)", fontsize="28")
    ax.set_xlabel("Target", fontsize=axis_label_sz)
    ax.set_ylabel("Throughput (kbps)", fontsize=axis_label_sz)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    ax.tick_params(axis="both", which="major", labelsize=axis_ticklabel_maj_sz)
    ax.tick_params(axis="both", which="minor", labelsize=axis_ticklabel_min_sz)
    ax.legend(fontsize=legend_item_sz, title="Tick Frequency (kHz)",
              title_fontsize=legend_title_sz)
    plt.grid(True, which="both")
    plt.savefig("eval_trgt_10cm_" + str(lux) + "lux_thrpt_freqs.svg")

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    for (k, v) in ber_vals.items():
        ax.plot([3, 6, 9, 10], v, linewidth=2, label=str(k))
    # ax.set_title(
    #     "Performance under varying tick frequency (Indoor Ambient Light)", fontsize="28")
    ax.set_xlabel("Tick Frequency (kHz)", fontsize=axis_label_sz)
    ax.set_ylabel("BER (%)", fontsize=axis_label_sz)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    ax.tick_params(axis="both", which="major", labelsize=axis_ticklabel_maj_sz)
    ax.tick_params(axis="both", which="minor", labelsize=axis_ticklabel_min_sz)
    ax.legend(fontsize=legend_item_sz, title="Target",
              title_fontsize=legend_title_sz)
    plt.grid(True, which="both")
    plt.savefig("eval_freq_10cm_" + str(lux) + "lux_ber_trgts.svg")

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    for (k, v) in thrpt_vals.items():
        ax.plot(tick_freqs_khz, v, linewidth=2, label=str(k))
    # ax.set_title(
    #     "Performance under varying tick frequency (Indoor Ambient Light)", fontsize="28")
    ax.set_xlabel("Tick Frequency (kHz)", fontsize=axis_label_sz)
    ax.set_ylabel("Throughput (kbps)", fontsize=axis_label_sz)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    ax.tick_params(axis="both", which="major", labelsize=axis_ticklabel_maj_sz)
    ax.tick_params(axis="both", which="minor", labelsize=axis_ticklabel_min_sz)
    ax.legend(fontsize=legend_item_sz, title="Target",
              title_fontsize=legend_title_sz)
    plt.grid(True, which="both")
    plt.savefig("eval_freq_10cm_" + str(lux) + "lux_thrpt_trgts.svg")

# -----------------------------------------------------------------------------

with open("data_0lux_10cm.pkl", "rb") as f:
    data_dark = pickle.load(f)
with open("data_282lux_10cm.pkl", "rb") as f:
    data_indoor = pickle.load(f)
with open("data_2576lux_10cm.pkl", "rb") as f:
    data_outdoor = pickle.load(f)

datas = [data_dark, data_indoor, data_outdoor]

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
for freq_khz in [3, 6, 9]:
    tick_tm_us = int(1000/freq_khz)
    bers = [data[tick_tm_us][255]["bER"] for data in datas]
    ax.plot([0, 300, 2600], bers, linewidth=2, label=freq_khz)
# ax.set_title(
#     "BER under various lighting conditions (Target = 255)", fontsize="28")
ax.set_xlabel("Ambient Light Intensity (lux)", fontsize=axis_label_sz)
ax.set_ylabel("BER (%)", fontsize=axis_label_sz)
ax.set_xticks([0, 300, 2600], [0, 300, 2600])
ax.set_ylim(-0.01, 0.1)

ax.tick_params(axis="both", which="major", labelsize=axis_ticklabel_maj_sz)
ax.tick_params(axis="both", which="minor", labelsize=axis_ticklabel_min_sz)
ax.legend(fontsize=legend_item_sz, title="Tick Frequency (kHz)",
          title_fontsize=legend_title_sz)
plt.grid(True, which="both")
plt.savefig("eval_lgt_111us_10cm_ber_freqs.svg")

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
for freq_khz in [3, 6, 9]:
    tick_tm_us = int(1000/freq_khz)
    thrpts = [get_throughput_kbps(
        freq_khz, 255, data[tick_tm_us][120]) for data in datas]
    ax.plot([0, 300, 2600], thrpts, linewidth=2, label=freq_khz)
# ax.set_title(
#     "Throughput under various lighting conditions (Target = 255)",
#     fontsize="28")
ax.set_xlabel("Ambient Light Intensity (lux)", fontsize=axis_label_sz)
ax.set_ylabel("Throughput (kbps)", fontsize=axis_label_sz)
ax.set_xticks([0, 300, 2600], [0, 300, 2600])

ax.tick_params(axis="both", which="major", labelsize=axis_ticklabel_maj_sz)
ax.tick_params(axis="both", which="minor", labelsize=axis_ticklabel_min_sz)
ax.legend(fontsize=legend_item_sz, title="Tick Frequency (kHz)",
          title_fontsize=legend_title_sz, loc="upper center",
          bbox_to_anchor=(0.5, 0.9))
plt.grid(True, which="both")
plt.savefig("eval_lgt_111us_10cm_thrpt_freqs.svg")

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
freq_khz = 9
tick_tm_us = int(1000/freq_khz)
for trgt in [30, 120, 255]:
    bers = [data[tick_tm_us][trgt]["bER"] for data in datas]
    ax.plot([0, 300, 2600], bers, linewidth=2, label=trgt)
# ax.set_title(
#     "BER under various lighting conditions (Tick Frequency = 9kHz)", fontsize="28")
ax.set_xlabel("Ambient Light Intensity (lux)", fontsize=axis_label_sz)
ax.set_ylabel("BER (%)", fontsize=axis_label_sz)
ax.set_xticks([0, 300, 2600], [0, 300, 2600])
ax.set_ylim(-0.01, 0.1)

ax.tick_params(axis="both", which="major", labelsize=axis_ticklabel_maj_sz)
ax.tick_params(axis="both", which="minor", labelsize=axis_ticklabel_min_sz)
ax.legend(fontsize=legend_item_sz, title="Target",
          title_fontsize=legend_title_sz)
plt.grid(True, which="both")
plt.savefig("eval_lgt_111us_10cm_ber_trgts.svg")

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
freq_khz = 9
tick_tm_us = int(1000/freq_khz)
for trgt in [30, 120, 255]:
    thrpts = [get_throughput_kbps(
        freq_khz, trgt, data[tick_tm_us][trgt]) for data in datas]
    ax.plot([0, 300, 2600], thrpts, linewidth=2, label=trgt)
# ax.set_title(
#     "Throughput under various lighting conditions (Tick Frequency = 9kHz)",
#     fontsize="28")
ax.set_xlabel("Ambient Light Intensity (lux)", fontsize=axis_label_sz)
ax.set_ylabel("Throughput (kbps)", fontsize=axis_label_sz)
ax.set_xticks([0, 300, 2600], [0, 300, 2600])

ax.tick_params(axis="both", which="major", labelsize=axis_ticklabel_maj_sz)
ax.tick_params(axis="both", which="minor", labelsize=axis_ticklabel_min_sz)
ax.legend(fontsize=legend_item_sz, title="Target",
          title_fontsize=legend_title_sz, loc="upper center",
          bbox_to_anchor=(0.5, 0.9))
plt.grid(True, which="both")
plt.savefig("eval_lgt_111us_10cm_thrpt_trgts.svg")

# -----------------------------------------------------------------------------

with open("data_282lux_5cm.pkl", "rb") as f:
    data_5 = pickle.load(f)
with open("data_282lux_10cm.pkl", "rb") as f:
    data_10 = pickle.load(f)
with open("data_282lux_20cm.pkl", "rb") as f:
    data_20 = pickle.load(f)
with open("data_282lux_40cm.pkl", "rb") as f:
    data_40 = pickle.load(f)

datas = [data_5, data_10, data_20, data_40]

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
for freq_khz in [3, 6, 9, 10]:
    tick_tm_us = int(1000/freq_khz)
    bers = [data[tick_tm_us][255]["bER"] for data in datas]
    ax.plot([5, 10, 20, 40], bers, linewidth=2, label=freq_khz)
# ax.set_title(
#     "Effect of Rx-Tx Distance on BER (Target = 255)", fontsize="28")
ax.set_xlabel("Distance (cm)", fontsize=axis_label_sz)
ax.set_ylabel("BER (%)", fontsize=axis_label_sz)
ax.set_xticks([5, 10, 20, 40], [5, 10, 20, 40])

ax.tick_params(axis="both", which="major", labelsize=axis_ticklabel_maj_sz)
ax.tick_params(axis="both", which="minor", labelsize=axis_ticklabel_min_sz)
ax.legend(fontsize=legend_item_sz, title="Tick Frequency (kHz)",
          title_fontsize=legend_title_sz)
plt.grid(True, which="both")
plt.savefig("eval_dist_111us_282lux_ber_freqs.svg")

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
for freq_khz in [3, 6, 9, 10]:
    tick_tm_us = int(1000/freq_khz)
    thrpts = [get_throughput_kbps(
        freq_khz, 255, data[tick_tm_us][120]) for data in datas]
    ax.plot([5, 10, 20, 40], thrpts, linewidth=2, label=freq_khz)
# ax.set_title(
#     "Effect of Rx-Tx Distance on Throughput (Target = 255)",
#     fontsize="28")
ax.set_xlabel("Distance (cm)", fontsize=axis_label_sz)
ax.set_ylabel("Throughput (kbps)", fontsize=axis_label_sz)
ax.set_xticks([5, 10, 20, 40], [5, 10, 20, 40])

ax.tick_params(axis="both", which="major", labelsize=axis_ticklabel_maj_sz)
ax.tick_params(axis="both", which="minor", labelsize=axis_ticklabel_min_sz)
ax.legend(fontsize=legend_item_sz, title="Tick Frequency (kHz)",
          title_fontsize=legend_title_sz)
plt.grid(True, which="both")
plt.savefig("eval_dist_111us_282lux_thrpt_freqs.svg")

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
freq_khz = 9
tick_tm_us = int(1000/freq_khz)
for trgt in [30, 120, 255]:
    bers = [data[tick_tm_us][trgt]["bER"] for data in datas]
    ax.plot([5, 10, 20, 40], bers, linewidth=2, label=trgt)
# ax.set_title(
#     "Effect of Rx-Tx Distance on BER (Tick Frequency = 9kHz)", fontsize="28")
ax.set_xlabel("Distance (cm)", fontsize=axis_label_sz)
ax.set_ylabel("BER (%)", fontsize=axis_label_sz)
ax.set_xticks([5, 10, 20, 40], [5, 10, 20, 40])

ax.tick_params(axis="both", which="major", labelsize=axis_ticklabel_maj_sz)
ax.tick_params(axis="both", which="minor", labelsize=axis_ticklabel_min_sz)
ax.legend(fontsize=legend_item_sz, title="Target",
          title_fontsize=legend_title_sz)
plt.grid(True, which="both")
plt.savefig("eval_dist_111us_282lux_ber_trgts.svg")

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
freq_khz = 9
tick_tm_us = int(1000/freq_khz)
for trgt in [30, 120, 255]:
    thrpts = [get_throughput_kbps(
        freq_khz, trgt, data[tick_tm_us][trgt]) for data in datas]
    ax.plot([5, 10, 20, 40], thrpts, linewidth=2, label=trgt)
# ax.set_title(
#     "Effect of Rx-Tx Distance on Throughput (Tick Frequency = 9kHz)",
#     fontsize="28")
ax.set_xlabel("Distance (cm)", fontsize=axis_label_sz)
ax.set_ylabel("Throughput (kbps)", fontsize=axis_label_sz)
ax.set_xticks([5, 10, 20, 40], [5, 10, 20, 40])

ax.tick_params(axis="both", which="major", labelsize=axis_ticklabel_maj_sz)
ax.tick_params(axis="both", which="minor", labelsize=axis_ticklabel_min_sz)
ax.legend(fontsize=legend_item_sz, title="Target",
          title_fontsize=legend_title_sz)
plt.grid(True, which="both")
plt.savefig("eval_dist_111us_282lux_thrpt_trgts.svg")

# -----------------------------------------------------------------------------

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
with open("data_282lux_10cm_111us_tx-1,2,4_10cm.pkl", "rb") as f:
    data = pickle.load(f)
for n_tx in data:
    thrpts = np.array([[k, get_throughput_kbps(9, min(255, n_tx*k), v)]
                       for (k, v) in data[n_tx].items()]).T
    ax.plot(thrpts[0], thrpts[1], linewidth=2, label=str(n_tx))

# ax.set_title(
#     "Throughput improvement with multiple Tx LEDs (Indoor Ambient Light, Tick Frequency = 9kHz)", fontsize="28")
ax.set_xlabel("Individual Target", fontsize=axis_label_sz)
ax.set_ylabel("Throughput (kbps)", fontsize=axis_label_sz)
ax.xaxis.set_major_locator(MaxNLocator(integer=True))

ax.tick_params(axis="both", which="major", labelsize=axis_ticklabel_maj_sz)
ax.tick_params(axis="both", which="minor", labelsize=axis_ticklabel_min_sz)
ax.legend(fontsize=legend_item_sz, title="Number of Tx LEDs",
          title_fontsize=legend_title_sz)
plt.grid(True, which="both")
plt.savefig("eval_numLEDs_111us_10cm_282lux_thrpt_numLEDs.svg")

# -----------------------------------------------------------------------------

# plt.subplots_adjust(top=0.93,
#                     bottom=0.15,
#                     left=0.11,
#                     right=0.98,
#                     hspace=0.2,
#                     wspace=0.2)
