# rcj_soccer_player controller - ROBOT B1

# Feel free to import built-in libraries
import math
import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
# You can now import scripts that you put into the folder with your
# robot B1 controller
from robot1 import rcj_soccer_robot, utils

def sign(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0

def bound(val, top):
    if abs(val) > top:
        return sign(val) * top
    return val

def dist(a, b):
    return math.sqrt((a['x'] - b['x']) ** 2 + (a['y'] - b['y']) ** 2)

def norm(x):
    while x <= -180:
        x += 360
    while x > 180:
        x -= 360
    return x

RAD2DEG = 180 / math.pi

BLUE_GOAL = [{'x': 0.8, 'y': -0.3}, {'x':0.8, 'y':0.3}, {'x':0.8, 'y':0}]
YELLOW_GOAL = [{'x': -0.8, 'y': -0.3}, {'x':-0.8, 'y':0.3}, {'x':-0.8, 'y':0}]

class MyRobot(rcj_soccer_robot.RCJSoccerRobot):
    def run(self):
        un_zero = 0
        while self.robot.step(rcj_soccer_robot.TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()

                # Get the position of our robot
                robot_pos = data[self.name]
                # Get the position of the ball
                ball_pos = data['ball']
                
                if self.name[0] == "Y":
                    ENEMY_GOAL = YELLOW_GOAL
                    north_sign = -1
                else:
                    ENEMY_GOAL = BLUE_GOAL
                    north_sign = 1
                
                # Get angle between the robot and the ball
                # and between the robot and the north 
                ball_angle, robot_angle = self.get_angles(ball_pos, robot_pos)
                
                ball_dist = dist(ball_pos, robot_pos)
                
                abs_enemy_goal_angle = [0,0]
                abs_enemy_goal_angle[0] = norm(RAD2DEG * math.atan2(
                    ENEMY_GOAL[0]['y'] - robot_pos['y'],
                    ENEMY_GOAL[0]['x'] - robot_pos['x']
                ))
                
                abs_enemy_goal_angle[1] = norm(RAD2DEG * math.atan2(
                    ENEMY_GOAL[1]['y'] - robot_pos['y'],
                    ENEMY_GOAL[1]['x'] - robot_pos['x']
                ))
                
                for i in range(2):
                    abs_enemy_goal_angle[i] += 15 * sign(abs_enemy_goal_angle[i])
                    abs_enemy_goal_angle[i] = norm(abs_enemy_goal_angle[i])
                
                abs_enemy_goal_angle_center = norm(RAD2DEG * math.atan2(
                    ENEMY_GOAL[2]['y'] - robot_pos['y'],
                    ENEMY_GOAL[2]['x'] - robot_pos['x']
                ))
                
                
                abs_ball_angle = RAD2DEG * math.atan2(
                    robot_pos['y'] - ball_pos['y'],
                    robot_pos['x'] - ball_pos['x']
                )
                
                ball_angle = norm(ball_angle)
                robot_angle = norm(robot_angle * RAD2DEG + 90 * north_sign)
                enemy_goal_angle = norm(abs_enemy_goal_angle_center / 2 + robot_angle)
                
                
                target_angle = norm(abs_ball_angle - abs_enemy_goal_angle_center)
                
                mul = math.sqrt(0.3 / ball_dist)
                if mul > 1.5:
                    mul = 1.5
                adduction = sign(target_angle) * 40 / (2 - mul)
                adduction = bound(adduction, 110)
                
                if abs(target_angle) < 10:
                    un_zero = 300
                else:
                    un_zero -= abs(target_angle)
                    
                if abs(target_angle) < 30 and ball_dist < 0.1:
                    un_zero = max(un_zero, 100)
                
                if un_zero > 0:
                    adduction = 0
                
                if ball_dist > 0.3:
                    adduction = 0
                
                target_angle += adduction
                u = norm(robot_angle + target_angle)
                u = u / 3 + u * u * sign(u) / 100
                vel = -10 + abs(u) / 4
                    
                left_speed = vel - u
                right_speed = vel + u
                    
                
                left_speed = bound(left_speed, 10)
                right_speed = bound(right_speed, 10)
                
                # Set the speed to motors
                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)


my_robot = MyRobot()
my_robot.run()
