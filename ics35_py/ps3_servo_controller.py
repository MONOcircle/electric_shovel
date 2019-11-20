#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import time
import struct
import os

import serialServo
import sys
import serial
import time
import wiringpi
from getch import _Getch

# GPIO初期化
wiringpi.wiringPiSetupGpio()
# GPIOを出力モード（1）に設定
wiringpi.pinMode( 2, 1 )

con = None
con = serial.Serial("/dev/ttyUSB0",
                    115200,
                    parity=serial.PARITY_EVEN,
                    stopbits=serial.STOPBITS_ONE,
                    timeout=1)

initial_angle = 135     # 中立

servos = []
for i in range(1):
    print("Servo", i, "initializing...")
    servos.append(serialServo.Servo(con, "{}".format(i)))
print(servos)
angles = [servo.GetPos() for servo in servos]

th = 25000

def max_angle_stick_control(servo_id, val):
    if (-1 * th <= val) and (val <= th):
        _pos = servos[servo_id].Pos(servos[servo_id].GetPos())
        _pos = servos[servo_id].Pos(_pos)
    if val > th:
        _pos = servos[servo_id].Pos(serialServo.MAX_ANGLE)
    if val < -1 * th:
        _pos = servos[servo_id].Pos(serialServo.MIN_ANGLE)
    print("servo_id = {}, angle postition = {}, value = {}".format(servo_id, _pos, val))


def fine_angle_stick_control(servo_id, val):
    if (-1 * th <= val) and (val <= th):
        _pos = servos[servo_id].Pos(servos[servo_id].GetPos())
        _pos = servos[servo_id].Pos(_pos)
    if val > th:
        _pos = servos[servo_id].Pos(servos[servo_id].GetPos() + 5)
    if val < -1 * th:
        _pos = servos[servo_id].Pos(servos[servo_id].GetPos() - 5)
    print("servo_id = {}, angle postition = {}, value = {}".format(servo_id, _pos, val))


def max_angle_control(servo_id, val, reverse=False):
    if val == 0:
        _pos = servos[servo_id].Pos(servos[servo_id].GetPos())
        _pos = servos[servo_id].Pos(_pos)
    else:
        if reverse:
            _pos = servos[servo_id].Pos(serialServo.MIN_ANGLE)
        else:
            _pos = servos[servo_id].Pos(serialServo.MAX_ANGLE)
    print("servo_id = {}, angle postition = {}".format(servo_id, _pos))


def infinite_loop_control(servo_id, val, reverse=False):
    if val == 0:
        _pos = servos[servo_id].Pos(135)    # 中立
    else:
        if reverse:
            _pos = servos[servo_id].Pos(serialServo.MIN_ANGLE)    # -方向
        else:
            _pos = servos[servo_id].Pos(serialServo.MAX_ANGLE)    # +方向
    print("servo_id = {}, angle postition = {}".format(servo_id, _pos))


def infinite_loop_stick_control(servo_id, val):
    if (-1 * th<= val) and (val <= th):
        _pos = servos[servo_id].Pos(135)    # 中立
    if val > th:
        _pos = servos[servo_id].Pos(serialServo.MAX_ANGLE)
    if val < -1 * th:
        _pos = servos[servo_id].Pos(serialServo.MIN_ANGLE)
    print("servo_id = {}, angle postition = {}, value={}".format(servo_id, _pos, val))


def ps3_control():
    device_path = "/dev/input/js0"
    EVENT_FORMAT = "LhBB";
    EVENT_SIZE = struct.calcsize(EVENT_FORMAT)

    with open(device_path, "rb") as device:
        event = device.read(EVENT_SIZE)
        while event:
            (ds3_time, ds3_val, ds3_type, ds3_num) = struct.unpack(EVENT_FORMAT, event)

            # ds3_num=0: left stick, left/right [servo_id=0], 旋回
            if ds3_num == 0:
                print("Left stick [LEFT/RIGHT]: {0}, {1}, {2}, {3}".format(ds3_time, ds3_val, ds3_type, ds3_num))
                servo_id = 0
                infinite_loop_stick_control(servo_id, ds3_val)
            '''
            # ds3_num=1: left stick, up/down [servo_id=1], Arm
            if ds3_num == 1:
                print("Left stick [UP/DOWN]: {0}, {1}, {2}, {3}".format(ds3_time, ds3_val, ds3_type, ds3_num))
                servo_id = 1
                fine_angle_stick_control(servo_id, ds3_val)

            # ds3_num=2: right stick, left/right [servo_id=2], Bucket
            if ds3_num == 2:
                print("Right stick [LEFT/RIGHT]: {0}, {1}, {2}, {3}".format(ds3_time, ds3_val, ds3_type, ds3_num))
                servo_id = 2
                max_angle_stick_control(servo_id, ds3_val)

            # ds3_num=3: right stick, up/down [servo_id=3], Boom
            if ds3_num == 3:
                print("Right stick [LEFT/RIGHT]: {0}, {1}, {2}, {3}".format(ds3_time, ds3_val, ds3_type, ds3_num))
                servo_id = 3
                fine_angle_stick_control(servo_id, ds3_val)

            # ds3_num=12: L2 [servo_id=4]
            if ds3_num == 12:
                print("L2 ON: {0}, {1}, {2}, {3}".format(ds3_time, ds3_val, ds3_type, ds3_num))
                servo_id = 4
                infinite_loop_control(servo_id, ds3_val)

            # ds3_num=14: L1 [servo_id=4]
            if ds3_num == 14:
                print("L1 ON: {0}, {1}, {2}, {3}".format(ds3_time, ds3_val, ds3_type, ds3_num))
                servo_id = 4
                infinite_loop_control(servo_id, ds3_val, reverse=True)

            # ds3_num=4: R2 [servo_id=5]
            if ds3_num == 13:
                print("R2 ON: {0}, {1}, {2}, {3}".format(ds3_time, ds3_val, ds3_type, ds3_num))
                servo_id = 5
                infinite_loop_control(servo_id, ds3_val, reverse=True)

            # ds3_num=4: R1 [servo_id=5]
            if ds3_num == 15:
                print("R1 ON: {0}, {1}, {2}, {3}".format(ds3_time, ds3_val, ds3_type, ds3_num))
                servo_id = 5
                infinite_loop_control(servo_id, ds3_val)
            '''
            event = device.read(EVENT_SIZE)


if __name__ == "__main__":
    ps3_control()

