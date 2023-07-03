#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  1 22:41:07 2023.

@author: Nishad Mandlik
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

_THRESH = 95

readings = np.load("readings.npy")

readings_thresh = (readings <= _THRESH).reshape(4, 4, 4, 4, 1)

ones = np.ones((4, 4, 4, 4, 1))

readings_rgb = np.concatenate(
    (ones, readings_thresh, readings_thresh), axis=4)

white_rgb = 255 * np.ones((4, 4, 3))

for i in range(0, 4):
    for j in range(0, 4):
        fig = plt.figure()

        ax = fig.add_subplot(121)

        white_rgb[i, j] = [255, 0, 0]
        ax.imshow(white_rgb)
        white_rgb[i, j] = [255, 255, 255]

        ax.set_xticks(np.arange(0, 4, 1))
        ax.set_yticks(np.arange(0, 4, 1))
        ax.set_xticklabels(np.arange(0, 4, 1))
        ax.set_yticklabels(np.arange(0, 4, 1))

        ax.set_xticks(np.arange(-.5, 4, 1), minor=True)
        ax.set_yticks(np.arange(-.5, 4, 1), minor=True)

        # Gridlines based on minor ticks
        ax.grid(which='minor', color='black', linestyle='-', linewidth=2)

        # Remove minor ticks
        ax.tick_params(which='minor', bottom=False, left=False)

        ax.tick_params(axis='both', which='major', labelsize=18)
        ax.set_title("Rx LED", fontsize=22)

        ax = fig.add_subplot(122)

        ax.imshow(readings_rgb[:, :, i, j])

        ax.set_xticks(np.arange(0, 4, 1))
        ax.set_yticks(np.arange(0, 4, 1))
        ax.set_xticklabels(np.arange(0, 4, 1))
        ax.set_yticklabels(np.arange(0, 4, 1))

        ax.set_xticks(np.arange(-.5, 4, 1), minor=True)
        ax.set_yticks(np.arange(-.5, 4, 1), minor=True)

        # Gridlines based on minor ticks
        ax.grid(which='minor', color='black', linestyle='-', linewidth=2)

        # Remove minor ticks
        ax.tick_params(which='minor', bottom=False, left=False)

        ax.tick_params(axis='both', which='major', labelsize=18)
        ax.set_title("Potential Tx LEDs", fontsize=22)
