import sys
sys.path.append('/app/controllers/')
sys.path.append('.')
# rcj_soccer_player controller - ROBOT B1

# Feel free to import built-in libraries
import math

# You can also import scripts that you put into the folder with controller
from team_002_libraries.robot1.rcj_soccer_robot import RCJSoccerRobot, TIME_STEP
from team_002_libraries.robot1 import utils


data = 0
cc_mal = 0
cc_plus = 0


class MyRobot(RCJSoccerRobot):

    

    def ballsuchen(self):
        while self.robot.step(TIME_STEP) != -1:
            
            data = self.get_new_data()

            if self.team_farbe == 'Y':

                if data[self.me]['x'] + 0.08 * cc_mal > data['ball']['x'] :
                    print("falsch")
                    self.zuruck() 
                else:
                    if self.vorne == 0:
                        #print("richtig")
                        self.left_motor.setVelocity(0)
                        self.right_motor.setVelocity(0)
                        if data[self.me]['orientation'] < self.ziel_dir - 0.1:                    
                            self.left_motor.setVelocity(8)
                            self.right_motor.setVelocity(4) 
                        elif data[self.me]['orientation'] > self.ziel_dir + 0.1:   
                            self.left_motor.setVelocity(4)
                            self.right_motor.setVelocity(8)
                        else:
                            #print("richtige richtung")
                            self.left_motor.setVelocity(10)
                            self.right_motor.setVelocity(10)
                    else:
                        #print("richtig")
                        self.left_motor.setVelocity(0)
                        self.right_motor.setVelocity(0)
                        if data[self.me]['orientation'] < self.ziel_dir - 0.1:                  
                            self.left_motor.setVelocity(-4)
                            self.right_motor.setVelocity(-8)
                            #print("links")
                        elif data[self.me]['orientation'] > self.ziel_dir + 0.1:   
                            self.left_motor.setVelocity(-8)
                            self.right_motor.setVelocity(-4)
                            #print("rechts")
                        else:
                            #print("richtige richtung")
                            self.left_motor.setVelocity(-10)
                            self.right_motor.setVelocity(-10) 
                break
            else:
                if data[self.me]['x'] + 0.08 * cc_mal < data['ball']['x'] :
                    print("falsch")
                    self.zuruck() 
                else:
                    if self.vorne == 0:
                        #print("richtig")
                        self.left_motor.setVelocity(0)
                        self.right_motor.setVelocity(0)
                        if data[self.me]['orientation'] < self.ziel_dir - 0.1:                    
                            self.left_motor.setVelocity(8)
                            self.right_motor.setVelocity(4)
                        elif data[self.me]['orientation'] > self.ziel_dir + 0.1:   
                            self.left_motor.setVelocity(4)
                            self.right_motor.setVelocity(8)
                        else:
                            #print("richtige richtung")
                            self.left_motor.setVelocity(10)
                            self.right_motor.setVelocity(10)
                    else:
                        #print("richtig")
                        self.left_motor.setVelocity(0)
                        self.right_motor.setVelocity(0)
                        if data[self.me]['orientation'] < self.ziel_dir - 0.1:                  
                            self.left_motor.setVelocity(-4)
                            self.right_motor.setVelocity(-8)
                            #print("links")
                        elif data[self.me]['orientation'] > self.ziel_dir + 0.1:   
                            self.left_motor.setVelocity(-8)
                            self.right_motor.setVelocity(-4)
                            #print("rechts")
                        else:
                            #print("richtige richtung")
                            self.left_motor.setVelocity(-10)
                            self.right_motor.setVelocity(-10) 
                break

    def zuruck(self):
        print("anfang von zuruck")
        while self.robot.step(TIME_STEP) != -1:
            data = self.get_new_data()
            if self.team_farbe == 'Y':
                if data[self.me]['x'] + 0.25 > data['ball']['x']:
                    print("neue daten")
                    if data[self.me]['orientation'] > 1.3 and data[self.me]['orientation'] < 1.8:
                        if data[self.me]['orientation'] >= 1.57:
                            print(data[self.me]['orientation'])
                            self.left_motor.setVelocity(9)
                            self.right_motor.setVelocity(10)                        
                        else:
                            print(data[self.me]['orientation'])
                            self.left_motor.setVelocity(10)
                            self.right_motor.setVelocity(9)

                    elif data[self.me]['orientation'] >= 1.4 or data[self.me]['orientation'] <= -1.4:
                        print(data[self.me]['orientation'])
                        self.left_motor.setVelocity(2)
                    elif data[self.me]['orientation'] < 1.4 or data[self.me]['orientation'] > -1.4:
                        print(data[self.me]['orientation'])
                        self.left_motor.setVelocity(10)
                        self.right_motor.setVelocity(2)
                else:
                    break
            else:
                if data[self.me]['x'] - 0.25 < data['ball']['x']:
                    print("neue daten")
                    if data[self.me]['orientation'] < -1.3 and data[self.me]['orientation'] > -1.8:
                        if data[self.me]['orientation'] <= -1.57:
                            print(data[self.me]['orientation'])
                            self.left_motor.setVelocity(10)
                            self.right_motor.setVelocity(9)
                        else:
                            print(data[self.me]['orientation'])
                            self.left_motor.setVelocity(9)
                            self.right_motor.setVelocity(10)
                    elif data[self.me]['orientation'] <= -1.4 or data[self.me]['orientation'] >= 1.4:
                        print(data[self.me]['orientation'])
                        self.left_motor.setVelocity(10)
                        self.right_motor.setVelocity(2)
                    elif data[self.me]['orientation'] > -1.4 or data[self.me]['orientation'] < 1.4:
                        print(data[self.me]['orientation'])
                        self.left_motor.setVelocity(2)
                        self.right_motor.setVelocity(10)
                else:
                    break


    def run(self):



        while self.robot.step(TIME_STEP) != -1:

            if self.is_new_data():
                data = self.get_new_data()

                self.team_farbe = self.team
                spielernummer = self.player_id
                self.me = self.team_farbe + str(spielernummer)



                if self.team_farbe == 'B':
                    cc_mal = 1
                    cc_plus = -math.pi
                elif self.team_farbe == 'Y':
                    cc_mal = -1 
                    cc_plus = math.pi

                print(self.team_farbe)

                # Get the position of our robot
                robot_pos = data[self.name]
                # Get the position of the ball
                ball_pos = data['ball']


                
                ball_angle, robot_angle = self.get_angles(ball_pos, robot_pos)

                # Compute the speed for motors
                direction = utils.get_direction(ball_angle)

                

                self.ydiff = data[self.me]['y']- data['ball']['y']
                self.xdiff = data[self.me]['x']- data['ball']['x'] 

                self.rotation = data[self.me]['orientation']

                
                self.ziel_dir = math.atan2(self.xdiff, self.ydiff)
                self.vorne = 0

                                #-3.14
                    
                #O     -1.57       R

                                #0.000


                print("ydiff: ")
                print(self.ydiff)
                print("xdiff: ")
                print(self.xdiff)
                
                
                print("ziel_dir: ")
                print(self.ziel_dir)                
                print("rotation: ")
                print(data[self.me]['orientation'])



                if self.ziel_dir > -1.57 and self.ziel_dir < 1.57:
                    if self.rotation > self.ziel_dir - 1.57 and self.rotation < self.ziel_dir + 1.57:
                        print("1")
                        self.ziel_dir = math.atan2(self.xdiff, self.ydiff) 
                        self.vorne = 0
                        
                    else:
                        print("2")
                        self.ziel_dir = -math.atan2(self.ydiff, self.xdiff) + math.pi/2 + cc_plus
                        self.vorne = 1
                else:
                    
                    if self.rotation > self.ziel_dir - 1.57 and self.rotation < self.ziel_dir + 1.57:
                        print("3")
                        self.ziel_dir = math.atan2(self.xdiff, self.ydiff)
                        self.vorne = 0
                        
                    else:
                        print("4")
                        self.ziel_dir = -math.atan2(self.ydiff, self.xdiff) - math.pi/2
                        self.vorne = 1
                    
                
                
                self.ballsuchen()

my_robot = MyRobot()
my_robot.run()
