#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  2 03:07:54 2023.

@author: Nishad Mandlik
"""

from datetime import datetime
from enum import Enum
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from serial import Serial, SerialException
from serial.tools.list_ports import comports
from threading import Thread
from time import sleep

_RX_SN = "95035313935351519241"
_TX_SN = "95035313935351914172"

_BAUD = 115200
_CMD_START = b"*"
_CMD_END = b"#"

_TX_CHAN = 0

CMDStage = Enum("CMDStage", ["WAITING", "INITED", "PROCED", "ENDED"])

# rx_tx_sets = [((0, 1), ((0, 0), (0, 1), (0, 2), (0, 3))),
#               ((0, 2), ((0, 0), (0, 1), (0, 2), (0, 3))),
#               ((1, 1), ((0, 0), (0, 1), (0, 2), (0, 3))),
#               ((1, 2), ((0, 0), (0, 1), (0, 2), (0, 3))),
#               ((2, 1), ((2, 0), (2, 1), (2, 2), (2, 3))),
#               ((3, 1), ((2, 3), (3, 0), (3, 1), (3, 2), (3, 3))),
#               ((3, 2), ((3, 0), (3, 1), (3, 2), (3, 3))),
#               ((3, 3), ((2, 1), (3, 1), (3, 2), (3, 3)))]

# rx_tx_sets = [
#     ((2, 2), ((2, 0), (2, 1), (2, 2), (2, 3)))]

rx_tx_sets = [
    ((2, 2), ((2, 0), (2, 1), (2, 2), (2, 3)))]

blink_half_times_us = [400]


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


def read_ser(ser, terminate, resp_recd, rx_id, period, log):
    while (1):
        if (ser.in_waiting):
            if (ser.read() == _CMD_START):
                resp = ser.read_until(_CMD_END).decode().strip("#\n\r")
                tmp = resp.split("\n")
                tmp = [i.split(",") for i in tmp]
                tmp = [(rx_id[0], period[0], int(i[0])-int(tmp[0][0]), int(i[1]))
                       for i in tmp]
                df_tmp = pd.DataFrame(
                    columns=["Rx ID", "Period (µs)", "Time (µs)",
                             "ADC Reading"])
                for i in tmp:
                    df_tmp.loc[len(df_tmp)] = i
                log[0] = df_tmp
                resp_recd[0] = True
        elif (terminate[0] is True):
            break
        else:
            sleep(0.001)


def save_log(log, name, clear=True):
    filename = "log_" + name + datetime.now().strftime("%Y%m%d_%H%M%S") + ".csv"
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
    rx_id = [0]
    period = [0]

    log = [None]

    t = Thread(target=read_ser, args=(
        ser_rx, terminate, resp_recd, rx_id, period, log))
    t.start()

    df = pd.DataFrame(
        columns=["Rx ID", "Period (µs)", "Time (µs)", "ADC Reading"])

    for rx_tx_set in rx_tx_sets:
        rx_led = rx_tx_set[0]
        tx_leds = rx_tx_set[1]
        tx_cmd_str_tmp = "b" + str(len(tx_leds))

        rx_id[0] = rx_led
        for tx_led in tx_leds:
            tx_cmd_str_tmp += (",%d,%d" % (tx_led[0], tx_led[1]))

        for time_us in blink_half_times_us:
            period[0] = 2*time_us

            tx_cmd_str = tx_cmd_str_tmp + "," + str(time_us)
            ser_tx.write(_CMD_START + tx_cmd_str.encode() + _CMD_END)
            sleep(0.2)

            rx_cmd_str = "s%d,%d" % (rx_led[0], rx_led[1])
            ser_rx.write(_CMD_START + rx_cmd_str.encode() + _CMD_END)
            while (resp_recd[0] is False):
                sleep(0.1)
            df = pd.concat((df, log[0]))
            resp_recd[0] = False

            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
            ax.plot(log[0]["Time (µs)"], log[0]
                    ["ADC Reading"], color="red", linewidth=3)
            ax.set_xlabel("Time (µs)", fontsize="28")
            ax.set_ylabel("ADC Reading", fontsize="28")
            ax.set_title("Rx Pos: " + str(rx_led) + ", Period: " +
                         str(period[0]) + "µs", fontsize='32')
            ax.tick_params(axis="both", which="major", labelsize=20)
            ax.tick_params(axis="both", which="minor", labelsize=18)
            plt.grid(True, which="both")
            plt.subplots_adjust(top=0.93,
                                bottom=0.15,
                                left=0.11,
                                right=0.98,
                                hspace=0.2,
                                wspace=0.2)

    df.to_pickle("log_" + datetime.now().strftime("%Y%m%d_%H%M%S"))

    terminate[0] = True
    t.join()
    ser_rx.close()
    ser_tx.close()
