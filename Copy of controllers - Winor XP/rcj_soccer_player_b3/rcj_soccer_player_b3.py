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
import math


class MyRobot(rcj_soccer_robot.RCJSoccerRobot):
    def run(self):
        leeway = 0.0
        counter = 0
        counter = 0
        time_diffrenz = 0
        bot_speed = 0
        ball_speed = 0
        ball_speed_x = 0
        millis = (self.robot.getTime() * 1000)
        laufzeit = millis
        ball_diffrenz_x = 0
        ball_diffrenz_y = 0
        ball_ankunft_y = 0
        if (self.name == 'B1'):
            Seite = -1
            player1 = 'B2'
            player2 = 'B3'
        elif (self.name == 'B2'):
            Seite = -1
            player1 = 'B1'
            player2 = 'B3'
        elif (self.name == 'B3'):
            Seite = -1
            player1 = 'B1'
            player2 = 'B2'
        elif (self.name == 'Y1'):
            Seite = 1
            player1 = 'Y2'
            player2 = 'Y3'
        elif (self.name == 'Y2'):
            Seite = 1
            player1 = 'Y1'
            player2 = 'Y3'
        else:
            Seite = 1
            player1 = 'Y1'
            player2 = 'Y2'
        while self.robot.step(rcj_soccer_robot.TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()
                #blue = 1, yellow = -1: NOCH NICHT EINPROGRAMMIERT
                bot_team = 1

                # Get the position of our robot
                robot_pos = data[self.name]
                if (Seite == -1):
                    other_robot_pos = data['B1']
                else:
                    other_robot_pos = data['Y1']
                # Get the position of the ball
                ball_pos = data['ball']
                millis = (self.robot.getTime() * 1000)
                
                counter += 1
                
                if counter == 1:
                    start_ball_pos_x = ball_pos["x"]
                    start_ball_pos_y = ball_pos["y"]
                    start_robot_pos_x = robot_pos["x"]
                    start_robot_pos_y = robot_pos["y"]
                    start_time = millis / 1000
                if counter == 3:
                    ball_diffrenz_x = start_ball_pos_x - ball_pos["x"]
                    ball_diffrenz_y = start_ball_pos_y - ball_pos["y"]
                    if ball_diffrenz_x == 0:
                        ball_diffrenz_x = 0.001
                    if ball_diffrenz_y == 0:
                        ball_diffrenz_y = 0.001
                    ball_steigung = ball_diffrenz_y / ball_diffrenz_x
                    ball_b = ball_pos["y"] - ball_steigung * ball_pos["x"]
                    ball_ankunft_y = ball_steigung * -0.6 * Seite + ball_b
                    robot_diffrenz_x = start_robot_pos_x - robot_pos["x"]
                    robot_diffrenz_y = start_robot_pos_y - robot_pos["y"]
                    ball_diffrenz = math.sqrt ((ball_diffrenz_x ** 2) + (ball_diffrenz_y ** 2))
                    ball_direction_angle = math.atan2(ball_diffrenz_x, ball_diffrenz_y)
                    robot_diffrenz = math.sqrt ((robot_diffrenz_x ** 2) + (robot_diffrenz_y ** 2))
                    time_diffrenz = start_time-millis / 1000
                    bot_speed = robot_diffrenz / time_diffrenz
                    ball_speed = (ball_diffrenz / time_diffrenz) *-1
                    ball_speed_x = ball_diffrenz_x / time_diffrenz
                if counter > 3:
                    counter = 0

                if ((robot_pos['x'] - ball_pos['x'])**2 + (robot_pos['y'] - ball_pos['y'])**2) >  ((other_robot_pos['x'] - ball_pos['x'])**2 + (other_robot_pos['y'] - ball_pos['y'])**2):
                    # if (ball_speed < 0.06):
                    
                    #     drive_pos = {'x': -0.1 * Seite, 'y': 0}

                    # else:
                    #     if ball_pos['x'] < -0.2:
                    #         if ball_pos['x'] < robot_pos['x']:
                    #             drive_pos = ball_pos
                    #         elif ball_pos['y'] < 0:
                    #             drive_pos = {'x': -0.6, 'y': 0.2}
                    #         else:
                    #             drive_pos = {'x': -0.6, 'y': -0.2}
                    #     else:
                    #         if ball_pos['y'] < 0:
                    #             drive_pos = {'x': -0.50, 'y': 0.3}
                    #         else:
                    #             drive_pos = {'x': -0.50, 'y': -0.3}
                    drive_pos = {'x': -0.1 * Seite, 'y': 0}
                    pRegler, direction = utils.p_regler(drive_pos, robot_pos, 0, 0)
                    left_speed, right_speed = utils.p_regler_drive(pRegler, 10, direction)
                    
                else:
                    #ausrechnen des Winkels zum Ball
                    if ball_pos['x'] != -0.7:
                        alpha = math.atan(ball_pos['y']/(-0.7 - ball_pos['x'])) * -1
                    else:
                        alpha = math.atan(ball_pos['y']/0.00000000000001) * -1
                    
                    #print(alpha)
                    if (Seite == -1):
                        if ((((robot_pos['x'] - ball_pos['x'] - (math.cos(alpha) * 0.06))**2) + (((robot_pos['y'] - ball_pos['y']) - (math.sin(alpha) * 0.06))**2))**0.5) < (0.04 + leeway):
                            cord_x = 0
                            cord_y = 0
                            leeway = 0.03
                        elif ball_pos['y'] < 0:
                            leeway = 0
                            if (robot_pos['x'] - ball_pos['x']) > 0.08:
                                cord_x = (math.cos(alpha) * 0.1)
                                cord_y = (math.sin(alpha) * 0.1)
                                print('Green')
                            
                            elif (robot_pos['y'] - ball_pos['y']) > 0.08:
                                cord_x = 0.09
                                cord_y = 0.09
                                print('Red')
                            
                            elif (robot_pos['x'] - ball_pos['x']) < -0.08:
                                cord_x = -0.09
                                cord_y = 0.09
                                print('Blue')

                            elif (robot_pos['y'] - ball_pos['y']) < -0.08:
                                cord_x = 0.09
                                cord_y = -0.09
                                print('Black')
                        else:
                            leeway = 0
                            if (robot_pos['x'] - ball_pos['x']) > 0.08:
                                cord_x = (math.cos(alpha) * 0.09)
                                cord_y = (math.sin(alpha) * 0.09)
                                print('Green2')
                            
                            elif (robot_pos['y'] - ball_pos['y']) < -0.08:
                                cord_x = 0.09
                                cord_y = -0.09
                                print('Red2')
                            
                            elif (robot_pos['x'] - ball_pos['x']) < -0.08:
                                cord_x = -0.09
                                cord_y = -0.09
                                print('Blue2')

                            elif (robot_pos['y'] - ball_pos['y']) > 0.08:
                                cord_x = 0.09
                                cord_y = 0.09
                                print('Black2')
                    else:
                        if ((((robot_pos['x'] - ball_pos['x'] + (math.cos(alpha) * 0.06))**2) + (((robot_pos['y'] - ball_pos['y']) + (math.sin(alpha) * 0.06))**2))**0.5) < (0.04 + leeway):
                            cord_x = 0
                            cord_y = 0
                            leeway = 0.03
                            print('attack')
                        elif ball_pos['y'] > 0:
                            leeway = 0
                            if (robot_pos['x'] - ball_pos['x']) < -0.08:
                                cord_x = (math.cos(alpha) * 0.1) * -1
                                cord_y = (math.sin(alpha) * 0.1) * -1
                                print('Green')
                            
                            elif (robot_pos['y'] - ball_pos['y']) < -0.08:
                                cord_x = -0.09
                                cord_y = -0.09
                                print('Red')
                            
                            elif (robot_pos['x'] - ball_pos['x']) > 0.08:
                                cord_x = 0.09
                                cord_y = -0.09
                                print('Blue')

                            elif (robot_pos['y'] - ball_pos['y']) > 0.08:
                                cord_x = -0.09
                                cord_y = 0.09
                                print('Black')
                        else:
                            leeway = 0
                            if (robot_pos['x'] - ball_pos['x']) < -0.08:
                                cord_x = (math.cos(alpha) * 0.09) * -1
                                cord_y = (math.sin(alpha) * 0.09) * -1
                                print('Green2')
                            
                            elif (robot_pos['y'] - ball_pos['y']) > 0.08:
                                cord_x = -0.09
                                cord_y = 0.09
                                print('Red2')
                            
                            elif (robot_pos['x'] - ball_pos['x']) > 0.08:
                                cord_x = 0.09
                                cord_y = 0.09
                                print('Blue2')

                            elif (robot_pos['y'] - ball_pos['y']) < -0.08:
                                cord_x = -0.09
                                cord_y = -0.09
                                print('Black2')
                    

                    pRegler, direction = utils.p_regler(ball_pos, robot_pos, cord_x, cord_y)

                    left_speed, right_speed = utils.p_regler_drive(pRegler, 14, direction)

                # Set the speed to motors
                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)

                '''print(leeway)
                print(robot_pos)
                print(pRegler)
                print(round(pRegler))
                print((robot_pos['y'] - ball_pos['y']) / ((robot_pos['x'] - ball_pos['x']) - 0.07))
                print(robot_pos['x'] - ball_pos['x'])
                print(robot_pos['y'] - ball_pos['y'])'''

my_robot = MyRobot()
my_robot.run()
