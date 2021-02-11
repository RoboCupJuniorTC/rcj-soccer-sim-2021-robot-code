# rcj_soccer_player controller - ROBOT B1

# Feel free to import built-in libraries
import math

# You can also import scripts that you put into the folder with controller
from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP
import utils


class MyRobot(RCJSoccerRobot):
    def run(self):
        while self.robot.step(TIME_STEP) != -1:
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
            
                # easier variables to type
                robx=robot_pos['x']
                roby=robot_pos['y']
                ballx=ball_pos['x']
                bally=ball_pos['y']
                robori = round(robot_angle, 1)
                color = self.team

                if color == 'Y':
                    if robx > -.60 and robori == 1.6:
                        left=5
                        right=5
                    elif robori > 3.1:
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
                    if robx < .64:
                        if robori == 4.7:
                            left=5
                            right=5
                        elif robori > 4.7:
                            left=-2
                            right=2
                        else:
                            left=2
                            right=-2
                    if robx >= .64 and robx < .7:
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
                    elif robx == .7:
                        left=-5
                        right=-3
                    elif ballx > .46 and robx < .75: #Check if ball is passing danger zone and if Geoff is already in position
                        if roby > -1.5:
                            if roby < 1.5: #Check if already in place for Super Geoff
                                if robori < 4.7:
                                    left=2
                                    right=-2
                                if robori == 4.7 and robx != .75:
                                    left=3
                                    right=3 
                                if robx == .75: #If Geoff in position, run Geoff code
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
                            elif roby < -1.5:
                                left=-5
                                right=-5
                            elif roby > 1.5:
                                left=5
                                right=5
                # Set the speed to motors
                self.left_motor.setVelocity(left)
                self.right_motor.setVelocity(right)


my_robot = MyRobot()
my_robot.run()
