import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
sys.path.append('/app/controllers')

# rcj_soccer_player controller - ROBOT B2

###### REQUIRED in order to import files from B1 controller
import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
# You can now import scripts that you put into the folder with your
# robot B1 controller
from team_026_libraries.robot1 import rcj_soccer_robot, utils
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
                
                polovica = 0 #ak je nula tak je na nasej polke
                             #ak je jedna tak je na superovej polke
                             
                #superova brana je robot_x -70
                #a robot_y je 18 az -18
                
  

                
    
                if robot_x < 25:
                    if (robot_x - 4) > ball_x:
                        if direction == 0:
                            left_speed = -10
                            right_speed = -10
                        else:
                            left_speed = direction * 10
                            right_speed = direction * -10
                    else:
                        if real_robot_angle <= 274:
                            if real_robot_angle >= 264: 
                                left_speed = 10
                                right_speed = 10
                            else:
                                left_speed = 3
                                right_speed = -3
                        else:
                            left_speed = -3
                            right_speed = 3
                else:
                    if real_robot_angle <= 274:
                        if real_robot_angle >= 264: 
                            left_speed = -10
                            right_speed = -10
                        else:
                            left_speed = 3
                            right_speed = -3
                    else:
                        left_speed = -3
                        right_speed = 3
                

                # Set the speed to motors
                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)


my_robot = MyRobot()
my_robot.run()
