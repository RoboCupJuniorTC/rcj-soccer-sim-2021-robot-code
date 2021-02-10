# rcj_soccer_player controller - ROBOT Y2

###### REQUIRED in order to import files from Y1 controller
import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
# You can now import scripts that you put into the folder with your
# robot B1 controller
from robot1 import rcj_soccer_robot, utils
######

# Feel free to import built-in libraries
import math


class MyRobot(rcj_soccer_robot.RCJSoccerRobot):
    def __init__(self):
        super().__init__()
        self.__start = False
        self.__forward = -1
        self.__ori = 0
        self.__role = ""
        
    def run(self):
        while self.robot.step(rcj_soccer_robot.TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()

                # Get the position of our robot
                robot_pos = data[self.name]
                # Get the position of the ball
                ball_pos = data['ball']

                if self.__start == False:
                    self.__ori = robot_pos['orientation']

                ball_angle, robot_angle, distance = self.get_angles(ball_pos, robot_pos)

                pos  = {"bot":robot_pos, "ball":ball_pos}
                ball = {"angle": ball_angle, "distance": math.sqrt((ball_pos['y'] - robot_pos['y'])**2 + (ball_pos['x'] - robot_pos['x'])**2)}
                left_speed, right_speed = utils.ploy(self.name[0], "", self.__ori, pos, ball)
                
                # Set the speed to motors
                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)
                self.__start = True


my_robot = MyRobot()
my_robot.run()
