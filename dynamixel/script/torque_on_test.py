from MX12W import MX12W, BAUDRATE
import argparse
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("device_name", help="device_name")
    parser.add_argument("id", type=int, help="id")
    args = parser.parse_args()

    mx12w = MX12W(args.device_name, BAUDRATE.B115200, args.id)
    if not mx12w.open():
        print("Error: Can't open port [", args.device_name, "]")
        sys.exit(1)
    mx12w.set_torque(MX12W.TORQUE_ON)
