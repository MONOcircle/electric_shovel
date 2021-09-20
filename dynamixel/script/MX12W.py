#!/usr/bin/env python3

from dynamixel_sdk import PacketHandler, PortHandler, COMM_SUCCESS

from enum import IntEnum, unique


@unique
class BAUDRATE(IntEnum):
    B2M = 0
    B1M = 1
    B500000 = 3
    B400000 = 4
    B250000 = 7
    B200000 = 9
    B115200 = 16
    B57600 = 34
    B19200 = 103
    B9600 = 207


class MX12W:
    ADDR_TORQUE_ENABLE = 24
    ADDR_GOAL_POSITION = 30
    ADDR_PRESENT_POSITION = 36
    ADDR_MOVING_SPEED = 32
    ADDR_CW_ANGLE_LIMIT = 6
    ADDR_CCW_ANGLE_LIMIT = 8
    PROTOCOL_VERSION = 1.0
    TORQUE_ON = 1
    TORQUE_OFF = 0

    def __init__(self, device_name, baudrate, servo_id):
        self.device_name = device_name
        self.port_handler = PortHandler(self.device_name)
        self.packet_handler = PacketHandler(self.PROTOCOL_VERSION)
        self.set_baudrate(baudrate)
        self.set_id(servo_id)

    def set_id(self, servo_id):
        self.servo_id = int(servo_id)

    def set_baudrate(self, baudrate):
        self.baudrate = int(baudrate)
        b_value = round((2000000/baudrate)-1)
        self.port_handler.setBaudRate(b_value)

    def open(self):
        if self.port_handler.openPort():
            return True
        else:
            return False

    def set_joint_mode(self):
        self.packet_handler.write2ByteTxRx(
            self.port_handler, self.servo_id, self.ADDR_CW_ANGLE_LIMIT,0)
        self.packet_handler.write2ByteTxRx(
            self.port_handler, self.servo_id, self.ADDR_CCW_ANGLE_LIMIT,4095)

    def set_wheel_mode(self):
        self.packet_handler.write2ByteTxRx(
            self.port_handler, self.servo_id, self.ADDR_CW_ANGLE_LIMIT,0)
        self.packet_handler.write2ByteTxRx(
            self.port_handler, self.servo_id, self.ADDR_CCW_ANGLE_LIMIT,0)

    def set_multi_turn_mode(self):
        self.packet_handler.write2ByteTxRx(
            self.port_handler, self.servo_id, self.ADDR_CW_ANGLE_LIMIT,4095)
        self.packet_handler.write2ByteTxRx(
            self.port_handler, self.servo_id, self.ADDR_CCW_ANGLE_LIMIT,4095)

    def set_torque(self, t):
        dxl_comm_result, dxl_error = self.packet_handler.write1ByteTxRx(
            self.port_handler, self.servo_id, self.ADDR_TORQUE_ENABLE, t)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packet_handler.getTxRxResult(dxl_comm_result))
            return False
        elif dxl_error != 0:
            print("%s" % self.packet_handler.getRxPacketError(dxl_error))
            return False
        else:
            return True

    def set_center(self):
        self.set_raw_position(2048)

    def set_position(self, pos):
        p_value = (pos+180.224)/0.088
        self.set_raw_position(p_value)

    def set_raw_position(self, pos):
        dxl_comm_result, dxl_error = self.packet_handler.write2ByteTxRx(
            self.port_handler, self.servo_id, self.ADDR_GOAL_POSITION, pos)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packet_handler.getTxRxResult(dxl_comm_result))
            return False
        elif dxl_error != 0:
            print("%s" % self.packet_handler.getRxPacketError(dxl_error))
            return False
        else:
            return True

    def set_wheel_speed(self,speed):
        dxl_comm_result, dxl_error = self.packet_handler.write2ByteTxRx(
            self.port_handler, self.servo_id, self.ADDR_MOVING_SPEED, speed)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packet_handler.getTxRxResult(dxl_comm_result))
            return False
        elif dxl_error != 0:
            print("%s" % self.packet_handler.getRxPacketError(dxl_error))
            return False
        else:
            return True

    def get_position(self):
        pos = self.get_raw_position()
        return pos*0.088-0.224

    def get_raw_position(self):
        dxl_present_position, dxl_comm_result, dxl_error = self.packet_handler.read2ByteTxRx(
            self.port_handler, self.servo_id, self.ADDR_PRESENT_POSITION)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packet_handler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packet_handler.getRxPacketError(dxl_error))
        return dxl_present_position
