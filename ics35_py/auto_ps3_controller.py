# -*- coding: utf-8 -*-
import struct
import serialServo
import serial
import wiringpi
import time
import os

###
# servoの初期化
###
con = serial.Serial("/dev/ttyUSB0",
                    115200,
                    parity=serial.PARITY_EVEN,
                    stopbits=serial.STOPBITS_ONE,
                    timeout=1)
servo0 = serialServo.Servo(con, "0")  # Servo ID = 0, 旋回
servo1 = serialServo.Servo(con, "1")  # Servo ID = 1, L1 or L2
servo2 = serialServo.Servo(con, "2")  # Servo ID = 2, R1 or R2
###
# servo操作関数
###
stick_th = 25000


def stick_infinite_loop_control(servo, val):
    if (-1 * stick_th <= val) and (val <= stick_th):
        _pos = servo.Pos(135)  # 中立
    if val > stick_th:
        _pos = servo.Pos(serialServo.MAX_ANGLE)
    if val < -1 * stick_th:
        _pos = servo.Pos(serialServo.MIN_ANGLE)
    #print("angle postition = {}, value={}".format(_pos, val))


def infinite_loop_control(servo, val, reverse=False):
    if val == 0:
        _pos = servo.Pos(135)  # 中立
    else:
        if reverse:
            _pos = servo.Pos(serialServo.MIN_ANGLE)  # -方向
        else:
            _pos = servo.Pos(serialServo.MAX_ANGLE)  # +方向
    #print("angle postition = {}".format(_pos))


###
# GPIOセットアップ
###
#
motor1_pin1 = 17
motor1_pin2 = 27
motor2_pin1 = 22
motor2_pin2 = 10
motor3_pin1 = 9
motor3_pin2 = 11
speaker_pin = 13
wiringpi.wiringPiSetupGpio()
# 全てのpin output
wiringpi.pinMode(motor1_pin1, 1)
wiringpi.pinMode(motor1_pin2, 1)
wiringpi.pinMode(motor2_pin1, 1)
wiringpi.pinMode(motor2_pin2, 1)
wiringpi.pinMode(motor3_pin1, 1)
wiringpi.pinMode(motor3_pin2, 1)
# PWM
wiringpi.pinMode(speaker_pin, 2)


def stick_motor_control(pin1, pin2, val):
    if (-1 * stick_th <= val) and (val <= stick_th):
        # ブレーキ
        input1 = 1
        input2 = 1
    if val > stick_th:
        # 正転
        input1 = 1
        input2 = 0
    if val < -1 * stick_th:
        # 逆転
        input1 = 0
        input2 = 1

    wiringpi.digitalWrite(pin1, input1)
    wiringpi.digitalWrite(pin2, input2)
    """print("pin1={}-input={}, pin2={}-input={}".format(pin1, input1,
                                                      pin2, input2))"""


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
                stick_infinite_loop_control(servo0, ds3_val)

            # ds3_num=1: left stick, up/down [servo_id=1], Arm
            if ds3_num == 1:
                """print("left stick [up/down]: {}, {}, {}, {}".format(ds3_time,
                                                                    ds3_val,
                                                                    ds3_type,
                                                                    ds3_num))"""
                                                                    
                stick_motor_control(motor1_pin1, motor1_pin2, ds3_val*-1)

            # ds3_num=2: right stick, left/right [servo_id=2], Bucket
            if ds3_num == 3:
                """print("Right stick [LEFT/RIGHT]: {0}, {1}, {2}, {3}".format(
                    ds3_time, ds3_val, ds3_type, ds3_num))"""
                stick_motor_control(motor2_pin1, motor2_pin2, ds3_val)

            # ds3_num=3: right stick, up/down [servo_id=3], Boom
            if ds3_num == 2:
                """print("Right stick [LEFT/RIGHT]: {0}, {1}, {2}, {3}".format(
                    ds3_time, ds3_val, ds3_type, ds3_num))"""
                stick_motor_control(motor3_pin1, motor3_pin2, ds3_val)

            # ds3_num=12: L2 [servo_id=1]
            if ds3_num == 12:
                """print("ServoId=1, L2 ON: {}, {}, {}, {}".format(ds3_time,
                                                                ds3_val,
                                                                ds3_type,
                                                                ds3_num))"""
                infinite_loop_control(servo1, ds3_val)

            # ds3_num=14: L1 [servo_id=1]
            if ds3_num == 14:
                """print("ServoId=1, L1 ON: {}, {}, {}, {}".format(ds3_time,
                                                                ds3_val,
                                                                ds3_type,
                                                                ds3_num))"""
                infinite_loop_control(servo1, ds3_val, reverse=True)

            # ds3_num=4: R2 [servo_id=2]
            if ds3_num == 13:
                """print("ServoId=2, R2 ON: {}, {}, {}, {}".format(ds3_time,
                                                                ds3_val,
                                                                ds3_type,
                                                                ds3_num))"""
                infinite_loop_control(servo2, ds3_val,reverse=True)

            # ds3_num=4: R1 [servo_id=2]
            if ds3_num == 15:
                """print("ServoId=2, R1 ON: {}, {}, {}, {}".format(ds3_time,
                                                                ds3_val,
                                                                ds3_type,
                                                                ds3_num))"""
                infinite_loop_control(servo2, ds3_val)
            
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
    os.system('sudo amixer cset numid=3 1')
    os.system('sudo amixer cset numid=1 400')
    os.system('sudo aplay /home/pi/Documents/electric_shovel/ics35_py/start.wav')
    os.system("sudo sixad -start &") # sixadのコマンド実行
    
    i = 0
    while True:
        i += 1
        try:
            ps3_control()
        except Exception as e:
            print("error:{e} retry:{i}".format(e=e, i=i))
            time.sleep(5)  # 5秒待つ
