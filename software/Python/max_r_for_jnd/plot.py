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
z = np.zeros((256, 256, 1), dtype="uint8")

# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.boxplot([i for i in rgb_space[:, 3].reshape(256, -1)],
#            medianprops={"linewidth": 2})
# ax.set_xticks(np.arange(1, 257, 15))
# ax.set_xticklabels(np.arange(0, 256, 15))
# ax.tick_params(axis='both', which='major', labelsize=18)
# ax.set_xlabel("Actual R", fontsize=22)
# ax.set_ylabel("$\mathregular{R_{max}}$", fontsize=22)
# ax.set_title(
#     "Distribution of $\mathregular{R_{max}}$", fontsize=24)

# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.boxplot([i for i in rgb_space[:, 3].reshape(256, -1)][152:],
#            medianprops={"linewidth": 2, "color": "red"})
# x = np.arange(1, 105, 1)
# y = x + 153
# y[y > 255] = 255
# ax.plot(x, y, linewidth=2, color="green", label="y = min(x+2, 255)")
# ax.legend(fontsize=16, loc="upper left")
# ax.set_xticks(np.arange(1, 105, 6))
# ax.set_xticklabels(np.arange(152, 256, 6))
# ax.tick_params(axis='both', which='major', labelsize=18)
# ax.set_xlabel("Actual R", fontsize=22)
# ax.set_ylabel("$\mathregular{R_{max}}$", fontsize=22)
# ax.set_title(
#     "Approximate Function for 152 ≤ R ≤ 255", fontsize=24)

# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.boxplot([i for i in rgb_space[:, 3].reshape(256, -1)][99:152],
#            medianprops={"linewidth": 2, "color": "red"})
# x = np.arange(1, 54, 1)
# y = x + 99
# y[y > 255] = 255
# ax.plot(x, y, linewidth=2, color="green", label="y = x+1")
# ax.legend(fontsize=16, loc="upper left")
# ax.set_xticks(np.arange(1, 54, 4))
# ax.set_xticklabels(np.arange(99, 152, 4))
# ax.tick_params(axis='both', which='major', labelsize=18)
# ax.set_xlabel("Actual R", fontsize=22)
# ax.set_ylabel("$\mathregular{R_{max}}$", fontsize=22)
# ax.set_title(
#     "Approximate Function for 99 ≤ R < 152", fontsize=24)


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
fig = plt.figure()
ax1 = fig.add_subplot(121)
ax1.imshow(z2)
ax1.tick_params(axis='both', which='major', labelsize=18)
ax1.set_xlabel("Blue", fontsize=22)
ax1.set_ylabel("Green", fontsize=22)

ax2 = fig.add_subplot(122)
rs = np.arange(0, 99, 1)
gbs = [(20, 20), (60, 60), (100, 100), (140, 140),
       (180, 180), (217, 217), (242, 242)]
for i in range(0, len(gbs)):
    ax2.plot(rs, list(map(get_max_r, [((r, ) + gbs[i]) for r in rs])),
             label="Zone " + str(i+1), linewidth=2)
    ax1.text(gbs[i][0]-5, gbs[i][0]+10, str(i+1),
             {"fontsize": 24, "fontweight": "bold", "color": "white"})

ax2.tick_params(axis='both', which='major', labelsize=18)
ax2.set_xlabel("Actual R", fontsize=22)
ax2.set_ylabel("$\mathregular{R_{max}}$", fontsize=22)
ax2.legend(fontsize=16, loc="upper left")
ax2.set_title("Approximate Function for 0 ≤ R < 99", fontsize=24)


# rgb_space = rgb_space[:256*256*99, 3].reshape(99, 256, 256)


# for r in rs:
#     fig = plt.figure()

#     ax = fig.add_subplot(111)

#     im = rgb_space[256*256*r:256*256*(r+1), 3].reshape(256, 256, -1)
#     im = np.concatenate([im, z, z], axis=2)
#     ax.imshow(im)
