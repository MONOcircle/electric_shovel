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
    print(_angle)

    # A: Up, B: Down
    if ikey == "A":
        _angle = servo.Pos(_angle + 5)

    if ikey == "B":
        _angle = servo.Pos(_angle - 5)

    if ikey == '\x03': # <Ctrl-c>
        break

servo.con.close()


# def scaleFunc(event):
#     deg = scale1.get()
#     posBuff.set(str(deg))
#     servo.Pos(deg)
# 
# 
# def setPos(event):
#     if posBuff.get():
#         value = float(posBuff.get())
#         scale1.set(value)
#         servo.Pos(value)
# 
# 
# def selectAdd(event):
#     global add
#     if buffer.get():
#         add = int(buffer.get())
#         servo.addr = add
#         addLabel.configure(text="address:" + str(add))
# 
# 
# def setPort(event):
#     global servo
#     value = portBuff.get()
#     serialServo.SetSerial(value)
#     servo = serialServo.Servo(add)
#     portLabel.configure(text="selected port")
# 
# 
# add = 0
