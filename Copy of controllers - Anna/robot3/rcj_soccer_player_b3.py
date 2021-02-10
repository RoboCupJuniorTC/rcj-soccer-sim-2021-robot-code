# rcj_soccer_player controller - ROBOT B3

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
               print(data['ball']['x']) 
               print(data['ball']['y'])
               print(data[self.name]['x'])
               print(data[self.name]['y'])

               ballx = (data['ball']['x'])                               
               bally = (data['ball']['y'])
               
               if self.name == 'B3':
                  x = 1
               else:
                  x = -1

               
               if direction == 0 and ballx * x >= 0.2791914652628236 and bally >= -0.35046926081602137 and bally <= 0.33868517936403864:
                  left_speed = -10 
                  right_speed = -10 
               elif (data[self.name]['x']) * x <= 0.6645016713541059 and ballx * x <= 0.320005904669597 and bally >= -0.35046926081602137 and bally <= 0.33868517936403864:
                  left_speed = 10 
                  right_speed = 10  
               elif ballx * x >= 0.6119832718662479:
                  left_speed = 0
                  right_speed = 0 
               else:
                  left_speed = direction * 4
                  right_speed = direction * -4

               

                # Set the speed to motors
               self.left_motor.setVelocity(left_speed)
               self.right_motor.setVelocity(right_speed)


my_robot = MyRobot()
my_robot.run()
