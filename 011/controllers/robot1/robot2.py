# rcj_soccer_player controller - ROBOT B2

###### REQUIRED in order to import files from B1 controller
import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
# You can now import scripts that you put into the folder with your
# robot B1 controller
from rcj_soccer_player_b1 import rcj_soccer_robot, utils
######

# Feel free to import built-in libraries
import math


class MyRobot(rcj_soccer_robot.RCJSoccerRobot):
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
                robx=robot_pos['x']
                roby=robot_pos['y']
                ballx=ball_pos['x']
                bally=ball_pos['y']
                robori = round(robot_angle, 1)
                color = self.team

                if color == 'Y':
                    if robx > 0:
                        if robori > 1.6:
                            left=-2
                            right=2
                        elif robori < 1.6:
                            left=2
                            right=-2
                        else:
                            left=5
                            right=5
                    elif ballx <= -.3:
                        if robx > -.68:
                            if robori > 1.7:
                                left=-2
                                right=2
                            elif robori < 1.5:
                                left=2
                                right=-2
                            else:
                                left=5
                                right=5
                        elif robori > 3.1:
                            left=-2
                            right=2
                        elif robori < 3.1:
                            left=2
                            right=-2
                        elif robori == 3.1:
                            if bally < roby:
                                left=-5
                                right=-5
                            elif bally > roby:
                                left=5
                                right=5
                            else:
                                left=0
                                right=0
                    elif ballx <= 0:
                        if direction == 0:
                            left = -5
                            right = -5
                        else:
                            left = direction * 5
                            right = direction * -5
                    else:
                        if robori > 3.1:
                            left=-2
                            right=2
                        elif robori < 3.1:
                            left=2
                            right=-2
                        elif robori == 3.1:
                            if bally > roby:
                                left=5
                                right=5
                            elif bally < roby:
                                left=-5
                                right=-5
                            else:
                                left=0
                                right=0
                                
                if color == 'B':
                    if robx < 0:
                        if robori > 1.6:
                            left=-2
                            right=2
                        elif robori < 1.6:
                            left=2
                            right=-2
                        else:
                            left=-5
                            right=-5
                    elif ballx >= .3:
                        if robx < .6:
                            if robori > 1.7:
                                left=-2
                                right=2
                            elif robori < 1.7:
                                left=2
                                right=-2
                            else:
                                left=-5
                                right=-5
                        elif robori > 3.1:
                            left=-2
                            right=2
                        elif robori < 3.1:
                            left=2
                            right=-2
                        elif robori == 3.1:
                            if bally < roby:
                                left=-5
                                right=-5
                            elif bally > roby:
                                left=5
                                right=5
                            else:
                                left=0
                                right=0
                    elif ballx >= 0:
                        if direction == 0:
                            left = -5
                            right = -5
                        else:
                            left = direction * 5
                            right = direction * -5
                    else:
                        if robori > 3.1:
                            left=-2
                            right=2
                        elif robori < 3.1:
                            left=2
                            right=-2
                        elif robori == 3.1:
                            if bally < roby:
                                left=-5
                                right=-5
                            elif bally > roby:
                                left=5
                                right=5
                            else:
                                left=0
                                right=0
                
                # Set the speed to motors
                self.left_motor.setVelocity(left)
                self.right_motor.setVelocity(right)


my_robot = MyRobot()
my_robot.run()
