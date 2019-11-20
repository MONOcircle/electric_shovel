# GPIOを制御するライブラリ
import wiringpi
# タイマーのライブラリ
import time

# GPIOの端子番号
motor1_pin1 = 17
motor1_pin2 = 27
motor2_pin1 = 22
motor2_pin2 = 10
motor3_pin1 = 9
motor3_pin2 = 11

# GPIO初期化
wiringpi.wiringPiSetupGpio()
# GPIOを出力モード（1）に設定
wiringpi.pinMode( motor1_pin1, 1 )
wiringpi.pinMode( motor1_pin2, 1 )
wiringpi.pinMode( motor2_pin1, 1 )
wiringpi.pinMode( motor2_pin2, 1 )
wiringpi.pinMode( motor3_pin1, 1 )
wiringpi.pinMode( motor3_pin2, 1 )

# whileの無限ループ
while True:
# GPIOを3.3V
    wiringpi.digitalWrite( motor1_pin1, 1 )
    wiringpi.digitalWrite( motor1_pin2, 0 )
    wiringpi.digitalWrite( motor2_pin1, 1 )
    wiringpi.digitalWrite( motor2_pin2, 0 )
    wiringpi.digitalWrite( motor3_pin1, 1 )
    wiringpi.digitalWrite( motor3_pin2, 0 )