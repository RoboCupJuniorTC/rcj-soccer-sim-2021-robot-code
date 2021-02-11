# rcj_soccer_player controller - ROBOT B1

# Feel free to import built-in libraries
import math

# You can also import scripts that you put into the folder with controller
from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP
import utils


class MyRobot(RCJSoccerRobot):
    def __init__(self):
        super().__init__()
        self.robot_pos = 0, 0
        self.avoid_time = -1000
        self.kickoff_time = -1000
        self.GOAL = 0.85 if self.name.startswith('Y') else -0.85, 0
        self.REAL_SPEED = 0.0182
        self.MAX_SPEED = 10
        self.SHOOT_DIST = 0.08
        self.AVOID_EL = 1/4

    def run(self):
        time = 0
        prev_ball_pos = {'x': -100, 'y': -100}
        target_x = target_y = 0
        while self.robot.step(TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()

                # Get the position of our robot
                self.robot_pos = data[self.name]
                # Get the position of the ball
                ball_pos = data['ball']
                if prev_ball_pos['x'] == -100:
                    prev_ball_pos = ball_pos.copy()

                # Calculate the speed of ball and predict its position
                act_time = self.robot.getTime()
                timedel = act_time-time
                if timedel == 0:
                    timedel = 1/1000
                time = act_time
                ball_x_vel = (prev_ball_pos['x']-ball_pos['x'])/timedel
                ball_y_vel = (prev_ball_pos['y']-ball_pos['y'])/timedel
                if abs(ball_x_vel) > 5:
                    ball_x_vel = 0
                if abs(ball_y_vel) > 5:
                    ball_y_vel = 0
                prev_ball_pos = ball_pos.copy()
                new_ball_x = ball_pos['x']
                new_ball_y = ball_pos['y']
                for _ in range(3):
                    rel_x = abs(new_ball_x-self.robot_pos['x'])
                    rel_y = abs(new_ball_y-self.robot_pos['y'])
                    ball_distance = math.hypot(rel_x, rel_y)
                    move_time = ball_distance/(self.MAX_SPEED*self.REAL_SPEED)
                    new_ball_x = ball_pos['x'] - move_time*ball_x_vel
                    new_ball_y = ball_pos['y'] - move_time*ball_y_vel

                # Calculate coordinates for shooting
                rel_ball_x, rel_ball_y = new_ball_x-self.GOAL[0], new_ball_y-self.GOAL[1]
                ball_goal_hypot = math.hypot(abs(rel_ball_x), abs(rel_ball_y))
                hypot_ratio = (ball_goal_hypot+self.SHOOT_DIST)/ball_goal_hypot
                target_x = self.GOAL[0] + rel_ball_x*hypot_ratio
                target_y = self.GOAL[1] + rel_ball_y*hypot_ratio

                # If the robot kicks off, shoot
                if -0.1 <= self.robot_pos['y'] <= 0.1 and -0.1 <= ball_pos['y'] <= 0.1:
                    self.kickoff_time = act_time

                # Realize whether the robot should shoot
                target_coords = {'x': target_x, 'y': target_y}
                if self.at_dest(target_x, target_y):
                    target_coords = {'x': self.GOAL[0], 'y': self.GOAL[1]}
                if act_time-self.kickoff_time <= 1.5:
                    target_coords = {'x': ball_pos['x'], 'y': ball_pos['y']}
                target_angle = self.get_angles(target_coords, self.robot_pos)[0]

                # Realize whether the robot is between ball and goal. If yes, avoid the ball
                el_goal_x = self.GOAL[0] + rel_ball_x*self.AVOID_EL
                el_goal_y = self.GOAL[1] + rel_ball_y*self.AVOID_EL
                el_ball_x = self.GOAL[0] + rel_ball_x*(1-self.AVOID_EL)
                el_ball_y = self.GOAL[1] + rel_ball_y*(1-self.AVOID_EL)
                b_rel_x, b_rel_y = self.robot_pos['x']-el_ball_x, self.robot_pos['y']-el_ball_y
                g_rel_x, g_rel_y = self.robot_pos['x']-el_goal_x, self.robot_pos['y']-el_goal_y
                ball_hypot = math.hypot(abs(b_rel_x), abs(b_rel_y))
                goal_hypot = math.hypot(abs(g_rel_x), abs(g_rel_y))
                if ball_hypot+goal_hypot < ball_goal_hypot:
                    self.avoid_time = act_time

                if act_time-self.avoid_time <= 0.2:
                    target_angle = (target_angle+30) % 360

                # Change the direction of move if advantageous
                speed = -self.MAX_SPEED
                if 90 < target_angle < 270:
                    target_angle = (target_angle+180) % 360
                    speed = self.MAX_SPEED

                # Calculate speeds
                direction = utils.get_direction(target_angle)
                if direction == 0:
                    left = speed
                    right = speed
                else:
                    left = speed/3 + direction * speed/3*2
                    right = speed/3 - direction * speed/3*2

                # Set the speed to motors
                self.left_motor.setVelocity(left)
                self.right_motor.setVelocity(right)

    def at_dest(self, x, y):
        tol = self.SHOOT_DIST
        rx, ry = self.robot_pos['x'], self.robot_pos['y']
        return x-tol <= rx <= x+tol and y-tol <= ry <= y+tol


my_robot = MyRobot()
my_robot.run()
