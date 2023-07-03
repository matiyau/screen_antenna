#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 07:24:46 2023.

@author: Nishad Mandlik
"""

from algo import get_max_r
import numpy as np
from skimage.color import rgb2lab

# rgb_space = np.load("max_r_in_rgb_space.npy")
delta_e = np.zeros((256, 256, 256))

r = -1

for r in range(0, 256):
    print(r)
    for g in range(0, 256):
        for b in range(0, 256):
            max_r = get_max_r([r, g, b])
            i = rgb2lab(np.array([r, g, b], dtype="uint8"),
                        illuminant="D65", observer="2")
            f = rgb2lab(np.array([max_r, g, b], dtype="uint8"),
                        illuminant="D65", observer="2")
            delta_e[r, g, b] = np.linalg.norm(f-i)
