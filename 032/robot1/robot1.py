# rcj_soccer_player controller - ROBOT B1
 
# Feel free to import built-in libraries
import math
 
# You can also import scripts that you put into the folder with controller
from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP
import utils
 
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
 
                if self.name[0] == "Y":
                    ENEMY_GOAL = YELLOW_GOAL
                    north_sign = -1
                else:
                    ENEMY_GOAL = BLUE_GOAL
                    north_sign = 1
                # Compute the speed for motors
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
 
                robot_angle = norm(robot_angle * RAD2DEG + 90 * north_sign)
                enemy_goal_angle = norm(abs_enemy_goal_angle_center / 2 + robot_angle)
 
                # If the robot has the ball right in front of it, go forward,
                # rotate otherwise
                const1 = 0
                if enemy_goal_angle > 0:
                    const1 = - 1/50 - 0.05
                else:
                    const1 = 1/50 + 0.05
                toBallX = ball_pos['x'] - robot_pos['x']
                toBallY = ball_pos['y'] - robot_pos['y']
                toBall = (toBallX * toBallX + toBallY * toBallY) ** 0.5
                angle = math.atan2(const1, toBall) * 57.3
                angle = (angle + ball_angle) % 360
                direction = utils.get_direction(angle)
                if direction == 0:
                    left_speed = -10
                    right_speed = -10
                else:
                    left_speed = direction * 10
                    right_speed = direction * -10
 
                # Set the speed to motors
                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)
                print(enemy_goal_angle)
 
 
my_robot = MyRobot()
my_robot.run()