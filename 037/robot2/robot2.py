import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
sys.path.append('/app/controllers')

# team = 'BLUE'
# rcj_soccer_player controller - ROBOT Y2

###### REQUIRED in order to import files from Y1 controller
import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
# You can now import scripts that you put into the folder with your
# robot B1 controller
# if team == 'BLUE':
from team_037_libraries.robot1 import rcj_soccer_robot, utils
# else:
#     from rcj_soccer_player_y1 import rcj_soccer_robot, utils
######

# Feel free to import built-in libraries
import math

class MyRobot(rcj_soccer_robot.RCJSoccerRobot):
    def run(self):
        frameCounter = 0
        past_position = {"x": 0, "y": 0}
        x_diff = 1
        y_diff = 1
        slope = 0
        if self.name[0] == 'Y':
            t_m  = 1
        else:
            t_m = -1
        status = "idling"
        past_intercept =  {"x": 0, "y": 0}
        while self.robot.step(rcj_soccer_robot.TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()

                # Get the position of our robot
                robot_pos = data[self.name]
                # Get the position of the ball
                ball_pos = data['ball']
                x_diff = ball_pos['x'] - past_position['x']
                y_diff = ball_pos['y'] - past_position['y']
                # if ball_pos['x'] > -0.75 and ball_pos['x'] < -0.59 and ball_pos['y'] > -0.35 and ball_pos['y'] < 0.35:

                if frameCounter % 15 == 0:
                    if x_diff != 0:
                        slope = y_diff / x_diff
                        to_go = self.get_next_position(slope, ball_pos, robot_pos, t_m)
                        if to_go == {}:
                            status = "idling"
                            if robot_pos['y'] < 0.1:
                                to_go = {'x': -0.56 * t_m, 'y': 0.11}
                            elif robot_pos['y'] > 0.1:
                                to_go = {'x': -0.56 * t_m, 'y': -0.11}
                        elif ball_pos['x'] * t_m < -0.35 and robot_pos['x'] > to_go['x'] - 0.02 and robot_pos['x'] < to_go['x'] + 0.02 and robot_pos['y'] > to_go['y'] - 0.02 and robot_pos['y'] < to_go['y'] + 0.02 and abs(to_go['y'] != 0.11):
                            to_go = ball_pos
                            status = "charging"
                            # print("charging")
                        elif status == "charging":
                            if past_intercept['y'] > to_go['y'] - 0.01 and past_intercept['y'] < to_go['y'] + 0.01 and past_intercept['x'] > to_go['x'] - 0.01 and past_intercept['x'] < to_go['x'] + 0.01:
                                to_go = ball_pos
                                status = "charging"
                            else:
                                status = "idling"

                    else:
                        to_go = self.track_ball(ball_pos, t_m)
                        status = "idling"
                        if to_go == {}:
                            if robot_pos['y'] < 0.1:
                                to_go = {'x': -0.56 * t_m, 'y': 0.11}
                            elif robot_pos['y'] > 0.1:
                                to_go = {'x': -0.56 * t_m, 'y': -0.11}
                past_position = ball_pos
                past_intercept = to_go
                # Get angle between the robot and the ball
                # and between the robot and the north
                ball_angle, robot_angle = self.get_angles(to_go, robot_pos)

                # Compute the speed for motors
                direction = utils.get_direction(ball_angle)

                # If the robot has the ball right in front of it, go forward,
                # rotate otherwise
                # normal forward speed is 5, but i turned it up to 10 - stanley
                if direction == 0:
                    left_speed = -10
                    right_speed = -10
                elif direction == 2:
                    left_speed = 10
                    right_speed = 10
                else:
                    left_speed = direction * 4
                    right_speed = direction * -4

                # Set the speed to motors
                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)

                frameCounter += 1
                # if frameCounter % 15 == 0:
                #     print(past_position)
                #     print(x_diff)
                #     print(y_diff)
                #     print(slope)
                #     print(x_box_intercept)
                # print(to_go)

    def get_next_position(self, slope, ball_pos, robot_pos, t_m):
        b = -slope * ball_pos['x'] + ball_pos['y']
        if ball_pos['x'] * t_m > -0.59 or ball_pos['y'] * t_m > 0.35 or ball_pos['y'] < -0.35:
            to_go = self.get_penalty_intercept(slope, ball_pos, b, t_m)
            if to_go['x'] * t_m == -0.56 and to_go['y'] == 0 and ball_pos['y'] != 0:
                # dx = -0.75 - ball_pos['x']
                # print("special")
                # new_slope = dx / (-ball_pos['y'])
                # new_b = new_slope * ball_pos['x'] + ball_pos['y']
                # to_go = self.get_penalty_intercept(new_slope, ball_pos, new_b)
                to_go = self.track_ball(ball_pos, t_m)
        else:
            to_go = {}
        return to_go

    def get_penalty_intercept(self, slope, ball_pos, b, t_m):
        x_box_intercept = slope * (-0.59 * t_m - ball_pos['x']) + ball_pos['y']
        if x_box_intercept > 0.65:
            y_box_intercept = (0.35 - ball_pos['y']) / slope + ball_pos['x']
            if y_box_intercept * t_m > -0.9 and y_box_intercept * t_m < -.59 and slope > 1:
                to_go = {"x": y_box_intercept, "y": 0.38}
            else:
                to_go = {"x": -0.56 * t_m, "y": 0}
            # print(x_box_intercept)
            # print(y_box_intercept)
        elif x_box_intercept < -0.65:
            y_box_intercept = (0.35 - ball_pos['y']) / slope + ball_pos['x']
            if y_box_intercept * t_m > -0.9 and y_box_intercept * t_m < -.59 and slope < 1:
                to_go = {"x": y_box_intercept, "y": -0.38}
            else:
                to_go = {"x": -0.56 * t_m, "y": 0}
            # print(x_box_intercept)
            # print(y_box_intercept)
        elif ball_pos['x'] * t_m > -0.59:
            to_go = {"x": -0.56 * t_m, "y": x_box_intercept}
        else:
            to_go = {"x": -0.56 * t_m, "y": 0}
        return to_go

    def track_ball(self, ball_pos, t_m):
        if ball_pos['y'] > -0.35 and ball_pos['y'] < 0.35:
            return {'x': -0.56 * t_m, 'y': ball_pos['y']}
        elif ball_pos['x'] * t_m > -0.75 and ball_pos['x'] * t_m < -0.59:
            if ball_pos['y'] > 0:
                return {'x': ball_pos['x'], 'y': 0.38}
            elif ball_pos['y'] < 0:
                return {'x': ball_pos['x'], 'y': -0.38}
        else:
            return {}


my_robot = MyRobot()
my_robot.run()
