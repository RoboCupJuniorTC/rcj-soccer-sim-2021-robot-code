import math

from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP
import utils


class MyRobot(RCJSoccerRobot):
    def MoveTo(self, x, y, orientation, robot_pos):
        target_pos = dict()
        target_pos["x"] = x
        target_pos["y"] = y
        target_pos["orientation"] = orientation
        angle, robot_angle = self.get_angles(target_pos, robot_pos)
        moveto = utils.get_direction(angle)
        if moveto == 0:
            left_speed = -10
            right_speed = -10
        else:
            left_speed = moveto * 10
            right_speed = moveto * -10
        self.left_motor.setVelocity(left_speed)
        self.right_motor.setVelocity(right_speed)

    def CheckPos(self, rob_x, rob_y, x, y, t):
        if ((rob_x + 100 <= x+100+t) and (rob_x + 100 >= x + 100 - t)) and ((rob_y + 100 <= y+100+t) and (rob_y + 100 >= y+100-t)):
            return 1
        else:
            return 0

    def run(self):
        oldball_x = 0
        oldball_y = 0
        squadra = 0
        while self.robot.step(TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()
                robot_pos = data[self.name]
                ball_pos = data['ball']
                if squadra == 0:
                    if robot_pos["orientation"] > 0:
                        squadra = 1
                    else:
                        squadra = -1
                curball_x = ball_pos["x"]
                curball_y = ball_pos["y"]
                if squadra == 1:
                    if curball_x - oldball_x == 0:
                        ydest = ball_pos["y"]
                    else:
                        ydest = (((-0.68 - curball_x)/(oldball_x - curball_x))*(oldball_y - curball_y)) + curball_y
                    oldball_x = curball_x
                    oldball_y = curball_y
                    if curball_x > 0:
                        xdest = -0.5
                    else:
                        xdest = -0.68
                    if ydest > 0.30:
                        self.MoveTo(xdest, 0.4, 0, robot_pos)
                    elif ydest < -0.30:
                        self.MoveTo(xdest, -0.4, 0, robot_pos)

                    if ydest < 0.4 and ydest > -0.4:
                        if ball_pos["y"] < -0.50 and ball_pos["y"] > -0.70:
                            self.MoveTo(ball_pos["x"], ball_pos["y"], 0, robot_pos)
                        else:
                            self.MoveTo(xdest, ydest, 0, robot_pos)
                else:
                    if curball_x - oldball_x == 0:
                        ydest = ball_pos["y"]
                    else:
                        ydest = (((0.68 - curball_x) / (oldball_x - curball_x)) * (oldball_y - curball_y)) + curball_y
                    oldball_x = curball_x
                    oldball_y = curball_y
                    if curball_x < 0:
                        xdest = 0.5
                    else:
                        xdest = 0.68
                    if ydest > 0.30:
                        self.MoveTo(xdest, 0.4, 0, robot_pos)
                    elif ydest < -0.30:
                        self.MoveTo(xdest, -0.4, 0, robot_pos)

                    if ydest < 0.4 and ydest > -0.4:
                        if ball_pos["y"] < -0.50 and ball_pos["y"] > -0.70:
                            self.MoveTo(ball_pos["x"], ball_pos["y"], 0, robot_pos)
                        else:
                            self.MoveTo(xdest, ydest, 0, robot_pos)


my_robot = MyRobot()
my_robot.run()
