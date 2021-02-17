import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
sys.path.append('/app/controllers')

# rcj_soccer_player controller - ROBOT B1

# Feel free to import built-in libraries
import math

# You can also import scripts that you put into the folder with controller
from team_054_libraries.robot1.rcj_soccer_robot import RCJSoccerRobot, TIME_STEP
from team_054_libraries.robot1 import utils

goalie = "1"
mid = "2"
strike = "3"

class MyRobot(RCJSoccerRobot):
    def to_goal(self):
        switch = False
        turned = False
        moved = False
        corrected = False
        while self.robot.step(TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()
                mult = 1
                if self.name[0] == "Y": mult = -1
                robot_pos = data[self.name]
                
                #variables for yellow switch
                spin1 = 3
                spin2 = 2.5
                turn_val = 2

                x = robot_pos['x']
                if x <= 0: x = abs(x) + 0.75
                y = robot_pos['y']
                if y < 0:
                    y = abs(y)
                    if not switch:
                        spin1 = -spin1
                        spin2 = -spin2
                        turn_val = -turn_val
                        switch = True

                tang = 180 + math.degrees(math.atan2(x, y))
                if corrected: tang -= 90

                #if (yellow or shitty) and not (yellow and shitty)
                
                if (self.get_angles(data['ball'], robot_pos)[1] > tang + turn_val or self.get_angles(data['ball'], robot_pos)[1] < tang - turn_val) and not turned: #turn to center of goal'
                    self.left_motor.setVelocity(-spin1 * mult)
                    self.right_motor.setVelocity(spin1 * mult)
                else: turned = True
                if robot_pos['x'] < 0.725 and turned and not moved: #go to goal line
                    self.left_motor.setVelocity(-10 * mult)
                    self.right_motor.setVelocity(-10 * mult)
                    if robot_pos['y'] <= 0 and robot_pos['x'] <= 0.75 and not corrected: # Correct the movement
                        turned = False
                        corrected = True
                elif turned: moved = True
                if self.get_angles(data['ball'], robot_pos)[1] < tang + (90 - (tang-180)) and moved: #rotate to side
                    self.right_motor.setVelocity(-spin2 * mult)
                    self.left_motor.setVelocity(spin2 * mult)
                elif moved and self.get_angles(data['ball'], robot_pos)[1] > tang + (90 - (tang-180)) + 1.75:
                    self.right_motor.setVelocity(1 * mult)
                    self.left_motor.setVelocity(-1 * mult)
                elif moved:
                    self.right_motor.setVelocity(0 * mult)
                    self.left_motor.setVelocity(0 * mult)
                    return self.defend()
                    
    def defend(self):
        while self.robot.step(TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()
                mult = 1
                if self.name[0] == "Y": mult = -1
                x = data[self.name]['x']

                direction = utils.get_direction(self.get_angles(data['ball'], data[self.name])[0])
                if x < 0.55:
                    return utils.new_roles(data, self.name)
                if data[self.name]['y'] >= 0.2 - 0.075/2 - 0.05 and direction == -1:
                    self.right_motor.setVelocity(-5 * mult)
                    self.left_motor.setVelocity(-5 * mult)
                elif data[self.name]['y'] <= -0.2 + 0.075/2 + 0.05 and direction == 1:
                    self.left_motor.setVelocity(5 * mult)
                    self.right_motor.setVelocity(5 * mult)
                else:
                    self.right_motor.setVelocity(direction * -5 * mult)
                    self.left_motor.setVelocity(direction * -5 * mult)

    def strike(self):
        at_ball = False
        global striker
        while self.robot.step(TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()
                mult = 1
                if self.name[0] == "Y": mult = -1
                if self.name[1] != striker:
                    return
                elif not at_ball:
                    #turn towards ball
                    bx = data['ball']['x']
                    if bx <= 0: bx = 0.75 - bx
                    by = data['ball']['y']

                    rx = data[self.name]['x']
                    if rx <= 0: rx = 0.75 - rx
                    ry = data[self.name]['y']

                    ball_angle = self.get_angles(data['ball'], data[self.name])[0]
                    ball_add = 2
                    if ball_angle >= 345 or ball_angle <= 15:
                        direction = 0
                    elif ball_angle < 355: direction = -1
                    else:
                        direction = 1
                        ball_add = -2

                    if direction == 0:
                        self.right_motor.setVelocity(-10 * mult)
                        self.left_motor.setVelocity(-10 * mult)
                    elif direction != 0:
                        self.right_motor.setVelocity(direction * -4 * mult)
                        self.left_motor.setVelocity(direction * 4 * mult)
                    if rx/(bx+0.01) > ry/(by+0.01) + 0.1 and rx/(bx+0.01) < ry/(by+0.01) - 0.1:
                        at_ball = True
                else:
                    if data[self.name]['x'] == -0.75:
                        at_ball = False
                    else:
                        print('here i am')
                        self.right_motor.setVelocity(-10 * mult)
                        self.left_motor.setVelocity(-10 * mult)

    def mid(self):
        global mid
        while self.robot.step(rcj_soccer_robot.TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()
                mult = 1
                if self.name[0] == "Y": mult = -1
                if self.name[1] != mid:
                    return
                else:

                    # Get the position of our robot
                    robot_pos = data[self.name]
                    # Get the position of the ball
                    ball_pos = data['ball']

                    # Get angle between the robot and the ball
                    # and between the robot and the north
                    ball_angle, robot_angle = self.get_angles(ball_pos, robot_pos)

                    # Compute the speed for motors
                    direction = self.gd(ball_angle)

                    # If the robot has the ball right in front of it, go forward,
                    # rotate otherwise
                    if direction == 0:
                        left_speed = -5
                        right_speed = -5
                    else:
                        left_speed = direction * 4
                        right_speed = direction * -4

                    # Set the speed to motors
                    self.left_motor.setVelocity(left_speed * mult)
                    self.right_motor.setVelocity(right_speed * mult)

    def gd(ball_angle: float) -> int:
        if ball_angle >= 345 or ball_angle <= 15:
            return 0
        return -1 if ball_angle < 180 else 1

    def run(self):
        global goalie
        global mid
        global striker
        while self.robot.step(TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()

                if self.name[1] == goalie:
                    print('goalie')
                    goalie, striker, mid = self.to_goal()
                elif self.name[1] == striker:
                    print('striker')
                    self.strike()
                else:
                    print('mid')
                    self.mid()


my_robot = MyRobot()
my_robot.run()
