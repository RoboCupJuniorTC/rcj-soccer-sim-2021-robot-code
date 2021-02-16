# rcj_soccer_player controller - ROBOT B2

###### REQUIRED in order to import files from B1 controller
import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
# You can now import scripts that you put into the folder with your
# robot B1 controller
from team_034_libraries.robot1 import rcj_soccer_robot, utils_victor
######

# Feel free to import built-in libraries
import math


class MyRobot(rcj_soccer_robot.RCJSoccerRobot):
    def run(self):
        if self.name[0] == "B":
            team_blue = 1
        else:
            team_blue = -1


        current_ball_x = 0
        current_ball_y = 0
        prev_ball_x = 0
        prev_ball_y = 0

        while self.robot.step(rcj_soccer_robot.TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()

                # Get the position of our robot


                robot_pos = data[self.name]
                    # Get the position of the ball
                ball_pos = data['ball']

                prev_ball_x = current_ball_x
                prev_ball_y = current_ball_y

                current_ball_x = ball_pos['x']
                current_ball_y = ball_pos['y']

                ball_y_slope = current_ball_y - prev_ball_y
                ball_x_slope = current_ball_x - prev_ball_x

                player_x_slope = -1 * ball_x_slope
                player_y_slope = -1 * ball_y_slope

                if ball_pos['x'] > .45 * team_blue:
                    x_real = .73 * team_blue
                if ball_pos['y'] < 0:
                    real_y = ball_pos['y'] - .05
                elif ball_pos['y'] >= 0:
                    real_y = ball_pos['y'] + .05

                x_real = .68 * team_blue
                goal_pos = {'x': x_real, 'y': real_y}
                player_to_ball_pos = {'x': robot_pos['x'] + player_x_slope, 'y': robot_pos['y'] + player_y_slope}

                    # Get angle between the robot and the ball
                   # and between the robot and the north
                goal_angle, robot_angle = self.get_angles(goal_pos, robot_pos)
                ball_angle, robot_angle = self.get_angles(ball_pos, robot_pos)
                ball_to_robot_pos, robot_angle = self.get_angles(player_to_ball_pos, robot_pos)

                    # Compute the speed for motors
                directionGoal = utils_victor.get_direction(goal_angle)
                directionBall = utils_victor.get_direction(ball_angle)
                directionGoodBall = utils_victor.get_direction(ball_to_robot_pos)

                distance = utils_victor.get_distance(ball_pos, robot_pos)
                # If the robot has the ball right in front of it, go forward,
                # rotate otherwise



                if distance > 0.35:
                    if directionGoal == 0:
                        left_speed = -10
                        right_speed = -10
                        self.left_motor.setVelocity(left_speed)
                        self.right_motor.setVelocity(right_speed)

                    else:
                        left_speed = directionGoal * 10
                        right_speed = directionGoal * -10
                        self.left_motor.setVelocity(left_speed)
                        self.right_motor.setVelocity(right_speed)


                elif ball_pos['x'] * team_blue < 0:
                    if directionGoal == 0:
                        left_speed = -10
                        right_speed = -10
                        self.left_motor.setVelocity(left_speed)
                        self.right_motor.setVelocity(right_speed)

                    else:
                        left_speed = directionGoal * 10
                        right_speed = directionGoal * -10
                        self.left_motor.setVelocity(left_speed)
                        self.right_motor.setVelocity(right_speed)

                else:
                    if directionBall == 0:
                        left_speed = -10
                        right_speed = -10
                        self.left_motor.setVelocity(left_speed)
                        self.right_motor.setVelocity(right_speed)

                    else:
                        left_speed = directionBall * 10
                        right_speed = directionBall * -10
                        self.left_motor.setVelocity(left_speed)
                        self.right_motor.setVelocity(right_speed)




                # Set the speed to motors

my_robot = MyRobot()
my_robot.run()
