import math
import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
from robot1 import rcj_soccer_robot, utils
import def_functions

class MyRobot(rcj_soccer_robot.RCJSoccerRobot):
    def getName(self):
        return self.name
    def run(self):
        t = 0.0
        while self.robot.step(rcj_soccer_robot.TIME_STEP) != -1:
            t += rcj_soccer_robot.TIME_STEP / 1000.0
            total_seconds = round(t + 0.5)
            minutes, seconds = divmod(600 - round(t + 0.5), 60)

            if self.is_new_data():
                data = self.get_new_data()
                robot_pos = data[self.name]
                ball_pos = data['ball']

                ball_angle, robot_angle = self.get_angles(ball_pos, robot_pos)
                direction = utils.get_direction(ball_angle)

                robot_angle = math.degrees(robot_angle)
                distance = math.sqrt(math.pow(robot_pos['x'] - ball_pos['x'], 2) + math.pow(robot_pos['y'] - ball_pos['y'], 2))

                left_speed = 0
                right_speed = 0
                spin_speed = 4
                angle_range = 8

                if "B" in self.name:
                    if ball_pos['x'] > 0.6 and ball_pos['y'] < 0.35 and ball_pos['y'] > -0.35 and robot_pos['x'] > 0.6:
                        if robot_pos['y'] > ball_pos['y']:
                            left_speed, right_speed = def_functions.move(self, robot_angle, -10, -10, 0, 0, True)
                        elif robot_pos['y'] < ball_pos['y']:
                            left_speed, right_speed = def_functions.move(self, robot_angle, 10, 10, 0, 0, True)
                    elif ball_pos['x'] > 0.44 and ball_pos['y'] > 0.32:
                        if robot_pos['y'] < 0.38 or robot_pos['y'] > 0.44:
                            angle, absolute_angle = def_functions.coords(self, robot_angle, robot_pos['x'],
                                                                         robot_pos['y'], 0.68,
                                                                         0.38)
                            if robot_angle > angle + angle_range or robot_angle < angle - angle_range:
                                left_speed, right_speed = def_functions.spin(self, robot_angle, angle, left_speed,
                                                                             right_speed,
                                                                             spin_speed, angle_range)
                            else:
                                left_speed, right_speed = def_functions.move(self, robot_angle, 10, 10, angle, absolute_angle,
                                                                       False)
                        else:
                            angle = def_functions.direction(self, robot_angle, 45, 225)
                            if robot_angle > angle + angle_range or robot_angle < angle - angle_range:
                                left_speed, right_speed = def_functions.spin(self, robot_angle, angle, left_speed,
                                                                             right_speed,
                                                                             spin_speed, angle_range)
                            else:
                                left_speed, right_speed = 2, 2
                                left_speed, right_speed = def_functions.border(self, robot_angle, robot_pos['y'],
                                                                         left_speed,
                                                                         right_speed, 0.27, -0.27, 0.05)
                    elif ball_pos['x'] > 0.44 and ball_pos['y'] < -0.32:
                        if robot_pos['y'] > -0.38 or robot_pos['y'] < -0.44:
                            angle, absolute_angle = def_functions.coords(self, robot_angle, robot_pos['x'],
                                                                         robot_pos['y'], 0.68,
                                                                         -0.38)
                            if robot_angle > angle + angle_range or robot_angle < angle - angle_range:
                                left_speed, right_speed = def_functions.spin(self, robot_angle, angle, left_speed,
                                                                             right_speed,
                                                                             spin_speed, angle_range)
                            else:
                                left_speed, right_speed = def_functions.move(self, robot_angle, 10, 10, angle, absolute_angle,
                                                                   False)
                        else:
                            angle = def_functions.direction(self, robot_angle, 135, 315)
                            if robot_angle > angle + angle_range or robot_angle < angle - angle_range:
                                left_speed, right_speed = def_functions.spin(self, robot_angle, angle, left_speed,
                                                                             right_speed,
                                                                             spin_speed, angle_range)
                            else:
                                left_speed, right_speed = -2, -2
                                left_speed, right_speed = def_functions.border(self, robot_angle, robot_pos['y'],
                                                                         left_speed,
                                                                         right_speed, 0.27, -0.27, 0.05)
                    else:
                        if robot_pos['x'] > 0.53 and robot_pos['x'] < 0.59:
                            if (robot_angle < 180 + angle_range and robot_angle > 180 - angle_range) or (
                                    robot_angle < 0 + angle_range or robot_angle > 360 - angle_range):
                                left_speed, right_speed = def_functions.chase(self, robot_angle, robot_pos['y'],
                                                                        ball_pos['y'])
                                if ball_pos['x'] < 0:
                                    left_speed, right_speed = def_functions.border(self, robot_angle, robot_pos['y'],
                                                                                   left_speed,
                                                                                   right_speed, 0.22, -0.22, 0.05)
                                else:
                                    left_speed, right_speed = def_functions.border(self, robot_angle, robot_pos['y'], left_speed,
                                                                         right_speed, 0.27, -0.27, 0.05)
                            else:
                                angle = def_functions.direction(self, robot_angle, 0, 180)
                                left_speed, right_speed = def_functions.spin(self, robot_angle, angle, left_speed,
                                                                       right_speed,
                                                                       spin_speed, angle_range)
                        else:
                            angle, absolute_angle = def_functions.coords(self, robot_angle, robot_pos['x'], robot_pos['y'],
                                                                   0.56,
                                                                   0)
                            if robot_angle > angle + angle_range or robot_angle < angle - angle_range:
                                left_speed, right_speed = def_functions.spin(self, robot_angle, angle, left_speed,
                                                                       right_speed,
                                                                       spin_speed, angle_range)
                            else:
                                left_speed, right_speed = def_functions.move(self, robot_angle, 10, 10, angle,
                                                                       absolute_angle,
                                                                       False)
                else:
                    if ball_pos['x'] < -0.6 and ball_pos['y'] < 0.35 and ball_pos['y'] > -0.35 and robot_pos['x'] < -0.6:
                        if robot_pos['y'] > ball_pos['y']:
                            left_speed, right_speed = def_functions.move(self, robot_angle, -10, -10, 0, 0, True)
                        elif robot_pos['y'] < ball_pos['y']:
                            left_speed, right_speed = def_functions.move(self, robot_angle, 10, 10, 0, 0, True)
                    elif ball_pos['x'] < -0.44 and ball_pos['y'] > 0.32:
                        if robot_pos['y'] < 0.38 or robot_pos['y'] > 0.44:
                            angle, absolute_angle = def_functions.coords(self, robot_angle, robot_pos['x'],
                                                                         robot_pos['y'], -0.68,
                                                                         0.38)
                            if robot_angle > angle + angle_range or robot_angle < angle - angle_range:
                                left_speed, right_speed = def_functions.spin(self, robot_angle, angle, left_speed,
                                                                             right_speed,
                                                                             spin_speed, angle_range)
                            else:
                                left_speed, right_speed = def_functions.move(self, robot_angle, 10, 10, angle,
                                                                             absolute_angle,
                                                                             False)
                        else:
                            angle = def_functions.direction(self, robot_angle, 135, 315)
                            if robot_angle > angle + angle_range or robot_angle < angle - angle_range:
                                left_speed, right_speed = def_functions.spin(self, robot_angle, angle, left_speed,
                                                                             right_speed,
                                                                             spin_speed, angle_range)
                            else:
                                left_speed, right_speed = 2, 2
                                left_speed, right_speed = def_functions.border(self, robot_angle, robot_pos['y'],
                                                                         left_speed,
                                                                         right_speed, 0.27, -0.27, 0.05)
                    elif ball_pos['x'] < -0.44 and ball_pos['y'] < -0.32:
                        if robot_pos['y'] > -0.38 or robot_pos['y'] < -0.44:
                            angle, absolute_angle = def_functions.coords(self, robot_angle, robot_pos['x'],
                                                                         robot_pos['y'], -0.68,
                                                                         -0.38)
                            if robot_angle > angle + angle_range or robot_angle < angle - angle_range:
                                left_speed, right_speed = def_functions.spin(self, robot_angle, angle, left_speed,
                                                                             right_speed,
                                                                             spin_speed, angle_range)
                            else:
                                left_speed, right_speed = def_functions.move(self, robot_angle, 10, 10, angle,
                                                                             absolute_angle,
                                                                             False)
                        else:
                            angle = def_functions.direction(self, robot_angle, 45, 225)
                            if robot_angle > angle + angle_range or robot_angle < angle - angle_range:
                                left_speed, right_speed = def_functions.spin(self, robot_angle, angle, left_speed,
                                                                             right_speed,
                                                                             spin_speed, angle_range)
                            else:
                                left_speed, right_speed = -2, -2
                                left_speed, right_speed = def_functions.border(self, robot_angle, robot_pos['y'],
                                                                         left_speed,
                                                                         right_speed, 0.27, -0.27, 0.05)
                    else:
                        if robot_pos['x'] < -0.53 and robot_pos['x'] > -0.59:
                            if (robot_angle < 180 + angle_range and robot_angle > 180 - angle_range) or (
                                    robot_angle < 0 + angle_range or robot_angle > 360 - angle_range):
                                left_speed, right_speed = def_functions.chase(self, robot_angle, robot_pos['y'],
                                                                        ball_pos['y'])
                                if ball_pos['x'] > 0:
                                    left_speed, right_speed = def_functions.border(self, robot_angle, robot_pos['y'],
                                                                                   left_speed,
                                                                                   right_speed, 0.22, -0.22, 0.05)
                                else:
                                    left_speed, right_speed = def_functions.border(self, robot_angle, robot_pos['y'],
                                                                                   left_speed,
                                                                                   right_speed, 0.27, -0.27, 0.05)
                            else:
                                angle = def_functions.direction(self, robot_angle, 0, 180)
                                left_speed, right_speed = def_functions.spin(self, robot_angle, angle, left_speed,
                                                                       right_speed,
                                                                       spin_speed, angle_range)
                        else:
                            angle, absolute_angle = def_functions.coords(self, robot_angle, robot_pos['x'], robot_pos['y'],
                                                                   -0.56,
                                                                   0)
                            if robot_angle > angle + angle_range or robot_angle < angle - angle_range:
                                left_speed, right_speed = def_functions.spin(self, robot_angle, angle, left_speed,
                                                                       right_speed,
                                                                       spin_speed, angle_range)
                            else:
                                left_speed, right_speed = def_functions.move(self, robot_angle, 10, 10, angle,
                                                                       absolute_angle,
                                                                       False)

                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)


my_robot = MyRobot()
my_robot.run()
