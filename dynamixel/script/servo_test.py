from MX12W import MX12W, BAUDRATE
import argparse
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("device_name", help="device_name")
    parser.add_argument("id", type=int, help="id")
    args = parser.parse_args()

    mx12w = MX12W(args.device_name, BAUDRATE.B1M, args.id)
    if not mx12w.open():
        print("Error: Can't open port [", args.device_name, "]")
        sys.exit(1)
    #mx12w.set_joint_mode()
    mx12w.set_wheel_mode()
    #mx12w.set_multi_turn_mode()
    mx12w.set_torque(MX12W.TORQUE_ON)
    #mx12w.set_raw_position(48672)
    mx12w.set_wheel_speed(100) #CCW=0~1023 CW=1024~2047
    # while True:
        # angle = mx12w.get_position()
        # print(angle)
