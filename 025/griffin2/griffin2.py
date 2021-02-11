# rcj_soccer_player controller - ROBOT B2

import rcj_soccer_robot, utils

# Feel free to import built-in libraries
import math
from typing import Tuple

class MyRobot(rcj_soccer_robot.RCJSoccerRobotT):
    def get_speed (self, angle: float) -> Tuple[float, float]:
        if angle >= 270 or angle <= 90:    
            if angle >= 345 or angle <= 15:
                left_speed = -10
                right_speed = -10
            elif angle > 180:
                left_speed = 4
                right_speed = -10
            else:
                left_speed = -10
                right_speed = 4
        else:
            if angle >= 165 and angle <= 195:
                left_speed = 10
                right_speed = 10
            elif angle > 180:
                left_speed = -4
                right_speed = 10
            else:
                left_speed = 10
                right_speed = -4
        return left_speed, right_speed
    
    def get_speed0 (self, angle: float) -> Tuple[float, float]:
        if angle >= 270 or angle <= 90:    
            if angle >= 345 or angle <= 15:
                left_speed = 0
                right_speed = 0
            elif angle > 180:
                left_speed = 4
                right_speed = -4
            else:
                left_speed = -4
                right_speed = 4
        else:
            if angle >= 165 and angle <= 195:
                left_speed = 0
                right_speed = 0
            elif angle > 180:
                left_speed = -4
                right_speed = 4
            else:
                left_speed = 4
                right_speed = -4
        return left_speed, right_speed

    def is_valid_pos (self, x: float, y: float):
        if x > 0.70 or x < -0.70:
            return False
        if y > 0.60 or y < -0.60:
            return False
        return True

    def run(self):
        while self.robot.step(rcj_soccer_robot.TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()

                # Get the position of our robot
                robot_pos = data[self.name]
                # Get the position of the ball
                ball_pos = data['ball']
                
                waiting_pos      = { 'x': -0.35, 'y': 0.20 }
                waiting_area     = { 'x1': -1.00, 'y1': -0.20, 'x2': -0.10, 'y2': 1.00 }
                attacking_area   = { 'x1': -1.00, 'x2': -0.10 }
                goal_pos         = { 'x': -0.90, 'y': 0.00 }
                goal_my_pos      = { 'x': 0.90, 'y': 0.00 }
                real_goal_my_pos = { 'x': 0.75, 'y': 0.00 }
                if self.name.startswith('Y'):
                    waiting_pos      = { 'x': 0.35, 'y': -0.20 }
                    waiting_area     = { 'x1': 0.10, 'y1': -1.00, 'x2': 1.00, 'y2': 0.20 }
                    attacking_area   = { 'x1': 0.10, 'x2': 1.00 }
                    goal_pos         = { 'x': 0.90, 'y': 0.00 }
                    goal_my_pos      = { 'x': -0.90, 'y': 0.00 }
                    real_goal_my_pos = { 'x': -0.75, 'y': 0.00 }
                # Get angle between the robot and the ball
                # and between the robot and the north
                ball_angle, robot_angle, waiting_angle = self.get_angles(ball_pos, robot_pos, waiting_pos)

                
                to_ball_x = ball_pos['x'] - robot_pos['x']
                to_ball_y = ball_pos['y'] - robot_pos['y']
                to_ball_dist = math.hypot(to_ball_x, to_ball_y)
                
                to_wait_x = waiting_pos['x'] - robot_pos['x']
                to_wait_y = waiting_pos['y'] - robot_pos['y']
                to_wait_dist = math.hypot(to_wait_x, to_wait_y)

                # strike_pos / strike_angle
                dx = ball_pos['x'] - goal_pos['x']
                dy = ball_pos['y'] - goal_pos['y']
                dd = math.hypot(dx, dy)
                dd2 = dd + 0.08
                if dd > 0.01:
                    strike_pos_x = goal_pos['x'] + dx * dd2 / dd
                    strike_pos_y = goal_pos['y'] + dy * dd2 / dd
                else: 
                    strike_pos_x = ball_pos['x']
                    strike_pos_y = ball_pos['y']
                
                dz_x = ball_pos['x'] - real_goal_my_pos['x']
                dz_y = ball_pos['y'] - real_goal_my_pos['y'] 
                dz = math.hypot( dz_x, dz_y )
                dz2 = dz - 0.08
                if dz > 0.01:
                    striker_near_barrier_x = real_goal_my_pos['x'] + dz_x * dz2 / dz
                    striker_near_barrier_y = real_goal_my_pos['y'] + dz_y * dz2 / dz
                else:
                    striker_near_barrier_x = ball_pos['x']
                    striker_near_barrier_y = ball_pos['y']

                if not self.is_valid_pos(strike_pos_x, strike_pos_y):
                    strike_pos_x = striker_near_barrier_x
                    strike_pos_y = striker_near_barrier_y
                
                #my goal - ak tlacime loptu do nasej brany tak ju obideme 
                dd1 = math.hypot(goal_my_pos['x'] - robot_pos['x'], goal_my_pos['y'] - robot_pos['y'])
                dd2 = math.hypot(goal_my_pos['x'] - ball_pos['x'], goal_my_pos['y'] - ball_pos['y'])
                
                
                avoid_ball = 0
                # robot je dalej od brany ako lopta (tlaci ju do brany)
                if dd1 > dd2 - 0.03:
                    avoid_ball = 1
                    #p1_pos = { 'x': ball_pos['x'] + goal_my_pos['x'] / 20, 'y': ball_pos['y'] + 0.08 } 
                    #p2_pos = { 'x': ball_pos['x'] + goal_my_pos['x'] / 20, 'y': ball_pos['y'] - 0.08 }
                    p1_pos = { 'x': ball_pos['x'] + goal_my_pos['x'] / 20, 'y': ball_pos['y'] + 0.08 } 
                    p2_pos = { 'x': ball_pos['x'] + goal_my_pos['x'] / 20, 'y': ball_pos['y'] - 0.08 }
                    p1_dist = math.hypot(p1_pos['x'] - robot_pos['x'], p1_pos['y'] - robot_pos['y'])
                    p2_dist = math.hypot(p2_pos['x'] - robot_pos['x'], p2_pos['y'] - robot_pos['y'])
                    if (p1_dist < p2_dist and p1_pos['y'] <= 0.60) or p2_pos['y'] < -0.60:
                        strike_pos_x = p1_pos['x']
                        strike_pos_y = p1_pos['y']
                    else:
                        strike_pos_x = p2_pos['x']
                        strike_pos_y = p2_pos['y']

                # vypocitame uhly a vzdialenosti
                to_strike_dist = math.hypot(strike_pos_x - robot_pos['x'], strike_pos_y - robot_pos['y']) 
                strike_angle, a1, goal_angle = self.get_angles({ 'x': strike_pos_x, 'y': strike_pos_y }, robot_pos, goal_pos)

                go_to_ball = 0
                go_to_wait = 0
                go_to_strike = 0
                go_to_goal = 0
                wait = 0

                # Lopta je v na mojej strane pred branou 
                if (ball_pos['y'] > waiting_area['y1'] and ball_pos['y'] < waiting_area['y2']) and (ball_pos['x'] > waiting_area['x1'] and ball_pos['x'] < waiting_area['x2']):
                    go_to_ball = 1
                elif ball_pos['x'] > attacking_area['x1'] and ball_pos['x'] < attacking_area['x2']:
                    # lopta je na strane supera ale nie je v mojej oblasti pred branou
                    go_to_wait = 1
                else:
                    # lopta je v nasej polke ihriska 
                    go_to_ball = 1

                if  to_ball_dist <= 0.15:
                    go_to_ball = 1

                if go_to_ball > 0:
                    if  to_ball_dist <= 0.05:
                        go_to_goal = 1
                    elif to_strike_dist > 0.05:
                        go_to_strike = 1

                if avoid_ball > 0 and go_to_ball > 0:
                    go_to_strike = 1
                
                if  to_wait_dist <= 0.05:
                    wait = 1
                else:
                    go_to_wait = 1
                
                """
                r3_data = data[f'{self.name[0]}3']
                r3_dist = math.hypot(abs(r3_data['x']-ball_pos['x']), abs(r3_data['y']-ball_pos['y']))
                if (r3_dist <= 0.1) and ((go_to_ball > 0) or (go_to_strike > 0)) and go_to_goal <= 0:
                    wait = 1
                    go_to_ball = 0
                    go_to_strike = 0
                """

                if go_to_goal > 0:
                    left_speed, right_speed = self.get_speed(goal_angle)
                elif go_to_strike > 0:
                    left_speed, right_speed = self.get_speed(strike_angle)
                elif go_to_ball > 0:
                    left_speed, right_speed = self.get_speed(ball_angle)
                elif wait > 0:
                    left_speed, right_speed = self.get_speed0(ball_angle)
                elif go_to_wait > 0:
                    left_speed, right_speed = self.get_speed(waiting_angle)
                
                #print(self.name + ": go_to_ball=" + str(go_to_ball) + ", go_to_wait=" + str(go_to_wait) + ", wait=" + str(wait) + ": go_to_goal=" + str(go_to_goal) + ", go_to_strike=" + str(go_to_strike) + ", avoid_ball=" + str(avoid_ball) + ", striker_near_barrier_x=" + str(striker_near_barrier_x) + ", striker_near_barrier_y=" + str(striker_near_barrier_y))
                #print(self.name + ": ball_pos_x=" + str(ball_pos['x']) + ", ball_pos_y=" + str(ball_pos['y']) + ", strike_pos_x=" + str(strike_pos_x) + ", strike_pos_y=" + str(strike_pos_y))
                
                # Set the speed to motors
                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)
my_robot = MyRobot()
my_robot.run()
