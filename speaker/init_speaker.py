#!/usr/bin/env python3
#coding: utf-8

import wiringpi
import subprocess

speaker_pin = 13

wiringpi.wiringPiSetupGpio()

# GPIO 13番ピンをPWMモードに変更
wiringpi.pinMode(speaker_pin, 2)    # wiringpi.PWM_OUTPUT = 2

# PCM Playback Route(numid=3) を3.5mmジャック、GPIOピン(1)に設定する
subprocess.call('amixer cset numid=3 1', shell=True)

# PCM Playback Volume(numid=1) を設定する(ミュート-10239〜最大400)
# 負の値を設定する場合は　値の前に　"--"(マイナスを2個)　を記載する
subprocess.call('amixer cset numid=1 -- -4000', shell=True)
