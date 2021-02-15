import math
import struct
from typing import Tuple
from controller import Robot

TIME_STEP = 64
ROBOT_NAMES = ["B1", "B2", "B3", "Y1", "Y2", "Y3"]
N_ROBOTS = len(ROBOT_NAMES)


class RCJSoccerRobot:
    def __init__(self):
        # create the Robot instance.
        self.robot = Robot()
        self.name = self.robot.getName()
        self.team = self.name[0]
        self.player_id = int(self.name[1])

        self.receiver = self.robot.getDevice("receiver")
        self.receiver.enable(TIME_STEP)

        self.left_motor = self.robot.getDevice("left wheel motor")
        self.right_motor = self.robot.getDevice("right wheel motor")

        self.left_motor.setPosition(float('+inf'))
        self.right_motor.setPosition(float('+inf'))

        self.left_motor.setVelocity(0.0)
        self.right_motor.setVelocity(0.0)

    def parse_supervisor_msg(self, packet: str) -> dict:
        struct_fmt = 'ddd' * N_ROBOTS + 'dd'

        unpacked = struct.unpack(struct_fmt, packet)

        data = {}
        for i, r in enumerate(ROBOT_NAMES):
            if r[0] == "B":
                data[r] = {
                    "x": unpacked[3 * i],
                    "y": unpacked[3 * i + 1],
                    "orientation": unpacked[3 * i + 2]
                }
                data["ball"] = {
                    "x": unpacked[3 * N_ROBOTS],
                    "y": unpacked[3 * N_ROBOTS + 1]
                }
            else:
                data[r] = {
                    "x": -unpacked[3 * i],
                    "y": -unpacked[3 * i + 1],
                    "orientation": unpacked[3 * i + 2]
                }
                data["ball"] = {
                    "x": -unpacked[3 * N_ROBOTS],
                    "y": -unpacked[3 * N_ROBOTS + 1]
                }
        return data

    def get_new_data(self) -> dict:
        packet = self.receiver.getData()
        self.receiver.nextPacket()

        return self.parse_supervisor_msg(packet)

    def is_new_data(self) -> bool:
        return self.receiver.getQueueLength() > 0

    def get_angles(self, ball_pos: dict, robot_pos: dict) -> Tuple[float, float]:
        robot_angle: float = robot_pos['orientation']

        # Get the angle between the robot and the ball
        angle = math.atan2(
            ball_pos['y'] - robot_pos['y'],
            ball_pos['x'] - robot_pos['x'],
        )

        if angle < 0:
            angle = 2 * math.pi + angle

        if robot_angle < 0:
            robot_angle = 2 * math.pi + robot_angle

        robot_ball_angle = math.degrees(angle + robot_angle)
        robot_angle = math.degrees(robot_angle)

        # Axis Z is forward
        robot_angle += 90
        if (robot_angle > 360): robot_angle -= 360
        robot_ball_angle -= 90
        if robot_ball_angle > 360:
            robot_ball_angle -= 360

        return robot_ball_angle, robot_angle

    def run(self):
        raise NotImplementedError
