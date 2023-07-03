#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  4 16:09:10 2023.

@author: Nishad Mandlik
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from algo import get_max_r

rs = [0]
# rs = [i for i in range(0, 256)]

rgb_space = np.load("max_r_in_rgb_space.npy")
delta_es = np.load("delta_e_for_r,g,b.npy")
z = np.zeros((256, 256, 1), dtype="uint8")

title_sz = 14
axis_label_sz = 14
axis_ticklabel_maj_sz = 12
axis_ticklabel_min_sz = 10
legend_item_sz = 10
legend_title_sz = 12

fig = plt.figure()
ax = fig.add_subplot(111)
# ax.boxplot([i for i in rgb_space[:, 3].reshape(256, -1)],
#            medianprops={"linewidth": 2})
# ax.set_xticks(np.arange(1, 257, 15))
# ax.set_xticklabels(np.arange(0, 256, 15))
ax.boxplot([i for i in
            (rgb_space[:, 3].reshape(256, -1))[np.arange(0, 256, 10)]],
           medianprops={"linewidth": 2},
           widths=26*[0.7])
ax.set_xticks(np.arange(1, 27, 5))
ax.set_xticklabels(np.arange(0, 256, 50))
ax.tick_params(axis='both', which='major',
               labelsize=(3/4)*axis_ticklabel_maj_sz)
ax.tick_params(axis="both", which="minor",
               labelsize=(3/4)*axis_ticklabel_min_sz)
ax.set_xlabel("Initial R", fontsize=(3/4)*axis_label_sz)
ax.set_ylabel("$\mathregular{R_{max}}$", fontsize=(3/4)*axis_label_sz)
# ax.set_title(
#     "Distribution of $\mathregular{R_{max}}$", fontsize=24)
ax.grid(True, which="both")
plt.savefig("r_max_variation_0_255.svg")

fig = plt.figure()
ax = fig.add_subplot(111)
# ax.boxplot([i for i in rgb_space[:, 3].reshape(256, -1)][152:],
#            medianprops={"linewidth": 2, "color": "red"})
# ax.set_xticks(np.arange(1, 105, 6))
# ax.set_xticklabels(np.arange(152, 256, 6))
ax.boxplot([i for i in
            (rgb_space[:, 3].reshape(256, -1))[np.arange(153, 256, 17)]],
           medianprops={"linewidth": 1, "color": "red"})
ax.set_xticks(np.arange(1, 8, 1))
ax.set_xticklabels(np.arange(153, 256, 17))
x = np.arange(1, 7+(1/17), 1/17)
y = 17*(x-1) + 155
y[y > 255] = 255
ax.plot(x, y, linewidth=2, color="green", label="y = min(x+2, 255)")
ax.legend(fontsize=(3/4)*legend_item_sz, loc="upper left")
ax.tick_params(axis='both', which='major',
               labelsize=(3/4)*axis_ticklabel_maj_sz)
ax.tick_params(axis="both", which="minor",
               labelsize=(3/4)*axis_ticklabel_min_sz)
ax.set_xlabel("Initial R", fontsize=(3/4)*axis_label_sz)
ax.set_ylabel("$\mathregular{R_{max}}$", fontsize=(3/4)*axis_label_sz)
# ax.set_title(
#     "Approximate Function for 152 ≤ R ≤ 255", fontsize=24)
ax.grid(True, which="both")
plt.savefig("r_max_approx_152_255.svg")

fig = plt.figure()
ax = fig.add_subplot(111)
# ax.boxplot([i for i in rgb_space[:, 3].reshape(256, -1)][99:152],
#            medianprops={"linewidth": 2, "color": "red"})
# ax.set_xticks(np.arange(1, 54, 4))
# ax.set_xticklabels(np.arange(99, 152, 4))
ax.boxplot([i for i in
            (rgb_space[:, 3].reshape(256, -1))[np.arange(99, 152, 4)]],
           medianprops={"linewidth": 1, "color": "red"})
ax.set_xticks(np.arange(1, 15, 2))
ax.set_xticklabels(np.arange(99, 152, 8))
x = np.arange(1, 14+(1/4), 1/4)
y = 4*(x - 1) + 100
y[y > 255] = 255
ax.plot(x, y, linewidth=2, color="green", label="y = x+1")
ax.legend(fontsize=(3/4)*legend_item_sz, loc="upper left")
ax.tick_params(axis='both', which='major',
               labelsize=(3/4)*axis_ticklabel_maj_sz)
ax.tick_params(axis="both", which="minor",
               labelsize=(3/4)*axis_ticklabel_min_sz)
ax.set_xlabel("Initial R", fontsize=(3/4)*axis_label_sz)
ax.set_ylabel("$\mathregular{R_{max}}$", fontsize=(3/4)*axis_label_sz)
# ax.set_title(
#     "Approximate Function for 99 ≤ R < 152", fontsize=24)
ax.grid(True, which="both")
plt.savefig("r_max_approx_99_151.svg")


z1 = np.zeros((256, 256, 3), dtype="uint8")
z2 = np.zeros((256, 256, 3), dtype="uint8")
for i in range(0, 256):
    for j in range(0, 256):
        z1[i, j, 0] = get_max_r([0, i, j])
        z2[i, j] = [0, i, j]
        if (((i == 60) and (j <= 20)) or ((i <= 20) and (j == 60)) or
                ((i > 20 and i <= 60) and (j > 20 and j <= 60) and
                 (i+j == 80))):
            z2[i, j] = [0, 0, 0]
        elif (((i == 100) and (j <= 60)) or ((i <= 60) and (j == 100)) or
                ((i > 60 and i <= 100) and (j > 60 and j <= 100) and
                 (i+j == 160))):
            z2[i, j] = [0, 0, 0]
        elif (((i == 140) and (j <= 100)) or ((i <= 100) and (j == 140)) or
                ((i > 100 and i <= 140) and (j > 100 and j <= 140) and
                 (i+j == 240))):
            z2[i, j] = [0, 0, 0]
        elif (((i == 180) and (j <= 140)) or ((i <= 140) and (j == 180)) or
                ((i > 140 and i <= 180) and (j > 140 and j <= 180) and
                 (i+j == 320))):
            z2[i, j] = [0, 0, 0]
        elif (((i == 220) and (j <= 180)) or ((i <= 180) and (j == 220)) or
                ((i > 180 and i <= 220) and (j > 180 and j <= 220) and
                 (i+j == 400))):
            z2[i, j] = [0, 0, 0]
        elif (((i == 255) and (j <= 215)) or ((i <= 215) and (j == 255)) or
              ((i > 215 and j <= 255) and (i > 215 and j <= 255) and
                (i+j == 470))):
            z2[i, j] = [0, 0, 0]

px = 1/plt.rcParams['figure.dpi']
fig = plt.figure(figsize=(640*px, 770.83*px))  # create a figure object
ax1 = fig.add_subplot(211)
ax1.imshow(z2)
ax1.tick_params(axis='both', which='major',
                labelsize=(3/4)*axis_ticklabel_maj_sz)
ax1.tick_params(axis="both", which="minor",
                labelsize=(3/4)*axis_ticklabel_min_sz)
ax1.set_xlabel("Blue", fontsize=(3/4)*axis_label_sz)
ax1.set_ylabel("Green", fontsize=(3/4)*axis_label_sz)

ax2 = fig.add_subplot(212)
rs = np.arange(0, 99, 1)
gbs = [(20, 20), (60, 60), (100, 100), (140, 140),
       (180, 180), (217, 217), (242, 242)]
for i in range(0, len(gbs)):
    ax1.text(gbs[i][0]-5, gbs[i][0]+10, str(i+1),
             {"fontsize": (3/4)*16, "fontweight": "bold", "color": "white"})
    if (i % 2 == 1):
        continue
    ax2.plot(rs, list(map(get_max_r, [((r, ) + gbs[i]) for r in rs])),
             label="Zone " + str(i+1), linewidth=2)

ax2.boxplot([i for i in
             (rgb_space[:, 3].reshape(256, -1))[np.arange(0, 99, 7)]],
            medianprops={"linewidth": 2, "color": "black"},
            positions=np.arange(0, 99, 7),
            boxprops={"linewidth": 2},
            whiskerprops={"linewidth": 2},
            capprops={"linewidth": 2},
            widths=15*[2])

ax2.set_xticks(np.arange(0, 99, 14))
# whiskerprops={"linewidth": 2})
ax2.tick_params(axis='both', which='major',
                labelsize=(3/4)*axis_ticklabel_maj_sz)
ax2.tick_params(axis="both", which="minor",
                labelsize=(3/4)*axis_ticklabel_min_sz)
ax2.set_xlabel("Initial R", fontsize=(3/4)*axis_label_sz)
ax2.set_ylabel("$\mathregular{R_{max}}$", fontsize=(3/4)*axis_label_sz)
ax2.legend(fontsize=(3/4)*legend_item_sz, loc="lower right")
ax2.grid(True, which="both")
# ax2.set_title("Approximate Function for 0 ≤ R < 99", fontsize=24)
plt.subplots_adjust(bottom=0.08, top=0.95, hspace=0.3)
plt.savefig("r_max_approx_0_98.svg")

fig = plt.figure()
ax = fig.add_subplot(111)
count, bins_count = np.histogram(delta_es.reshape(-1), bins=10000)

# finding the PDF of the histogram using count values
pdf = count / sum(count)

# using numpy np.cumsum to calculate the CDF
# We can also find using the PDF values by looping and adding
cdf = np.cumsum(pdf)

ax.plot(bins_count[1:], cdf, linewidth=2)
ax.tick_params(axis='both', which='major', labelsize=axis_ticklabel_maj_sz)
ax.tick_params(axis="both", which="minor", labelsize=axis_ticklabel_min_sz)
ax.set_xlabel("$\mathregular{\Delta{E}}$", fontsize=axis_label_sz)
ax.set_ylabel("CDF", fontsize=axis_label_sz)
ax.grid(True, which="both")
plt.savefig("r_max_delta_E_CDF.svg")


# rgb_space = rgb_space[:256*256*99, 3].reshape(99, 256, 256)


# for r in rs:
#     fig = plt.figure()

#     ax = fig.add_subplot(111)

#     im = rgb_space[256*256*r:256*256*(r+1), 3].reshape(256, 256, -1)
#     im = np.concatenate([im, z, z], axis=2)
#     ax.imshow(im)
