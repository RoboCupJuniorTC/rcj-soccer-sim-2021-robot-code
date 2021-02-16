# NT from Japn

# rcj_soccer_player controller - robot2
# By Akitoshi Saeki,Tomoki Takaba

###### REQUIRED in order to import files from B1 controller
import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
# You can now import scripts that you put into the folder with your
# robot B1 controller
from team_015_libraries.robot1 import rcj_soccer_robot, utils
######

# Feel free to import built-in libraries
import math


class MyRobot(rcj_soccer_robot.RCJSoccerRobot):
    start_angle=None
    robot_originalangle=None
    back=0
    l=0
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
                if self.start_angle is None:
                    self.start_angle=math.degrees(robot_angle)
                
                self.robot_originalangle=self.start_angle-math.degrees(robot_angle)
                if self.robot_originalangle < 0:
                    self.robot_originalangle=self.robot_originalangle+360
                if self.robot_originalangle >= 180:
                    self.robot_originalangle=-(360-self.robot_originalangle)
                ##print(self.robot_originalangle)

                
                # Compute the speed for motors
                direction = utils.get_direction(ball_angle)

                # If the robot has the ball right in front of it, go forward,
                # rotate otherwise
                if robot_pos['x']-ball_pos['x']<0.2:
                    if self.back==1:
                        dir_ball=0
                        if ball_angle<180:
                            extra=180-ball_angle
                            if 180-ball_angle>30:
                                print(self.robot_originalangle)
                                if self.robot_originalangle>-45:
                                    if self.l==0:
                                        dir_ball=utils.get_direction(180+ball_angle+extra*0.8)
                                else:
                                    self.l=1
                                    dir_ball=utils.get_direction(30)
                            else:
                                dir_ball=0
                        if ball_angle>180:
                            extra=180-ball_angle
                            if 180-ball_angle<-30:
                                if self.robot_originalangle<45:
                                    if self.l==0:
                                        dir_ball=utils.get_direction(180-ball_angle-extra*0.8)
                                else:
                                    dir_ball=utils.get_direction(330)
                            else:
                                dir_ball=0
                        if dir_ball==0:
                                left_speed = 10
                                right_speed = 10
                        else:
                            left_speed=dir_ball*10
                            right_speed=dir_ball*-10
                    if robot_pos['x']-ball_pos['x']<0:
                        self.back=1
                        if abs(self.robot_originalangle)<20:
                            left_speed = 10
                            right_speed = 10
                        else:
                            left_speed=self.robot_originalangle
                            right_speed=-self.robot_originalangle
                    else:
                        if self.back==1:
                            dir_ball=0
                            if ball_angle<180:
                                extra=180-ball_angle
                                if 180-ball_angle>30:
                                    print(self.robot_originalangle)
                                    if self.robot_originalangle>-45:
                                        if self.l==0:
                                            dir_ball=utils.get_direction(180+ball_angle+extra*0.8)
                                    else:
                                        self.l=1
                                        dir_ball=utils.get_direction(30)
                                else:
                                    dir_ball=0
                            if ball_angle>180:
                                extra=180-ball_angle
                                if 180-ball_angle<-30:
                                    if self.robot_originalangle<45:
                                        if self.l==0:
                                            dir_ball=utils.get_direction(360-ball_angle+abs(extra)*0.8)
                                            print(360-ball_angle)
                                            print(dir_ball)
                                    else:
                                        self.l=1
                                        dir_ball=utils.get_direction(330)
                                else:
                                    dir_ball=0
                            if dir_ball==0:
                                    left_speed = 10
                                    right_speed = 10
                            else:
                                left_speed=dir_ball*10
                                right_speed=dir_ball*-10
                        else:
                            if direction == 0:
                                left_speed = -10
                                right_speed = -10
                            else:
                                left_speed = direction * 10
                                right_speed = direction * -10
                else:
                    self.back=0
                    if direction == 0:
                        left_speed = -10
                        right_speed = -10
                    else:
                        left_speed = direction * 10
                        right_speed = direction * -10

                # Set the speed to motors
                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)


my_robot = MyRobot()
my_robot.run()
