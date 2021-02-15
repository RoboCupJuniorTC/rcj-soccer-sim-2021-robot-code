# rcj_soccer_player controller - ROBOT Y2

###### REQUIRED in order to import files from Y1 controller
import sys
import time
from pathlib import Path
from typing import Tuple
sys.path.append(str(Path('.').absolute().parent))
# You can now import scripts that you put into the folder with your
# robot B1 controller
from rcj_soccer_player_b1 import rcj_soccer_robot, utils
######

# Feel free to import built-in libraries
import math



class MyRobot(rcj_soccer_robot.RCJSoccerRobot):
    
    def run(self):
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

        Defense_point = {'x': -0.75 * Seite, 'y': 0}

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
                    ball_ankunft_y = ball_steigung * -0.7 * Seite + ball_b
                    robot_diffrenz_x = start_robot_pos_x - robot_pos["x"]
                    robot_diffrenz_y = start_robot_pos_y - robot_pos["y"]
                    ball_diffrenz = math.sqrt ((ball_diffrenz_x ** 2) + (ball_diffrenz_y ** 2))
                    ball_direction_angle = math.atan2(ball_diffrenz_x, ball_diffrenz_y)
                    robot_diffrenz = math.sqrt ((robot_diffrenz_x ** 2) + (robot_diffrenz_y ** 2))
                    time_diffrenz = start_time-millis / 1000
                    bot_speed = robot_diffrenz / time_diffrenz
                    ball_speed = ball_diffrenz / time_diffrenz
                    ball_speed_x = ball_diffrenz_x / time_diffrenz
                if counter > 3:
                    counter = 0

                if Seite == 1:
                
                    if (ball_ankunft_y > -0.25 and ball_ankunft_y < 0.25):
                    #setzt die Koordinate vom Defencepoint weg von der Tormitte auf den Ankunftspunkt des Balles im Tor
                        Defense_point = {'x': -0.75, 'y': ball_ankunft_y / 2}
                    else:
                        Defense_point = {'x': -0.75, 'y': 0}
                    
                    
                    Verteidigungsgerade = {
                        
                        'x_diff': (ball_pos['x'] - Defense_point['x']),
                        'y_diff': (ball_pos['y'] - Defense_point['y']),
                        #zieht eine gerade durch die ballpostion und den Defence_point 
                        # y = m*x+b <=> b = y-m*x
                        'm': ((ball_pos['y'] - Defense_point['y']) / (ball_pos['x'] - Defense_point['x'])),
                        'b': (ball_pos['y'] - ((ball_pos['y'] - Defense_point['y']) / (ball_pos['x'] - Defense_point['x']) * ball_pos['x']))
                    }
                    ball_entfernung = {
                        #a^2 + b^2 = c^2
                        #entfernung des Balls zum Defencepoint
                        'c':  math.sqrt((Verteidigungsgerade['x_diff']) ** 2 + (Verteidigungsgerade['y_diff']) ** 2),
                        
                    }


                    #Ball rollt Richtung Tor
                    if (ball_ankunft_y > -0.25 and ball_ankunft_y < 0.25):
                        #berechnen wo der ball ankommt
                        print ("berechnung")
                        print (ball_ankunft_y)
                        if ((ball_pos['x'] < -0.38) and ((ball_pos['y'] > -0.2) or (ball_pos['y'] < 0.2))):
                            position = {'x': ball_pos['x'], 'y': ball_pos['y']}
                            print ("verteidigen")
                            #auf ball fahren weil er in einem nahen bereich vorm tor ist
                        else:
                            position = {'x': Defense_point['x'] + (Verteidigungsgerade['x_diff'] / 2), 'y': Defense_point['y'] + (Verteidigungsgerade['y_diff'] / 2)}
                            # auf mittelpunkt zwischen ankunftspunkt und ball fahren
                    elif (ball_pos['x'] > 0.1):
                        # Coordinaten in coordinatenverfolger einsetzen
                        print ("weg")
                        position = {'x': -0.5, 'y': (Verteidigungsgerade['m'] * -0.5 + Verteidigungsgerade['b'])}
                    

                    elif ((ball_pos['x'] < -0.62) and ((ball_pos['y'] < -0.17) or (ball_pos['y'] > 0.17))):
                        #zum Pfosten fahren und Seiten blockieren
                        #
                        #zeichen muss geändert werden
                        if (robot_pos['x'] > -0.65):
                            if (ball_pos['y'] < -0.17):
                                position = {'x': -0.67, 'y': -0.27}
                            else:
                                position = {'x': -0.67, 'y': 0.27}
                        #wenn der roboter nah an der wand ist fängt er an zur seite auf den ball zu fahren
                        else:
                            position = ball_pos

                    
                    else:
                        #auf Mittelpunkt zwischen ball und tormitte fahren 
                        print ("nah")
                        position = {'x': Defense_point['x'] + (Verteidigungsgerade['x_diff'] / 2), 'y': Defense_point['y'] + (Verteidigungsgerade['y_diff'] / 2)}
                    
                    

                # Roboter ist Blau
                else:
                    if (ball_ankunft_y > -0.25 and ball_ankunft_y < 0.25):
                    #setzt die Koordinate vom Defencepoint weg von der Tormitte auf den Ankunftspunkt des Balles im Tor
                        Defense_point = {'x': 0.75, 'y': ball_ankunft_y / 2}
                    else:
                        Defense_point = {'x': 0.75, 'y': 0}
                    
                    
                    Verteidigungsgerade = {
                        
                        'x_diff': (ball_pos['x'] - Defense_point['x']),
                        'y_diff': (ball_pos['y'] - Defense_point['y']),
                        #zieht eine gerade durch die ballpostion und den Defence_point 
                        # y = m*x+b <=> b = y-m*x
                        'm': ((ball_pos['y'] - Defense_point['y']) / (ball_pos['x'] - Defense_point['x'])),
                        'b': (ball_pos['y'] - ((ball_pos['y'] - Defense_point['y']) / (ball_pos['x'] - Defense_point['x']) * ball_pos['x']))
                    }
                    ball_entfernung = {
                        #a^2 + b^2 = c^2
                        #entfernung des Balls zum Defencepoint
                        'c':  math.sqrt((Verteidigungsgerade['x_diff']) ** 2 + (Verteidigungsgerade['y_diff']) ** 2),
                        
                    }


                    #Ball rollt Richtung Tor
                    if (ball_ankunft_y > -0.25 and ball_ankunft_y < 0.25):
                        #berechnen wo der ball ankommt
                        print ("berechnung")
                        print (ball_ankunft_y)
                        if ((ball_pos['x'] > 0.38) and ((ball_pos['y'] > -0.2) or (ball_pos['y'] < 0.2))):
                            position = {'x': ball_pos['x'], 'y': ball_pos['y']}
                            print ("verteidigen")
                            #auf ball fahren weil er in einem nahen bereich vorm tor ist
                        else:
                            position = {'x': Defense_point['x'] + (Verteidigungsgerade['x_diff'] / 2), 'y': Defense_point['y'] + (Verteidigungsgerade['y_diff'] / 2)}
                            # auf mittelpunkt zwischen ankunftspunkt und ball fahren
                    elif (ball_pos['x'] < -0.1):
                        # Coordinaten in coordinatenverfolger einsetzen
                        print ("weg")
                        position = {'x': 0.5, 'y': (Verteidigungsgerade['m'] * 0.5 + Verteidigungsgerade['b'])}
                    

                    elif ((ball_pos['x'] > 0.62) and ((ball_pos['y'] < -0.17) or (ball_pos['y'] > 0.17))):
                        #zum Pfosten fahren und Seiten blockieren
                        #
                        #zeichen muss geändert werden
                        if (robot_pos['x'] < 0.65):
                            if (ball_pos['y'] < -0.17):
                                position = {'x': 0.67, 'y': -0.27}
                            else:
                                position = {'x': 0.67, 'y': 0.27}
                        #wenn der roboter nah an der wand ist fängt er an zur seite auf den ball zu fahren
                        else:
                            position = ball_pos

                    
                    else:
                        #auf Mittelpunkt zwischen ball und tormitte fahren 
                        print ("nah")
                        position = {'x': Defense_point['x'] + (Verteidigungsgerade['x_diff'] / 2), 'y': Defense_point['y'] + (Verteidigungsgerade['y_diff'] / 2)}
                    
                #berechnung welcher roboter am nächsten zum verteidigungsort ist
                
                robot_self_to_defence = math.sqrt((position['x'] - robot_pos['x']) ** 2 + (position['y'] - robot_pos['y']) ** 2)
                robot_1_to_defence = math.sqrt((position['x'] - data[player1]['x']) ** 2 + (position['y'] - data[player1]['y']) ** 2)
                robot_2_to_defence = math.sqrt((position['x'] - data[player2]['x']) ** 2 + (position['y'] - data[player2]['y']) ** 2)

                if (robot_self_to_defence < robot_1_to_defence and robot_self_to_defence < robot_2_to_defence):
                    print ('ich')

                pRegler, direction = utils.p_regler( position, robot_pos, 0, 0)
                left_speed, right_speed = utils.p_regler_drive(pRegler, 20, direction)
                # Set the speed to motors                 
                self.left_motor.setVelocity(left_speed)                 
                self.right_motor.setVelocity(right_speed)

                

my_robot = MyRobot()
my_robot.run()
