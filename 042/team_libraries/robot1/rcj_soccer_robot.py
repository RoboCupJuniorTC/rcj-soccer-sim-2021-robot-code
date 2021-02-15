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
        self.robot = Robot()                                            #建立robot
        self.name = self.robot.getName()                                #讀名字   ex:B1
        self.team = self.name[0]                                        #讀隊伍      B
        self.player_id = int(self.name[1])                              #讀號碼       1

        self.receiver = self.robot.getDevice("receiver")
        self.receiver.enable(TIME_STEP)

        self.left_motor = self.robot.getDevice("left wheel motor")      #指定class裡"左馬達"變數
        self.right_motor = self.robot.getDevice("right wheel motor")    #指定class裡"右馬達"變數

        self.left_motor.setPosition(float('+inf'))                      #初始角度應設為infinity 單位:(-PI, +PI)
        self.right_motor.setPosition(float('+inf'))

        self.left_motor.setVelocity(0.0)                                #設置速度 單位:(rad/s)
        self.right_motor.setVelocity(0.0)

    def parse_supervisor_msg(self, packet: str) -> dict:
        """Parse message received from supervisor

        Returns:
            dict: Location info about each robot and the ball.
            Example:
                {
                    'B1': {'x': 0.0, 'y': 0.2, 'orientation': 1},
                    'B2': {'x': 0.4, 'y': -0.2, 'orientation': 1},
                    ...
                    'ball': {'x': -0.7, 'y': 0.3}
                }
        """
        # X, Z and rotation for each robot
        # plus X and Z for ball
        struct_fmt = 'ddd' * N_ROBOTS + 'dd'

        unpacked = struct.unpack(struct_fmt, packet)            #解析全場資料
        data = {}
        for i, r in enumerate(ROBOT_NAMES):                     #將資料寫成字典格式
            data[r] = {                                         #機子名稱對應自身座標+角度
                "x": unpacked[3 * i],
                "y": unpacked[3 * i + 1],
                "orientation": unpacked[3 * i + 2]
            }
            data["ball"] = {                                    #球座標
                "x": unpacked[3 * N_ROBOTS],
                "y": unpacked[3 * N_ROBOTS + 1]
            }
        
        return data

    def get_new_data(self) -> dict:                                                 #讀Queue最前面的data
        """Read new data from supervisor

        Returns:
            dict: See `parse_supervisor_msg` method
        """
        packet = self.receiver.getData()
        self.receiver.nextPacket()

        return self.parse_supervisor_msg(packet)

    def is_new_data(self) -> bool:                                                  #確認Queue是否Empty
        """Check if there are new data to be received 

        Returns:
            bool: Whether there is new data received from supervisor.
        """
        return self.receiver.getQueueLength() > 0

    def get_angles(self, ball_pos: dict, robot_pos: dict) -> Tuple[float, float]:
        """Get angles in degrees.

        Args:
            ball_pos (dict): Dict containing info about position of the ball
            robot_pos (dict): Dict containing info about position and rotation
                of the robot

        Returns:
            :rtype: (float, float):
                Angle between the robot and the ball
                Angle between the robot and the north
        """
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
        robot_angle = 360 - (math.degrees(robot_angle) + 90)

        # Axis Z is forward
        # TODO: change the robot's orientation so that X axis means forward
        robot_ball_angle -= 90
        if robot_ball_angle > 360:
            robot_ball_angle -= 360

        distance = math.sqrt((ball_pos['y'] - robot_pos['y'])**2 + (ball_pos['x'] - robot_pos['x'])**2)
        return robot_ball_angle, robot_angle, distance  
                                                        #單位:deg
                                                        #robot_ball     robot_deg
                                                        #     F              F
                                                        #     0              0   
                                                        #270      90    270     90  
                                                        #    180            180
    def run(self):
        raise NotImplementedError
