# -*- coding: utf-8 -*-
import struct
import time
import os
from MX12W import MX12W, BAUDRATE

def ps3_control():
    device_path = "/dev/input/js0" 
    EVENT_FORMAT = "LhBB"
    EVENT_SIZE = struct.calcsize(EVENT_FORMAT)

    with open(device_path, "rb") as device:
        event = device.read(EVENT_SIZE)
        while event:
            (ds3_time, ds3_val, ds3_type, ds3_num) = struct.unpack(EVENT_FORMAT,
                                                                   event)
            # ds3_num=0: left stick, left/right [servo_id=0], 旋回
            if ds3_num == 0:
                """print(
                    "ServoId=0, Left stick [LEFT/RIGHT]: {}, {}, {}, {}".format(
                        ds3_time, ds3_val, ds3_type, ds3_num))"""
                rotate.stick_control_rotate(ds3_val)
            
            # ds3_num=12: L2 [servo_id=1] left wheel CW
            if ds3_num == 12:
                """print("ServoId=1, L2 ON: {}, {}, {}, {}".format(ds3_time,
                                                                ds3_val,
                                                                ds3_type,
                                                                ds3_num))"""
                left.button_control_wheel(ds3_val)

            # ds3_num=14: L1 [servo_id=1] left wheel CCW
            if ds3_num == 14:
                """print("ServoId=1, L1 ON: {}, {}, {}, {}".format(ds3_time,
                                                                ds3_val,
                                                                ds3_type,
                                                                ds3_num))"""
                left.button_control_wheel(ds3_val, reverse=True)

            # ds3_num=4: R2 [servo_id=2] right wheel CW
            if ds3_num == 13:
                """print("ServoId=2, R2 ON: {}, {}, {}, {}".format(ds3_time,
                                                                ds3_val,
                                                                ds3_type,
                                                                ds3_num))"""
                right.button_control_wheel(ds3_val,reverse=True)

            # ds3_num=4: R1 [servo_id=2] right wheel CCW
            if ds3_num == 15:
                """print("ServoId=2, R1 ON: {}, {}, {}, {}".format(ds3_time,
                                                                ds3_val,
                                                                ds3_type,
                                                                ds3_num))"""
                right.button_control_wheel(ds3_val)

            # ds3_num=3: right stick, left/right [servo_id=3], Bucket
            if ds3_num == 2:
                """print("Right stick [LEFT/RIGHT]: {0}, {1}, {2}, {3}".format(
                    ds3_time, ds3_val, ds3_type, ds3_num))"""
                bucket.stick_control(ds3_val)
                
            # ds3_num=1: left stick, up/down [servo_id=1], Arm
            if ds3_num == 1:
                """print("left stick [up/down]: {}, {}, {}, {}".format(ds3_time,
                                                                    ds3_val,
                                                                    ds3_type,
                                                                    ds3_num))"""
                arm.stick_control(ds3_val*-1)

            # ds3_num=2: right stick, up/down [servo_id=2], Boom
            if ds3_num == 3:
                """print("Right stick [LEFT/RIGHT]: {0}, {1}, {2}, {3}".format(
                    ds3_time, ds3_val, ds3_type, ds3_num))"""
                boom.stick_control(ds3_val)

            if ds3_num == 0:
                if ds3_val == 1:
                    select_button = 1
                else:
                    select_button = 0

            if ds3_num == 3:
                if ds3_val == 1:
                    start_button = 1
                else:
                    start_button = 0

            if select_button == 1 and start_button == 1:
                os.system('sudo aplay /home/pi/Documents/electric_shovel/ics35_py/stop.wav')
                os.system("sudo shutdown -h now")

            event = device.read(EVENT_SIZE)

if __name__ == "__main__":
    #os.system('sudo amixer cset numid=3 1')
    #os.system('sudo amixer cset numid=1 400')
    #os.system('sudo aplay /home/pi/Documents/electric_shovel/ics35_py/start.wav')
    
    ###servo initialize###
    rotate  = MX12W("/dev/ttyUSB0", BAUDRATE.B1M, 0)
    left    = MX12W("/dev/ttyUSB0", BAUDRATE.B1M, 1)
    right   = MX12W("/dev/ttyUSB0", BAUDRATE.B1M, 2)
    boom    = MX12W("/dev/ttyUSB0", BAUDRATE.B1M, 3)
    arm     = MX12W("/dev/ttyUSB0", BAUDRATE.B1M, 4)
    bucket  = MX12W("/dev/ttyUSB0", BAUDRATE.B1M, 5)
    
    rotate.open()
    left.open()
    right.open()
    left.open()
    boom.open()
    arm.open()
    bucket.open()

    rotate.set_wheel_mode()
    left.set_wheel_mode()
    right.set_wheel_mode()
    boom.set_wheel_mode()
    arm.set_wheel_mode()
    bucket.set_wheel_mode()

    rotate.set_torque(MX12W.TORQUE_ON)
    left.set_torque(MX12W.TORQUE_ON)
    right.set_torque(MX12W.TORQUE_ON)
    boom.set_torque(MX12W.TORQUE_ON)
    arm.set_torque(MX12W.TORQUE_ON)
    bucket.set_torque(MX12W.TORQUE_ON)
    
    os.system("sudo sixad -start &") # sixadのコマンド実行

    i = 0
    while True:
        i += 1
        try:
            ps3_control()
            
        except Exception as e:
            print("error:{e} retry:{i}".format(e=e, i=i))
            time.sleep(5)  # 5秒待つ
