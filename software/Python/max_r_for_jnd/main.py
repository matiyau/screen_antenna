#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  3 23:43:49 2023.

@author: Nishad Mandlik
"""

import numpy as np
import pandas as pd
from skimage.color import rgb2lab
import time

start = time.time()

rgb_space = np.array([(r, g, b, 0) for r in range(0, 256)
                      for g in range(0, 256) for b in range(0, 256)])

max_r_init = 0

rgb_space[:, 3] = rgb_space[:, 0]

for rgb in rgb_space[:256*256*255]:
    if (rgb[2] == 0):
        if (rgb[1] == 0):
            print("Red Comp: %d" % (rgb[0],))

    #     else:
    #         max_r_init = rgb_space[256*256*rgb[0] + 256*(rgb[1]-1)][3]

    # max_r_init = max(max_r_init, rgb[0]+1)
    if (rgb[0] != 0):
        max_r_init = rgb_space[256*256*(rgb[0]-1) + 256*rgb[1] + rgb[2]][3]
    else:
        max_r_init = 1

    lab = rgb2lab(np.array([[rgb[:3]]], dtype="uint8"),
                  illuminant="D65", observer="2")

    for i in range(max_r_init, 256):
        lab2 = rgb2lab(np.array([[[i, rgb[1], rgb[2]]]], dtype="uint8"),
                       illuminant="D65", observer="2")
        delta_e = np.linalg.norm(lab2 - lab)
        if (round(delta_e, 2) <= 1):
            rgb[3] = i
            max_r_init = i
        else:
            break

df = pd.DataFrame(rgb_space, columns=["R", "G", "B", "R_new Max"])

np.save("max_r_in_rgb_space", rgb_space)
df.to_csv("max_r_in_rgb_space.csv", index=False)

end = time.time()

print(f"Runtime: {(end-start)*10**3:.03f}ms")
