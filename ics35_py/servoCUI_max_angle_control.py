import serialServo
import sys
import serial
import time
from getch import _Getch

con = None

con = serial.Serial("/dev/ttyUSB0",
                    115200,
                    parity=serial.PARITY_EVEN,
                    stopbits=serial.STOPBITS_ONE,
                    timeout=1)

servo = serialServo.Servo(con, "0", 10)

_angle = servo.GetPos()
getch = _Getch()
while True:
    ikey = getch()

    # A: Up, B: Down
    if ikey == "A":
        _pos = servo.Pos(serialServo.MAX_ANGLE)
    elif ikey == "B":
        _pos = servo.Pos(serialServo.MIN_ANGLE)
    else:
        _pos = servo.Pos(servo.GetPos())
        _pos = servo.Pos(_pos)
    print(_pos)

    if ikey == '\x03': # <Ctrl-c>
        break

servo.con.close()

