#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 00:19:07 2023.

@author: Nishad Mandlik
"""

import os
from serial.tools.list_ports import comports

env = DefaultEnvironment()

board_sn = env.GetProjectOption("board_sn")
upload_port = "/"
board_found = False

if (board_sn != ""):
    for port, desc, hwid in comports():
        hwid_parts = [part.split("=") for part in hwid.split(" ")]
        hwid_parts = dict([part for part in hwid_parts if len(part) == 2])
        if ((hwid_parts["VID:PID"] == "2341:003D") and
                (hwid_parts["SER"] == board_sn)):
            board_found = True
            upload_port = port
            break

    if board_found:
        print("Board with S/N: %s found at %s." % (board_sn, upload_port))
    else:
        raise OSError("Board with S/N: %s not found." % (board_sn,))
else:
    for port, desc, hwid in comports():
        hwid_parts = [part.split("=") for part in hwid.split(" ")]
        hwid_parts = dict([part for part in hwid_parts if len(part) == 2])
        if (hwid_parts["VID:PID"] == "2341:003D"):
            print("Board S/N not provided. Selecting %s." % (upload_port,))
            upload_port = port

env["UPLOAD_PORT"] = upload_port
