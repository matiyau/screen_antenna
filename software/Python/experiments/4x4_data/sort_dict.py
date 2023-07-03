#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 21:40:23 2023.

@author: Nishad Mandlik
"""

import pickle


def sort(d):
    d = {k: v for k, v in sorted(d.items(), key=lambda item: item[0])}
    for i in d:
        d[i] = {k: v for k, v in sorted(
            d[i].items(), key=lambda item: item[0])}
    return d


files = ["dark_10", "indoor_10", "outdoor_10", "indoor_5",
         "indoor_111us_tx-1,2,4_10"]

for file in files:
    with open("data_" + file + "cm.pkl", "rb") as f:
        dat = pickle.load(f)

    dat = sort(dat)
    with open("data_" + file + "cm.pkl", "wb") as f:
        pickle.dump(dat, f)
