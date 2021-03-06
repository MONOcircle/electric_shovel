#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import serial
import time
from functools import reduce

MAX_ANGLE = 270
MIN_ANGLE = 0

def ListToStr(data):
    strings = "".join(map(str, data))
    return strings


def DataToStr(x, y):
    if isinstance(x, str):
        return x + chr(y)
    else:
        return chr(x) + chr(y)


con = None


def SetSerial(port="/dev/ttyUSB0"):
    global con
    con = serial.Serial(port,
                        115200,
                        parity=serial.PARITY_EVEN,
                        stopbits=serial.STOPBITS_ONE,
                        timeout=1)


class Servo:
    def __init__(self, con, addr, angle=None):
        self.con = con
        self.addr = int(addr)
        self.angle = angle
        self.bef_angle = 0
        if angle != None:
            self.Pos(angle)

    def GetId(self):
        return self.addr

    def Pos(self, angle):
        if angle > 270: angle = 270
        if angle < 0:   angle = 0
        # self.bef_angle = self.angle
        self.angle = angle
        angle = int(3500 + int((8000 * angle) / 270))
        data = reduce(DataToStr, [(0x80 | int(self.addr)), angle >> 7, angle & 0x7f])
        self.con.write(data)

        time.sleep(0.0001)
        rcv = [ord(i) for i in self.con.read(6)]
        bef_angle = rcv[-2:]
        self.bef_angle = 270.0*((bef_angle[0] << 7 | bef_angle[1] & 0x7f) - 3500)/8000
        self.con.flushInput()
        return self.bef_angle

    def GetPos(self):
        return self.angle

    def Speed(self, speed):
        self.con.flushInput()
        self.con.write(ListToStr([(0xc0 | self.addr), 0x03, speed]))
        rcv = [ord(i) for i in self.con.read(6)]
        return rcv[-1]

    def GetSpeed(self):
        self.con.flushInput()
        self.con.write(ListToStr([(0xa0 | self.addr), 0x03]))
        rcv = [ord(i) for i in self.con.read(5)]
        return rcv[-1]

    def Stretch(self, stretch):
        self.con.flushInput()
        self.con.write(ListToStr([(0xc0 | self.addr), 0x02, stretch]))
        rcv = [ord(i) for i in self.con.read(6)]
        return rcv[-1]

    def GetStretch(self):
        self.con.flushInput()
        self.con.write(ListToStr([(0xc0 | self.addr), 0x02]))
        rcv = [ord(i) for i in self.con.read(5)]
        return rcv[-1]

