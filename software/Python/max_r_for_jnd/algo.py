#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  4 20:17:09 2023.

@author: Nishad Mandlik
"""

import numpy as np
import matplotlib.pyplot as plt
from skimage.color import rgb2lab
import time


def get_max_r(rgb):
    if (rgb[0] >= 152):
        return min(255, rgb[0]+2)
    elif (rgb[0] >= 99):
        return rgb[0] + 1
    elif (((rgb[1] <= 60) and (rgb[2] <= 20)) or
          ((rgb[1] <= 20) and (rgb[2] <= 60)) or
          ((rgb[1] > 20 and rgb[1] <= 60) and
           (rgb[2] > 20 and rgb[2] <= 60) and
           (rgb[1]+rgb[2] <= 80))):
        # return 0
        return rgb[0] + 3
    elif (((rgb[1] <= 100) and (rgb[2] <= 60)) or
          ((rgb[1] <= 60) and (rgb[2] <= 100)) or
          ((rgb[1] > 60 and rgb[1] <= 100) and
           (rgb[2] > 60 and rgb[2] <= 100) and
           (rgb[1]+rgb[2] <= 160))):
        # return 42
        return int(0.9489795918367347 * rgb[0]) + 7
    elif (((rgb[1] <= 140) and (rgb[2] <= 100)) or
          ((rgb[1] <= 100) and (rgb[2] <= 140)) or
          ((rgb[1] > 100 and rgb[1] <= 140) and
           (rgb[2] > 100 and rgb[2] <= 140) and
           (rgb[1]+rgb[2] <= 240))):
        # return 84
        return int(0.8877551020408163 * rgb[0]) + 13
    elif (((rgb[1] <= 180) and (rgb[2] <= 140)) or
          ((rgb[1] <= 140) and (rgb[2] <= 180)) or
          ((rgb[1] > 140 and rgb[1] <= 180) and
           (rgb[2] > 140 and rgb[2] <= 180) and
           (rgb[1]+rgb[2] <= 320))):
        # return 126
        if (rgb[0] < 20):
            return int(0.65 * rgb[0]) + 17
        elif (rgb[0] < 40):
            return int(0.75 * rgb[0]) + 15
        else:
            return int(0.9482758620689655 * rgb[0] + 7.9482758620689655)
    elif (((rgb[1] <= 220) and (rgb[2] <= 180)) or
          ((rgb[1] <= 180) and (rgb[2] <= 220)) or
          ((rgb[1] > 180 and rgb[1] <= 220) and
           (rgb[2] > 180 and rgb[2] <= 220) and
           (rgb[1]+rgb[2] <= 400))):
        # return 168
        if (rgb[0] < 20):
            return int(0.55 * rgb[0]) + 22
        elif (rgb[0] < 40):
            return int(0.75 * rgb[0]) + 18
        else:
            return int(0.9137931034482759 * rgb[0] + 11.44827586206896)
    elif (((rgb[1] <= 255) and (rgb[2] <= 215)) or
          ((rgb[1] <= 215) and (rgb[2] <= 255)) or
          ((rgb[1] > 215 and rgb[1] <= 255) and
           (rgb[2] > 215 and rgb[2] <= 255) and
           (rgb[1]+rgb[2] <= 470))):
        # return 210
        if (rgb[0] < 20):
            return int(0.5 * rgb[0]) + 26
        elif (rgb[0] < 40):
            return int(0.7 * rgb[0]) + 22
        else:
            return int(0.896551724137931 * rgb[0] + 14.137931034482762)
    else:
        # return 252
        if (rgb[0] < 20):
            return int(0.4 * rgb[0]) + 32
        elif (rgb[0] < 40):
            return int(0.6 * rgb[0]) + 28
        else:
            return int(0.8793103448275862 * rgb[0] + 16.827586206896555)


# start = time.time()

# delta_es = np.zeros((256, 256, 256))

# for r in range(0, 256):
#     print("Red Comp: %d" % (r, ))
#     for g in range(0, 256):
#         for b in range(0, 256):
#             r_max = get_max_r([r, g, b])
#             lab_i = rgb2lab(np.array([[[r, g, b]]], dtype="uint8"),
#                             illuminant="D65", observer="2")
#             lab_f = rgb2lab(np.array([[[r_max, g, b]]], dtype="uint8"),
#                             illuminant="D65", observer="2")
#             delta_es[r, g, b] = round(np.linalg.norm(lab_f - lab_i), 2)

# end = time.time()

# print(f"Runtime: {(end-start)*10**3:.03f}ms")
