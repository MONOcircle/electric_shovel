# dynamixel

# INSTALL

* Dynamixel SDKをインストール

```
git clone https://github.com/ROBOTIS-GIT/DynamixelSDK.git
cd DynamixelSDK/python
python setup.py install
pip install argparse
```

# TORQUE TEST

```
cd script
python torque_on_test.py device_name id
python torque_off_test.py device_name id
```

* device_name: "/dev/ttyUSB0" など
* id: サーボのID