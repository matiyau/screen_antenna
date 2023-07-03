#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 23:35:37 2023.

@author: Nishad Mandlik
"""

from datetime import datetime
from enum import Enum
from matplotlib import pyplot as plt
import pandas as pd
from serial import Serial, SerialException
from serial.tools.list_ports import comports
from threading import Thread
from time import sleep

_RX_SN = "95035313935351519241"
_TX_SN = "95035313935351914172"

_HALF_TMS_US = (50, 75, 100, 200, 400)

_BAUD = 115200
_CMD_START = b"*"
_CMD_END = b"#"

CMDStage = Enum("CMDStage", ["WAITING", "INITED", "PROCED", "ENDED"])


class DummySerial():
    def __init__(self):
        self.out_buf = b""
        self.cmd_stage = CMDStage.WAITING
        self.curr_cmd = b""

    def read(self):
        if (self.in_waiting > 0):
            tmp = self.out_buf[0].to_bytes(1, 'little')
            self.out_buf = self.out_buf[1:]
            return tmp
        else:
            return b""

    def read_until(self, end_bytes):
        while (end_bytes not in self.out_buf):
            sleep(0.02)
        end_pos = self.out_buf.find(end_bytes) + len(end_bytes)
        tmp = self.out_buf[:end_pos]
        self.out_buf = self.out_buf[end_pos+1:]
        return tmp

    def write(self, cmd_bytes):
        for byte in cmd_bytes:
            self.write_byte(byte.to_bytes(1, 'little'))

    def write_byte(self, byte):
        if (self.cmd_stage == CMDStage.WAITING):
            if (byte == _CMD_START):
                self.cmd_stage = CMDStage.INITED
                self.curr_cmd = b""
        elif (self.cmd_stage == CMDStage.INITED):
            if (byte == _CMD_END):
                if (self.curr_cmd[0].to_bytes(1, 'little') == b"l"):
                    pass
            self.curr_cmd += byte

    @property
    def in_waiting(self):
        return len(self.out_buf)

    def close(self):
        pass


def read_ser(ser, terminate, resp_recd, half_tm, log):
    while (1):
        if (ser.in_waiting):
            if (ser.read() == _CMD_START):
                resp = ser.read_until(
                    _CMD_END).decode().strip("#\n\r").split("\r\n")
                resp = [i.split(",") for i in resp]
                resp = [[half_tm[0], int(i[0]), int(i[1])] for i in resp]
                df = pd.DataFrame(
                    resp, columns=["Half-Time (us)", "Uptime (us)",
                                   "ADC Reading"])
                df["Uptime (us)"] = df["Uptime (us)"] - \
                    df["Uptime (us)"][0]
                log[0] = pd.concat([log[0], df])
                resp_recd[0] = True
        elif (terminate[0] is True):
            break
        else:
            sleep(0.001)


def save_log(log, clear=True):
    filename = "log_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".csv"
    log[0].to_csv(filename)


if __name__ == "__main__":
    port_rx = ""
    port_tx = ""

    for port, desc, hwid in comports():
        hwid_parts = [part.split("=") for part in hwid.split(" ")]
        hwid_parts = dict([part for part in hwid_parts if len(part) == 2])
        if (hwid_parts["VID:PID"] == "2341:003D"):
            if (hwid_parts["SER"] == _RX_SN):
                port_rx = port
            elif (hwid_parts["SER"] == _TX_SN):
                port_tx = port

    if (port_rx == ""):
        raise OSError("Rx Board (S/N: %s) not found." % (_RX_SN,))
    if (port_tx == ""):
        raise OSError("Tx Board (S/N: %s) not found." % (_TX_SN,))

    try:
        ser_rx = Serial(port=port_rx, baudrate=_BAUD)
    except SerialException:
        print("Dummy Serial initiated for " + port_rx)
        ser_rx = DummySerial()

    try:
        ser_tx = Serial(port=port_tx, baudrate=_BAUD)
    except SerialException:
        print("Dummy Serial initiated for " + port_tx)
        ser_tx = DummySerial()

    sleep(1)

    terminate = [False]
    resp_recd = [False]
    half_tm = [0]

    log = [pd.DataFrame(
        columns=["Half-Time (us)", "Uptime (us)", "ADC Reading"])]

    t = Thread(target=read_ser, args=(
        ser_rx, terminate, resp_recd, half_tm, log))
    t.start()

    for i in _HALF_TMS_US:
        print("Half Time: %s us" % (i,))
        resp_recd[0] = False
        half_tm[0] = i
        ser_tx.write(_CMD_START + str(i).encode() + _CMD_END)
        sleep(0.5)
        ser_rx.write(_CMD_START + b"l" + _CMD_END)
        while (resp_recd[0] is False):
            sleep(0.1)

    ser_tx.write(_CMD_START + b"0" + _CMD_END)

    terminate[0] = True
    t.join()
    ser_rx.close()
    ser_tx.close()
    df = log[0]
    fig = plt.figure()  # create a figure object
    for i in _HALF_TMS_US:
        ax = fig.add_subplot(3, 2, 1)
        df_tmp = df[df["Half-Time (us)"] == i]
        (line, ) = ax.plot(df_tmp["Uptime (us)"],
                           df_tmp["ADC Reading"], linewidth=2)
        ax.set_xlabel("Time (μs)", fontsize="20")
        ax.set_ylabel("ADC Reading", fontsize="20")
        ax.set_title("Oscillation Period: %dμs, Frequency: %fkHz" %
                     (2*i, round((10 ** 3)/(2*i), 2)), fontsize='20')
        ax.tick_params(axis="both", which="major", labelsize=14)
        ax.tick_params(axis="both", which="minor", labelsize=10)
        plt.grid(True, which="both")
        plt.subplots_adjust(top=0.93,
                            bottom=0.15,
                            left=0.11,
                            right=0.98,
                            hspace=0.2,
                            wspace=0.2)
    save_log(log, clear=False)
