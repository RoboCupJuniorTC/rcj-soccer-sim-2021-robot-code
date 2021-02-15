import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
from rcj_soccer_player_b1 import rcj_soccer_robot
import utils
######

# Feel free to import built-in libraries
import math


class MyRobot(rcj_soccer_robot.RCJSoccerRobot):
    def gd(ball_angle: float) -> int:
        if ball_angle >= 345 or ball_angle <= 15:
            return 0
        return -1 if ball_angle < 180 else 1
    def run(self):
        while self.robot.step(rcj_soccer_robot.TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()

                # Get the position of our robot
                robot_pos = data[self.name]
                # Get the position of the ball
                ball_pos = data['ball']

                # Get angle between the robot and the ball
                # and between the robot and the north
                ball_angle, robot_angle = self.get_angles(ball_pos, robot_pos)

                # Compute the speed for motors
                direction = utils.get_direction(ball_angle)

                # If the robot has the ball right in front of it, go forward,
                # rotate otherwise
                if direction == 0:
                    left_speed = -5
                    right_speed = -5
                else:
                    left_speed = direction * 4
                    right_speed = direction * -4

                # Set the speed to motors
                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)


my_robot = MyRobot()
my_robot.run()
