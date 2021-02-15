###### REQUIRED in order to import files from B1 controller
import sys
import time
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
# robot B1 controller
try:
    from rcj_soccer_player_b1 import hey
    print("blue")
    from rcj_soccer_player_b1 import rcj_soccer_robot, utils
except:
    print("yellow")
    from rcj_soccer_player_y1 import rcj_soccer_robot, utils

import math



class MyRobot(rcj_soccer_robot.RCJSoccerRobot):
    def run(self):
        y = 0
        while self.robot.step(rcj_soccer_robot.TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()

                # Get the position of our robot
                robot_pos = data[self.name]
                # Get the position of the ball
                ball_pos = data['ball']



                # Get angle between the robot and the ball
                # and between the robot and the north
                ball_angle, robot_angle = self.get_angles(ball_pos, robot_pos)

                # Compute the speed for motors
                direction = utils.get_direction(ball_angle)
                


                

                if self.team == 'B':
                    print("blau")
                    # Position von B2 Roboter
                    b2_x = data['B2']['x']
                    b2_y = data['B2']['y']
                    b2_rotation = data['B2']['orientation']

                    # Wenn der Roboter am Anfang ist nach hinten bis zur höhe des Tores
                    if robot_pos["x"] < 0.5 and y == 0 and b2_rotation > -1.7 and b2_rotation < -1.4:
                        left_speed = 10
                        right_speed = 10
                        print("Anfang")


                    #wenn der Ball auf meiner Seite vor das tor hin und her fahren
                    elif ball_pos["x"] >= 0 and y == 1:
                        #Wenn der Ball hinter dir ist nach hinten fahren       
                        if ball_pos["x"] > robot_pos["x"]:
                            if b2_rotation <-1.7:
                                left_speed = 10
                                right_speed = -10
                            elif b2_rotation > -1.4:
                                left_speed = -10
                                right_speed = 10
                            elif robot_pos["x"] < ball_pos["x"]:
                                left_speed = 10
                                right_speed = 10
                        #Drehung, damit der vor dem Tor fahren kann
                        elif  b2_rotation < -0.3 or b2_rotation > 0.3:
                            print("drehen")
                            left_speed = 10
                            right_speed = -10
                        #Ball verfolgen
                        elif robot_pos["y"] < ball_pos["y"]:
                            print("verfolgung1")
                            y = 1
                            left_speed = -10
                            right_speed = -10
                        elif robot_pos["y"] > ball_pos["y"]:
                            print("verfolgung2")
                            y = 1
                            left_speed = 10
                            right_speed = 10 
                        

                    #wenn der Ball vorne ist roboter nach vorne auf höhe des Balls              
                    elif ball_pos["x"] < 0 and y == 1:
                        #Wenn der Ball in der Torzone ist nach vorne
                        if robot_pos["x"] > 0.6:
                            if b2_rotation < -1.7:
                               left_speed = 5
                               right_speed = -5
                            elif b2_rotation > -1.4:
                                left_speed = -5
                                right_speed = 5
                            elif robot_pos["x"] > 0.6:
                                left_speed = -10
                                right_speed = -10
                        elif robot_pos["x"] < 0.4:
                            if b2_rotation < -1.7:
                                left_speed = 5
                                right_speed = -5
                            elif b2_rotation > -1.4:
                                left_speed = -5
                                right_speed = 5
                            elif robot_pos["x"] < 0.55:
                                left_speed = 10
                                right_speed = 10
                        #richten
                        elif b2_rotation < -0.2:
                            left_speed = 5
                            right_speed = -5
                            print("richten")
                        elif b2_rotation > 0.2:
                            left_speed = -5
                            right_speed = 5
                            print("richten")
                        #vor dem Tor fahren
                        elif robot_pos["y"] > 0.15:
                            left_speed = 10
                            right_speed = 10
                        elif robot_pos["y"] < -0.15:
                            left_speed = -10
                            right_speed = -10
                        else:
                            left_speed = -10
                            right_speed = -10

                        print("fahren")
                        
                    #wichtig, damit der Roboter immer am anfang nach hinten fährt
                    elif robot_pos["x"] >= -0.3 and y== 1:
                        y = 0
                            
                        
                    else:
                        y = 1


                    # Set the speed to motors
                    #falls der sich nicht bewegt zitat paul "weg damit" :D
                    self.left_motor.setVelocity(left_speed)
                    self.right_motor.setVelocity(right_speed)
                if self.team == 'Y':
                    print("gelb")                
                    y2_x = data['Y2']['x']
                    y2_y = data['Y2']['y']
                    y2_rotation = data['Y2']['orientation']
                    # Wenn der Roboter am Anfang ist nach hinten bis zur höhe des Tores
                    if robot_pos["x"] > -0.5 and y == 0 and y2_rotation < 1.6 and y2_rotation > 1.4:
                        left_speed = 10
                        right_speed = 10
                        print("Anfang")

                
                    #wenn der Ball auf meiner Seite vor das tor hin und her fahren
                    elif ball_pos["x"] <= 0 and y == 1: 
                        if ball_pos["x"] < robot_pos["x"]:
                            print("Ballhintermir")
                            if y2_rotation > 1.7:
                                left_speed = -10
                                right_speed = 10
                                print("drehen1")
                            elif y2_rotation < 1.3:
                                left_speed = 10
                                right_speed =-10
                                print("drehen2")
                            elif robot_pos["x"] >= ball_pos["x"]:
                                left_speed = 10
                                right_speed = 10
                                print("zurück")
                       # Drehung, damit der vor dem Tor fahren kann
                        elif  y2_rotation >= 0.4 or y2_rotation <= -0.1:
                            print("drehen")
                            left_speed = -10
                            right_speed = 10
                        #Ball verfolgen
                        elif robot_pos["y"] < ball_pos["y"]:
                            print("verfolgung1")
                            y = 1
                            left_speed = -10
                            right_speed = -10
                        elif robot_pos["y"] > ball_pos["y"]:
                            print("verfolgung2")
                            y = 1
                            left_speed = 10
                            right_speed = 10 

                    #wenn der Ball vorne ist roboter nach vorne auf höhe des Balls              
                    elif ball_pos["x"] > 0 and y == 1:
                        #muss noch bearbeitetwerden
                        #Wenn der Ball in der Torzone ist nach vorne
                        if robot_pos["x"] < -0.5:
                            print("zu weit hinten")
                            if y2_rotation > 1.7:
                               left_speed = -5
                               right_speed = 5
                            elif y2_rotation < 1.3:
                                left_speed = 5
                                right_speed = -5
                            elif robot_pos["x"] <= -0.4:
                                left_speed = -10
                                right_speed = -10
                        elif robot_pos["x"] > -0.45:
                            print("zu weit vorne")
                            if y2_rotation > 1.7:
                                left_speed = -5
                                right_speed = 5
                            elif y2_rotation < 1.3:
                                left_speed = 5
                                right_speed = -5
                            elif robot_pos["x"] >= -0.45:
                                left_speed = 10
                                right_speed = 10
                                print("bye")
                          
                        #richten 
                        elif y2_rotation < -0.1:
                            left_speed = 5
                            right_speed = -5
                            print("richten")
                        elif y2_rotation > 0.1:
                            left_speed = -5
                            right_speed = 5
                            print("richten")
                        #vor dem Tor fahren
                        elif robot_pos["y"] > 0.15:
                            left_speed = 10
                            right_speed = 10
                        elif robot_pos["y"] < -0.15:
                            left_speed = -10
                            right_speed = -10
                        else:
                            left_speed = -10
                            right_speed = -10

                        print("fahren")

                        
                    #wichtig, damit der Roboter immer am anfang nach hinten fährt
                    elif robot_pos["x"] > -0.3 and y== 1:
                        y = 0

                              
                    else:
                        y = 1
                        print("Ende")
                        left_speed = 0
                        right_speed = 0
                    self.left_motor.setVelocity(left_speed)
                    self.right_motor.setVelocity(right_speed)
            
my_robot = MyRobot()
my_robot.run()