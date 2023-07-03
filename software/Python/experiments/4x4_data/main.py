#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 02:24:12 2023.

@author: Nishad Mandlik
"""

from datetime import datetime
from enum import Enum
from matplotlib import pyplot as plt
import numpy as np
from math import ceil
import pickle
from serial import Serial, SerialException
from serial.tools.list_ports import comports
from threading import Thread
from time import sleep

_RX_SN = "95035313935351519241"
_TX_SN = "95035313935351914172"

_BAUD = 115200
_CMD_START = b"*"
_CMD_END = b"#"


CMDStage = Enum("CMDStage", ["WAITING", "INITED", "PROCED", "ENDED"])

# (rx_row, rx_col)
rx_led = (2, 2)

trgts = [210]

# (tx_row, tx_col, tx_budget)
tx_leds = [(2, 1, i) for i in range(30, 256, 45)]

freqs_khz = np.array([3])

tick_tms_us = (1000/freqs_khz).astype("int")


class DummySerial():
    def __init__(self):
        self.out_buf = b""
        self.cmd_stage = CMDStage.WAITINGnp
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


def read_ser(ser, terminate, resp_recd, log):
    while (1):
        if (ser.in_waiting):
            if (ser.read() == _CMD_START):
                resp = ser.read_until(_CMD_END).decode().strip("#\n\r")
                tmp = resp.split("\n")
                log[0] = [int(i) for i in tmp]
                resp_recd[0] = True
        elif (terminate[0] is True):
            break
        else:
            sleep(0.001)


def save_data(dat):
    filename = "data_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".pkl"
    with open(filename, "wb") as f:
        pickle.dump(dat, f)


def get_ber(rx_arr, tx_arr):
    total_bits = 8 * len(tx_arr)
    err_cnt = 0
    for i in range(0, len(tx_arr)):
        if (i >= len(rx_arr)):
            tmp = 0
        else:
            tmp = rx_arr[i]
        if (tmp != tx_arr[i]):
            for j in range(0, 8):
                if (((tmp >> j) & 1) != ((tx_arr[i] >> j) & 1)):
                    err_cnt += 1
    return (err_cnt*100)/total_bits


def get_Ber(rx_arr, tx_arr):
    # Byte Error Rate
    total_bytes = len(tx_arr)
    err_cnt = 0
    for i in range(0, len(tx_arr)):
        if (i >= len(rx_arr)):
            err_cnt += 1
        elif (rx_arr[i] != tx_arr[i]):
            err_cnt += 1
    return (err_cnt*100)/total_bytes


def get_cer(rx_arr, tx_arr):
    # Chunk Error Rate
    total_chunks = ceil(len(tx_arr)/64)
    err_cnt = 0
    for i in range(0, total_chunks):
        for j in range(64*i, min(64*(i+1), len(tx_arr))):
            if (j >= len(rx_arr)):
                err_cnt += 1
                break
            if (rx_arr[j] != tx_arr[j]):
                err_cnt += 1
                break
    return (err_cnt*100)/total_chunks


if __name__ == "__main__":
    # tmp = 0
    # rep_cnt = 0
    # while (1):
    # tx_leds = [(2, 1, trgts[tmp])]

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

    rx_terminate = [False]
    rx_resp_recd = [False]
    rx_log = [None]

    tx_terminate = [False]
    tx_resp_recd = [False]
    tx_log = [None]

    rx_t = Thread(target=read_ser, args=(ser_rx, rx_terminate, rx_resp_recd,
                                         rx_log))
    tx_t = Thread(target=read_ser, args=(ser_tx, tx_terminate, tx_resp_recd,
                                         tx_log))
    rx_t.start()
    tx_t.start()

    data = {}

    for tick_tm_us in tick_tms_us:
        data[tick_tm_us] = {}
        for tx_led in tx_leds:
            rx_cmd_str = "r," + str(tick_tm_us) + "," + str(rx_led[0]) + \
                "," + str(rx_led[1])
            ser_rx.write(_CMD_START + rx_cmd_str.encode() + _CMD_END)
            sleep(2)
            tx_cmd_str = "t," + str(tick_tm_us) + "," + str(tx_led[0]) + \
                "," + str(tx_led[1]) + "," + str(tx_led[2])

            ser_tx.write(_CMD_START + tx_cmd_str.encode() + _CMD_END)

            while ((tx_resp_recd[0] is False) or (rx_resp_recd[0] is False)):
                sleep(0.1)

            data[tick_tm_us][tx_led[2]] = {"Tx": np.array(tx_log[0]),
                                           "Rx": np.array(rx_log[0])}

            data[tick_tm_us][tx_led[2]]["bER"] = \
                get_ber(data[tick_tm_us][tx_led[2]]["Rx"],
                        data[tick_tm_us][tx_led[2]]["Tx"])

            data[tick_tm_us][tx_led[2]]["BER"] = \
                get_Ber(data[tick_tm_us][tx_led[2]]["Rx"],
                        data[tick_tm_us][tx_led[2]]["Tx"])

            data[tick_tm_us][tx_led[2]]["CER"] = \
                get_cer(data[tick_tm_us][tx_led[2]]["Rx"],
                        data[tick_tm_us][tx_led[2]]["Tx"])

            tx_resp_recd[0] = False
            rx_resp_recd[0] = False
            print("%d, %d: bER = %f%%, BER = %f%%, CER = %f%%" %
                  (tick_tm_us, tx_led[2], data[tick_tm_us][tx_led[2]]["bER"],
                   data[tick_tm_us][tx_led[2]]["BER"],
                   data[tick_tm_us][tx_led[2]]["CER"]))
            sleep(2)

    tx_terminate[0] = True
    rx_terminate[0] = True
    tx_t.join()
    rx_t.join()
    ser_rx.close()
    ser_tx.close()

    # if ((data[100][trgts[tmp]]["bER"] >= 0.16) and (data[100][trgts[tmp]]["bER"] <= 0.22)):
    save_data(data)
    #     rep_cnt = 0
    #     tmp += 1
    #     if (tmp == len(trgts)):
    #         break
    # else:
    #     rep_cnt += 1
    #     if (rep_cnt == 20):
    #         rep_cnt = 0
    #         tmp += 1
    #         if (tmp == len(trgts)):
    #             break
