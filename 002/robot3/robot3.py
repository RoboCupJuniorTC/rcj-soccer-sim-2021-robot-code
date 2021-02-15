import sys
sys.path.append('/app/controllers/')
sys.path.append('.')
# rcj_soccer_player controller - ROBOT Y3

###### REQUIRED in order to import files from Y1 controller
import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
# You can now import scripts that you put into the folder with your
# robot B1 controller

######

try:
    from team_002_libraries.robot1 import hey
    print("blue")
    from team_002_libraries.robot1 import rcj_soccer_robot, utils
except:
    print("yellow")
    from team_002_libraries.robot1 import rcj_soccer_robot, utils


class MyRobot(rcj_soccer_robot.RCJSoccerRobot):
    def run(self):
        while self.robot.step(rcj_soccer_robot.TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()

                # Get the position of our robot
                robot_pos = data[self.name]
                # Get the position of the ball
                ball_pos = data['ball']

                # Get angle between the robot and the ball

                rotation = data[self.name]['orientation']
                robot_pos = data[self.name]
                ball_pos = data['ball']
                x = data[self.name]['x']
                y = data[self.name]['y']
                x_ball = data['ball']['x']
                y_ball = data['ball']['y']
                

                dy = y_ball - y # y diff vom ball und roboter
                dx = x_ball -x # x diff vom ball und roboter
                p = dy * 12 # y diff mal nen Faktor es von der geschindigkeit zu subtrahieren
                m = dy * 12.2 # y diff mal nen Faktor um es von der geschindigkeit zu subtrahieren
                g = dy * 12.25 # y diff mal nen Faktor um es von der geschindigkeit zu subtrahieren (werte mit den man die geschiwindigkeit verändert)
                mg = -0.065 # werte bei den sich die geschwindigkeit verändern soll
                pg = 0.065 # werte bei den sich die geschwindigkeit verändern soll
                l = 0.071 # werte bei den sich die geschwindigkeit verändern soll
                if self.team == 'Y':
                    if x_ball < 0.02 and x_ball > -0.1 and y_ball > -0.025 and y_ball < 0.025:

                        if dy > 0 and dy < 0: 
                            left_speed = -10
                            right_speed = -10
                        elif dy < 0 and dy > mg:
                            left_speed = -10
                            right_speed = -10 - p
                            print(1)
                        elif dy > 0 and dy < pg:
                            left_speed = -10 + p
                            right_speed = -10
                            print(2)
                        elif dy < mg and dy > -l:
                            left_speed = -10
                            right_speed = -10 - m
                            print(3)
                        elif dy > pg and dy < l:
                            left_speed = -10 + m
                            right_speed = -10
                            print(4)
                        elif dy > l:
                            left_speed = -10 + g
                            right_speed = -10
                            print(5)
                        elif dy < -l:
                            left_speed = -10
                            right_speed = 10 - g
                            print(6)
                        else:
                            left_speed = 0
                            right_speed = 0
                    else: 
                        if y > -0.04 and y < 0.04 and rotation < 1.2 or rotation > 1.6:
                            print("drehen")
                            left_speed = 10
                            right_speed = -10
                        elif x < -0.4:
                            left_speed = -10
                            right_speed = -10
                        elif x > -0.1:
                            left_speed = 10
                            right_speed = 10
                        elif y < -0.04 or y > 0.04:
                            if rotation > 0.4:
                                left_speed = -10
                                right_speed = 10
                                print("1")
                            elif y < -0.04:
                                left_speed = -10
                                right_speed = -10
                                print("2")
                            elif y > 0.04:
                                left_speed = 10
                                right_speed = 10
                                print("3")
                            elif rotation < 1.2 or rotation > 1.6: 
                                left_speed = 10
                                right_speed = -10
                            else:
                                left_speed = 0
                                right_speed = 0
                                print("4")
                        else:
                            left_speed = -10
                            right_speed = -10
                else:
                    if x_ball < 0.02 and x_ball > -0.1 and y_ball > -0.025 and y_ball < 0.025:

                        if dy > 0 and dy < 0: 
                            left_speed = -10
                            right_speed = -10
                        elif dy < 0 and dy > mg:
                            left_speed = -10
                            right_speed = -10 - p
                            print(1)
                        elif dy > 0 and dy < pg:
                            left_speed = -10 + p
                            right_speed = -10
                            print(2)
                        elif dy < mg and dy > -l:
                            left_speed = -10
                            right_speed = -10 - m
                            print(3)
                        elif dy > pg and dy < l:
                            left_speed = -10 + m
                            right_speed = -10
                            print(4)
                        elif dy > l:
                            left_speed = -10 + g
                            right_speed = -10
                            print(5)
                        elif dy < -l:
                            left_speed = -10
                            right_speed = 10 - g
                            print(6)
                        else:
                            left_speed = 0
                            right_speed = 0
                    else: 
                        if rotation < -1.92 or rotation > -1.48 and y > -0.04 and y < 0.04:
                            print("drehen")
                            left_speed = 10
                            right_speed = -10
                        elif x < 0.1:
                            left_speed = 10
                            right_speed = 10
                        elif x > 0.4:
                            left_speed = -10
                            right_speed = -10
                        elif y < -0.04 or y > 0.04:
                            if rotation < -0.4 or rotation > 0.4:
                                left_speed = 10
                                right_speed = -10
                                print("r")
                            elif y < -0.04:
                                left_speed = -10
                                right_speed = -10
                            elif y > 0.04:
                                left_speed = 10
                                right_speed = 10
                            else: 
                                if rotation < -1.92 or rotation > -1.48:
                                    print("drehen")
                                    left_speed = 10
                                    right_speed = -10
                                else:
                                    left_speed = 0
                                    right_speed = 0
                        else:
                            left_speed = -10
                            right_speed = -10

                # Set the speed to motors
                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)


my_robot = MyRobot()
my_robot.run()
