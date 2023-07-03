#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  1 19:03:34 2023.

@author: Nishad Mandlik
"""

from datetime import datetime
from enum import Enum
from matplotlib import pyplot as plt
import numpy as np
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
                resp = ser.read_until(_CMD_END).decode().strip("#\n\r")
                log[0] = int(resp)
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
    half_tm = [0]

    log = [None]

    t = Thread(target=read_ser, args=(
        ser_rx, terminate, resp_recd, half_tm, log))
    t.start()

    readings = np.zeros((4, 4, 4, 4))

    for tx_i in range(0, 4):
        for tx_j in range(3, -1, -1):
            print("Tx LED: %d, %d" % (tx_i, tx_j))
            tx_cmd_str = "s%d,%d,%d,%d" % (tx_i, tx_j, _TX_CHAN, 255)
            ser_tx.write(_CMD_START + tx_cmd_str.encode() + _CMD_END)
            sleep(1)
            for rx_i in range(0, 4):
                for rx_j in range(0, 4):
                    rx_cmd_str = "g%d,%d" % (rx_i, rx_j)
                    ser_rx.write(_CMD_START + rx_cmd_str.encode() + _CMD_END)
                    while (resp_recd[0] is False):
                        sleep(0.1)

                    resp_recd[0] = False
                    readings[tx_i][3-tx_j][rx_i][rx_j] = log[0]

            tx_cmd_str = "s%d,%d,%d,%d" % (tx_i, tx_j, _TX_CHAN, 0)
            ser_tx.write(_CMD_START + tx_cmd_str.encode() + _CMD_END)
            sleep(1)

    np.save("readings", readings)
    terminate[0] = True
    t.join()
    ser_rx.close()
    ser_tx.close()
