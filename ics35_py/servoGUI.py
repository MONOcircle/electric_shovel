import serialServo
import sys
import serial
import Tkinter as tk

con = None

con = serial.Serial("/dev/ttyUSB0",
                    115200,
                    parity=serial.PARITY_EVEN,
                    stopbits=serial.STOPBITS_ONE,
                    timeout=1)
servo = serialServo.Servo(con, "0", 10)


def scaleFunc(event):
    deg = scale1.get()
    posBuff.set(str(deg))
    servo.Pos(deg)


def setPos(event):
    if posBuff.get():
        value = float(posBuff.get())
        scale1.set(value)
        servo.Pos(value)


def selectAdd(event):
    global add
    if buffer.get():
        add = int(buffer.get())
        servo.addr = add
        addLabel.configure(text="address:" + str(add))


def setPort(event):
    global servo
    value = portBuff.get()
    serialServo.SetSerial(value)
    servo = serialServo.Servo(add)
    portLabel.configure(text="selected port")


add = 0
# servo = None

root = tk.Tk()

portLabel = tk.Label(root, text="don't select port")
portLabel.pack()
portBuff = tk.StringVar()
portBuff.set("/dev/ttyUSB0")

portEntry = tk.Entry(root, textvariable=portBuff)
portEntry.pack()
portEntry.bind("<Return>", setPort)

buffer = tk.StringVar()
buffer.set(str(add))

posBuff = tk.StringVar()
posBuff.set("0")

scale1 = tk.Scale(root,
                  label="servo position",
                  orient="h",
                  from_=0.0, to=270.0, resolution=0.1,
                  command=scaleFunc)
scale1.pack()

posEntry = tk.Entry(root, textvariable=posBuff)
posEntry.pack()
posEntry.bind("<Return>", setPos)

addLabel = tk.Label(root, text="address:0")
addLabel.pack()

addEntry = tk.Entry(root, textvariable=buffer)
addEntry.pack()
addEntry.bind("<Return>", selectAdd)

root.mainloop()
servo.con.close()
