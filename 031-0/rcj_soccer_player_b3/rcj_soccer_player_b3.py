# rcj_soccer_player controller - ROBOT B3

###### REQUIRED in order to import files from B1 controller
import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
# You can now import scripts that you put into the folder with your
# robot B1 controller
from rcj_soccer_player_b1 import rcj_soccer_robot, utils
######

# Feel free to import built-in libraries
import math, time


class MyRobot(rcj_soccer_robot.RCJSoccerRobot):

    def run(self):
        ROT_K = 0.4
        ROT_D = 0
        ROT_I = 0
        I_MAX = 0
        I = 0.0
        oldErr = 0
        err = 0
        speed = -10
        rTime = time.time()
        goal = {'x': -0.7, 'y': 0}
        old_robot_pos = {'x': 0, 'y': 0}
        flag = 0
        cnt = 0

        #Please subscribe to us!
        #inst: @semicolon.robocup
        #YouTube: https://www.youtube.com/channel/UC9m3bGAsJcVbLzjM8-gC-Kg

        while self.robot.step(rcj_soccer_robot.TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()

                robot_pos = data[self.name]
                ball_pos = data['ball']

                ball_angle, robot_angle = self.get_angles(ball_pos, robot_pos)
                ball_angle = utils.angle_converter(ball_angle)
                robot_angle = utils.angle_converter(robot_angle)

                if(utils.norm(old_robot_pos["x"] - ball_pos["x"], old_robot_pos["y"] - robot_pos["y"]) < 0.007):
                    cnt+=1
                else:
                    cnt = 0

                if(cnt > 100):
                    cnt = 0
                    flag = 1
                    timer = time.time()


                B = -(goal['x'] - ball_pos['x'])
                A = (goal['y'] - ball_pos['y'])
                D = abs(A*(robot_pos['x'] - ball_pos['x']) + B*(robot_pos['y'] - ball_pos['y'])) / math.sqrt(A**2 + B**2)
                c1 = {'x': ball_pos['x'] - robot_pos['x'], 'y': ball_pos['y'] - robot_pos['y']}
                c2 = {'x': ball_pos['x'] - goal['x'], 'y': ball_pos['y'] - goal['y']}
                if D < 0.01 and utils.scalarMult(c1, c2) < 0:
                    err = utils.angle_converter(utils.getAngleToPoint(ball_pos, robot_pos))
                else:
                    err = utils.angle_converter(utils.rotateOnTangent(
                            robot = robot_pos, 
                            point = ball_pos, 
                            goal = goal, 
                            R = 0.1   
                        )
                    )

                k = (err * ROT_K) + ((err - oldErr) * ROT_D) + I * ROT_I

                if flag == 1:
                    if(time.time() - timer < 1):
                        speed = -speed
                    else:
                        flag = 0
                        cnt = 0
                  
                left_speed = speed - (0.8 * k)
                right_speed = speed + (0.8 * k)

                old_robot_pos = robot_pos

                oldErr = err
                rTime = time.time()

                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)


my_robot = MyRobot()
my_robot.run()
