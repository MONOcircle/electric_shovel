# -*- coding: utf-8 -*-
from MX12W import MX12W, BAUDRATE
from getch import _Getch

if __name__ == "__main__":
    rotate = MX12W("/dev/ttyUSB0", BAUDRATE.B1M, 1)

    if not rotate.open():
        print("Error: Can't open port [", "/dev/ttyUSB0", "]")
        sys.exit(1)

    rotate.set_wheel_mode()
    rotate.set_torque(MX12W.TORQUE_ON)

    getch = _Getch()
    print("START!!")
    while True:
        ikey = getch()
        if ikey == "a":
            rotate.set_wheel_speed(100) #CCW=0~1023 CW=1024~2047

        if ikey == "b":
            rotate.set_wheel_speed(1124) #CCW=0~1023 CW=1024~2047
            
        if ikey == '\x03': # <Ctrl-c>
            rotate.set_wheel_speed(0)
            rotate.set_torque(MX12W.TORQUE_OFF)
            break
        
