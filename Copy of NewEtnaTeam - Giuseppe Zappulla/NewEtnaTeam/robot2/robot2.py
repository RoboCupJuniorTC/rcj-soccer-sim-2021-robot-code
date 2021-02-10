import math

# You can also import scripts that you put into the folder with controller
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
        stato = "gotoPosizione"
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
                if squadra == 1:
                    if stato == "gotoPosizione":
                        self.MoveTo(ball_pos["x"] - 0.15, ball_pos["y"], 0, robot_pos)
                        if robot_pos["x"] < ball_pos["x"] - 0.15:
                            stato = "attaccante"
                    elif stato == "attaccante":
                        self.MoveTo(ball_pos["x"], ball_pos["y"], 0, robot_pos)
                        if robot_pos["x"] > ball_pos["x"]:
                            stato = "gotoPosizione"
                else:
                    if stato == "gotoPosizione":
                        self.MoveTo(ball_pos["x"] + 0.15, ball_pos["y"], 0, robot_pos)
                        if robot_pos["x"] > ball_pos["x"] + 0.15:
                            stato = "attaccante"
                    elif stato == "attaccante":
                        self.MoveTo(ball_pos["x"], ball_pos["y"], 0, robot_pos)
                        if robot_pos["x"] < ball_pos["x"]:
                            stato = "gotoPosizione"


my_robot = MyRobot()
my_robot.run()
