# rcj_soccer_player controller - ROBOT B1

# Feel free to import built-in libraries
import math

# You can also import scripts that you put into the folder with controller
from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP
import utils

import time


a = 0
b = 0

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

                # If the robot has the ball right in front of it, go forward,
                # rotate otherwise
                #if direction == 0:
                #    left_speed = -5
                #    right_speed = -5
                #else:
                #    left_speed = direction * 4
                #    right_speed = direction * -4

                real_robot_angle = robot_angle*57
                
                robot_x = robot_pos["x"]*100
                robot_y = robot_pos["y"]*100
                
                ball_x = ball_pos["x"]*100
                ball_y = ball_pos["y"]*100
                
                
                if ball_x >= 25:
                    if direction == 0:
                        left_speed = -10
                        right_speed = -10
                        global b
                        b = 0
                    else:
                        left_speed = direction * 10
                        right_speed = direction * -10
                else:
                    if robot_y <= 5:
                        if robot_y >= -5:
                            if real_robot_angle <= 274:
                                if real_robot_angle >= 264:
                                    if robot_x > 70:
                                        left_speed = 0
                                        right_speed = 0
                                        global a
                                        if a == 0:
                                            start_time1 = time.time()
                                            a = 1
                                        else:
                                            if(time.time() - start_time1) > 4:
                                                if robot_x > 50:
                                                        left_speed = -10
                                                        right_speed = -10
                                                        b = 1
                                                else:
                                                    start_time1 = time.time()
                                                    b = 0
      
                                    else:
                                        if b == 1:
                                            if robot_x > 50:
                                                left_speed = -10
                                                right_spedd = -10
                                            else:
                                                
                                                left_speed = 10
                                                right_speed = 10
                                                b = 0
                                                a = 0
                                        else:
                                            left_speed = 10
                                            right_speed = 10
                                            b = 0
                                else:
                                    left_speed = 3
                                    right_speed = -3
                            else:
                                left_speed = -3
                                right_speed = 3
                        else:
                            if real_robot_angle >= 177:
                                if real_robot_angle <= 181:
                                    left_speed = 10
                                    right_speed = 10
                                else:
                                    left_speed = -3
                                    right_speed = 3
                            else:
                                left_speed = 3
                                right_speed = -3
                                
                    else:
                        if real_robot_angle >= 176:
                            if real_robot_angle <= 182:
                                left_speed = -10
                                right_speed = -10
                            else:
                                left_speed = -3
                                right_speed = 3
                        else:
                            left_speed = 3
                            right_speed = -3
                                                
                # Set the speed to motors
                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)
                
                
my_robot = MyRobot()
my_robot.run()
