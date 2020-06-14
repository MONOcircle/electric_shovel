#!/usr/bin/env python3
#coding: utf-8

### 音声ファイルを再生する
### wavファイルのみ　再生可能
### wavファイルの配置場所は　"/home/pi/dev/"

import subprocess
import sys

args = sys.argv
filename = args[1]

# wavファイル再生コマンドを生成
cmd_play_sound = 'aplay' + ' ' + './dev/' + filename
# 再生コマンドを実行
subprocess.call(cmd_play_sound, shell=True)