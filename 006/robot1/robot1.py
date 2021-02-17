import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
sys.path.append('/app/controllers')

# rcj_soccer_player controller - ROBOT B1

# Feel free to import built-in libraries
import math

# You can also import scripts that you put into the folder with controller
from team_006_libraries.robot1.rcj_soccer_keeper_robot import RCJSoccerRobot, TIME_STEP, line_posB, line_posY
from team_006_libraries.robot1 import utils

x = 1
y = 1
i = 1
Check = 1
Linie = 0
CheckA = 0
CheckB = 0


class MyRobot(RCJSoccerRobot):
    def run(self):
        global Check, CheckB
        global Linie
        global line_posB, line_posY
        team = self.team
        print ('Team:', team)
        while self.robot.step(TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()
                if team == 'B':
                    line_pos = line_posB
                if team == 'Y':
                    line_pos = line_posY
                print ('Line Position:', line_pos)
                # Get the position of our robot
                robot_pos = data[self.name]
                
                # Get the position of the ball
                ball_pos = data['ball']
                ball_angle, robot_angle = self.get_angles(line_pos, robot_pos)
                direction = utils.get_direction(ball_angle)
                robot_ori = data[self.name]['orientation']
                
                #Variabeln setzen für Reset
                
                                
                #Berechnung der Richtung zum Strafraumpunkt
                x = (line_pos['x'] - robot_pos['x'])
                y = (ball_pos['y'] - robot_pos['y'])
                z = (abs(ball_pos['x']) - abs(robot_pos['x']))
                ä = (ball_pos['x'] * robot_pos['x'])
                ß = (robot_pos['x'] * robot_pos['y'])
                
                print('z:', z)
                print('ß:', ß)
                
                if y < 0:
                    y = y - 10.0
                if y > 0:
                    y = y + 10.0
                if y < -10:
                    y = -10
                if y > 10:
                    y = 10
                if z > 0:
                    z = z + 10.0
                if z < 0:
                    z = z - 10.0
                if z < -10:
                    z = -10
                if z > 10:
                    z = 10
                    
                print('x:', x)
                print('y:', y)
                
                print('position:', robot_pos)
                print('ball_pos', ball_pos)
                print('orientation:', robot_ori)
                
                
                #Zum Strafraum fahren
                if abs(x) <= 0.04 and Check == 1:
                    Linie = 1
                    print("Bin da!")
                    
                    right_speed = 0
                    left_speed = 0
              
                    #print ('Linie:', Linie)

                    #ausrichten
                    robot_ori = data[self.name]['orientation']
                    if robot_ori <= 2.9 and robot_ori >= -3.1 and Linie == 1 and CheckA != 1:
                        
                        print('ich drehe mich')
                        #print('Linie:', Linie)
                        left_speed = 10
                        right_speed = -10 
                        self.left_motor.setVelocity(left_speed)
                        self.right_motor.setVelocity(right_speed)
                    else:
                        print('Ich habe mich ausgerichtet')
                        right_speed = 0
                        left_speed = 0
                        self.left_motor.setVelocity(left_speed)
                        self.right_motor.setVelocity(right_speed)
                        Check = 3
                else:                    
                    Linie = 0 
                    if direction == 0 and Check == 1:
                        left_speed = -10
                        right_speed = -10
                    if direction != 0 and Check == 1:
                        left_speed = direction * 10
                        right_speed = direction * -10
                        
                if Check == 3 and abs(robot_pos['y']) > 0.2 and abs(ball_pos['y']) > 0.2 and abs(ball_pos['x']) >= 0.55:
                    CheckA = 1
                else:
                    CheckA = 0
                
                if ä < 0:
                    CheckA = 0
                
                if robot_pos['x'] < 0.40 and robot_pos['x'] > -0.40:
                    print('Weg hier')
                    Check = 1
                    
                if robot_ori >= -2.4 and robot_ori <= 2.4 and CheckA != 1:
                    print('Weg hier')
                    Check = 1
                                   
                print('Check:', Check)   
                print('CheckA:', CheckA)             
                if Check == 3:
                    left_speed = y
                    right_speed = y
                    if CheckA == 1:
                        if ß > 0:
                            if robot_pos['y'] > 0:
                                left_speed = 10
                                right_speed = -10
                                if abs(robot_ori) < 1.7:
                                    left_speed = z
                                    right_speed = z
                            
                            if robot_pos['y'] <= 0:
                                left_speed = 10
                                right_speed = -10
                                if abs(robot_ori) < 1.7:
                                    left_speed = z * -1
                                    right_speed = z * -1
                        if ß < 0:
                            if robot_pos['y'] < 0:
                                left_speed = -10
                                right_speed = 10
                                if abs(robot_ori) < 1.7:
                                    left_speed = z * -1
                                    right_speed = z * -1
                            if robot_pos['y'] > 0:
                                left_speed = -10
                                right_speed = 10
                                if abs(robot_ori) < 1.7:
                                    left_speed = z * 1 
                                    right_speed = z * 1
                        if abs(ball_pos['x']) < 0.55:
                            Check = 1
                    else:
                        CheckA == 0
                        
                if robot_pos['y'] > 0.42 and Check == 3 and CheckA == 0:
                    left_speed = -10
                    right_speed = -10
                if robot_pos['y'] < -0.42 and Check == 3 and CheckA == 0:
                    left_speed = 10
                    right_speed = 10  
            	
                # Set the speed to motors
                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)



    
my_robot = MyRobot()
my_robot.run()

