# ics3.5_for_python

これはpythonから近藤科学のKRS-6003RHV(以下サーボ）を制御するためのパッケージです．  
raspberry piからの制御を基準で考えています．しかし，FT232RLのUSBシリアル変換モジュールなどを使えばPCからでも制御が可能です．

ラズパイ(Linux)からシリアルUSBアダプター経由で、KONDOサーボを動かすには下記の設定が必要です。
https://kondo-robot.com/faq/usb_adapter_for_linux_2019

ICS3.5コマンドリファレンス（サーボの動かし方）
https://kondo-robot.com/faq/ics3-5_softwaremanual_1

## modules
### serialServo
 このモジュールは実際にサーボを制御するためのものです．

#### def SetSerial(port)  
サーボモータと通信するためのポートを選択する関数です．デフォルトで/dev/ttyAMA0ポートと接続されます．引数を与えることで任意のポートと接続できます．

#### class Servo(address, angle)
サーボを制御するクラスです．引数にはサーボのアドレスと初期角度を与えます．初期角度を与えないとサーボはフリーの状態となります．
##### method GetId() return address
サーボのアドレスを取得します．

##### method Pos(angle) return bef_angle
サーボの角度を制御するメソッドです．0.0から270.0[deg]でサーボの角度を与えてやります．分解能は0.03[deg]程度です．戻り値は前の角度です．

#### method GetPos() return angle
サーボの現在の角度を取得します．

### setid
このモジュールはサーボのid設定用のモジュールです．

### servoGUI
このモジュールはサーボ単体を簡単に操作できるGUIツールです．


### PS3コントローラの接続
ゲームコントローラーを USB で RasPi につなげて、PSボタンを押して(1のみ点灯)から
sudo sixpair
を実行しペアリングする。

正しくペアリングされれば下記のメッセージが表示される。
Current Bluetooth master:MACアドレス
Setting master bd_addr to:MACアドレス

ゲームコントローラーをRasPiから外し、
`sudo sixad -start &`
を実行
[....] Starting bluetooth (via systemctl): blue[ ok .service.
sixad-bin[6327]: started
sixad-bin[6327]: sixad started, press the PS button now

のあとにPSボタンを押す
