# rcj_soccer_player controller - ROBOT B2
#Final
#----------------------------------------------------------------- DO NOT CHANGE OR DELETE
import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))

from rcj_soccer_player_b1 import rcj_soccer_robot, utils, minhas_tarefas
from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP
#-----------------------------------------------------------------------------------------
#----------------------------------------------------------------IMPORT BUILT_IN LIBRARIES
# Feel free to import built-in libraries here

#----------------------------------------------------------------- DO NOT CHANGE OR DELETE
import math


OP_GOAL = [-0.856, 0] # Opponent's goal position [x, y]
OWN_GOAL = [0.856, 0] # Own's goal position [x, y]
counter = 0
score = [0, 0]
GOAL_FLAG = False
TIME_FLAG = False
IMPORT_FLAG = False
GOAL_DEFAULT_DIST = 0.4
goal_time = 0
STOP_NEAR_GOALKEEPER = True
KICK_FLAG = 0
KICK_INTENSITY_DEFAULT = 5
GP = 0
GC = 0
RP = 0
BP = 0
#------------------------------------------------------------------------------------------

class MyRobot(rcj_soccer_robot.RCJSoccerRobot):

    def LadoCampo(self):
        while self.robot.step(TIME_STEP) != -1:

            if self.is_new_data():
                data = self.get_new_data()
                robot_pos = data[self.name]

                if robot_pos['x'] < 0:
                    valor = -1
                    print("sou amarelo")
                    GP = 0
                    GC = 1
                else:
                    valor = 1
                    print("sou azul")
                    GP = 1
                    GC = 0
                return valor  
                
    def run(self, counter, score, goal_time, GOAL_FLAG, TIME_FLAG, IMPORT_FLAG, KICK_FLAG):
        
        lado = self.LadoCampo()
        
        while self.robot.step(rcj_soccer_robot.TIME_STEP) != -1:
            if self.is_new_data():
                
                # ********************************************************************
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
                AnguloRobot = math.degrees(robot_pos['orientation'])
                DistBall = math.sqrt((robot_pos['x']-ball_pos['x'])**2 + (robot_pos['y']-ball_pos['y'])**2)
                
                
                game_clock, counter = minhas_tarefas.game_time (counter)
                score, goal_time, GOAL_FLAG, TIME_FLAG = minhas_tarefas.scoreboard (data, score, game_clock, goal_time,GOAL_FLAG, TIME_FLAG)
                
           
                if lado == 1:
                    GP = 1
                    GC = 0
                else:
                    GP = 0
                    GC = 1
                    
                RP = -0.15
                BP = -0.15
                
                #adequação da estratégia
                if counter > 2800 or score[GP] - score[GC] < 0:
                    if score[GP] - score[GC] < 2:
                        #muda a estratégia 
                        RP = -1
                        BP = -1
                        print("estrategia 2")
                        
                
                print(counter)
                #4675 é o valor correspondente a 5 min de game 
                
                print("meu placar")
                print(score[GP]) #score[GP] é o comando para pegar quantos gols nos fizemos
                print("placar adv")
                print(score[GC]) #score[GC] é o comando para pegar quantos gols levamos
                 
                if ball_angle < 0:
                    AnguloABS = 360 + ball_angle 
                else:
                    AnguloABS = ball_angle

                if AnguloABS > 180:
                    AnguloABS = AnguloABS - 360
                    
                # If the robot has the ball right in front of it, go forward,
                # rotate otherwise
                #print(ball_pos['y'])
                #print (AnguloABS)
                print(lado)
                if ball_pos['x'] * lado > 0.4 and ball_pos['y'] * lado < -0.35:
                    
                    print("espera o respanw")
                    if robot_pos['y'] * lado > 0.06 or robot_pos['y'] * lado < -0.06:
                        if robot_pos['y'] * lado > 0.06:
                            dir = -1 * lado
                        elif robot_pos['y'] * lado < -0.06:
                            dir = 1 * lado
                        alvo = -150 * lado
                        
                        left_speed  = dir * 10 - (AnguloRobot-alvo)/2
                        right_speed = dir * 10 + (AnguloRobot-alvo)/2
                        
                    elif robot_pos['x'] * lado > 0.25 or robot_pos['x'] * lado < 0.2:
                        if robot_pos['x'] * lado > 0.25:
                            dir = -1
                        elif robot_pos['x'] * lado < 0.2:
                            dir = 1
                            
                        alvo = -90 * lado
                        
                        left_speed  = dir * 10 - (AnguloRobot-alvo)/2
                        right_speed = dir * 10 + (AnguloRobot-alvo)/2
                    
                    else: 
                        left_speed  = 3
                        right_speed = 3
                
                elif ball_pos['x'] * lado < -0.7 and ball_pos['y'] * lado < 0:
                   
                    print("ajuda empurrar")
                    
                    if robot_pos['x'] * lado < -0.6:
                       print("ST3")
                       if lado == 1:
                           alvo = -30 * lado
                       else:
                           alvo = -150 * lado
                       print(alvo)
                       print(AnguloRobot)
                       left_speed  = -10 - (AnguloRobot-alvo)/2
                       right_speed = -10 + (AnguloRobot-alvo)/2 
                       
                    elif robot_pos['y'] * lado > -0.55:
                       print("ST1")
                       if lado == 1:
                           alvo = -150 * lado
                       else:
                           alvo = -30 * lado
                       print(alvo)
                       print(AnguloRobot) 
                       left_speed  = -10 - (AnguloRobot-alvo)/2
                       right_speed = -10 + (AnguloRobot-alvo)/2
                    
                    else:  
                       alvo = -90 * lado
                       print("ST2")
                       print(alvo)
                       print(AnguloRobot)
                       left_speed  = -10 - (AnguloRobot-alvo)/2
                       right_speed = -10 + (AnguloRobot-alvo)/2 
                                          
                
                elif robot_pos['y'] * lado > RP or ball_pos['y'] * lado > BP:
                    print("corre atras da bola")
                    print(DistBall)
                    if AnguloABS < 20 and AnguloABS > -20:

                        G1 = AnguloABS/10
    
                        left_speed = -10 - G1
                        right_speed = -10 + G1
                        
                       
                                
                    elif AnguloABS >= 20:
                        left_speed = -10
                        right_speed = 10
                        
                    else: 
                        left_speed = 10
                        right_speed = -10
                else:
                    if AnguloABS < 40:
                       dir = -1
                       #print("angulo menor que -45")
                       #print(AnguloABS)
                    else:
                        dir = 1
                       # print("angulo maior que -45")
                       # print(AnguloABS)
                    alvo = -90 * lado

                    left_speed  = dir * 8 - (AnguloRobot-alvo)/2
                    right_speed = dir * 8 + (AnguloRobot-alvo)/2
                
                if left_speed > 10:
                    left_speed = 10
                    
                if left_speed < -10:
                    left_speed = -10
                        
                if right_speed > 10:
                    right_speed = 10
                        
                if right_speed < -10:
                    right_speed = -10 
               
                
                
                 # Set the speed to motors
                 
                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)

                    
                # ********************************************************************


my_robot = MyRobot()
my_robot.run(counter, score, goal_time, GOAL_FLAG, TIME_FLAG, IMPORT_FLAG, KICK_FLAG)