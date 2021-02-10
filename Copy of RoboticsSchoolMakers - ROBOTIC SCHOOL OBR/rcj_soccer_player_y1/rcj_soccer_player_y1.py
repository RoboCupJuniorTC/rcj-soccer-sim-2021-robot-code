# rcj_soccer_player controller - ROBOT Y1
# FINAL
# Feel free to import built-in libraries
import math

# You can also import scripts that you put into the folder with controller
from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP
import utils
import minhas_tarefas

dir = 0
DistBall = 0
AnguloABS = 0
AnguloRobot = 0     
FechaBola = 0 
lado = 0
tempo = 0
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
MIRROR_FLAG = True
CONTANDO_FLAG = False
BALL_AREA = [0, 0, 0, 0]
INICIO = 0
GP = 0
GC = 0
OFENSIVO = False
left_speed = 0
right_speed = 0

class Goleiro(RCJSoccerRobot):
    
     
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
                                       
    def PosDef(self, counter, score, goal_time, GOAL_FLAG, TIME_FLAG, IMPORT_FLAG, KICK_FLAG, CONTANDO_FLAG, BALL_AREA, INICIO):
    
        lado = self.LadoCampo()
             
        while self.robot.step(TIME_STEP) != -1:
           
                
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

                # If the robot has the ball right in front of it, go forward,
                # rotate otherwise
                
                #calculo distancia do robo para a bola
                DistBall = math.sqrt((robot_pos['x']-ball_pos['x'])**2 + (robot_pos['y']-ball_pos['y'])**2)
            
                game_clock, counter = minhas_tarefas.game_time (counter)
                score, goal_time, GOAL_FLAG, TIME_FLAG = minhas_tarefas.scoreboard (data, score, game_clock, goal_time,GOAL_FLAG, TIME_FLAG)
                
                if lado == 1:
                    GP = 1
                    GC = 0
                else:
                    GP = 0
                    GC = 1
                
                print(counter)
                #4675 é o valor correspondente a 5 min de game 
                print("meu placar")
                print(score[GP])
                print("placar adv")
                print(score[GC])
                
                #Angulo absoluto da loba em relação ao robo
                if ball_angle < 0:
                    AnguloABS = 360 + ball_angle 
                else:
                    AnguloABS = ball_angle
                    
                if AnguloABS > 180:
                    AnguloABS = AnguloABS - 360
                #converção da orientação de radiandos para graus 
                
                AnguloABS = AnguloABS * lado
                    
                AnguloRobot = math.degrees(robot_pos['orientation'])
               # AnguloRobot = (AnguloRobot * 180/3.141592) 
                OFENSIVO = False
                if counter > 2800 or score[GP] - score[GC] < 0:
                    if score[GP] - score[GC] < 2:
                        #muda a estratégia 
                        OFENSIVO = True
                        print("Ofensivo")
                    else:
                        #muda a estratégia 
                        OFENSIVO = False
                        print("Defensivo")
                left_speed = 0
                right_speed = 0


                print (AnguloABS)
                if ball_pos['x'] * lado > 0.5:
                    #print(AnguloABS)  
                  if (robot_pos['y']*lado < 0.2 and robot_pos['y']*lado > -0.2) or DistBall > 0.4:
                    if robot_pos['y']> ball_pos['y']:
                        print("fecha a bola tras")
                        
                        if AnguloABS > 0:
                            G1 = (AnguloABS - 180)/10
                        else:
                            G1 = (AnguloABS + 180)/10
                        left_speed = 10 - G1 * lado
                        right_speed = 10 + G1 * lado
                        
                    else:
                        print("fecha a bola frente")
                        G1 = (AnguloABS)/10
                
                        left_speed = -10 - G1 * lado
                        right_speed = -10 + G1 * lado
                  else:
                        if ball_pos['y'] > 0:
                            print("fecha a bola esquerda")
                            alvo = -90 * lado
                
                            left_speed  = 10 - (AnguloRobot-alvo)/2 
                            right_speed = 10 + (AnguloRobot-alvo)/2   
                         
                        else:     
                            print("fecha a bola direita")
                            alvo = -90 * lado
                
                            left_speed  = 10 - (AnguloRobot-alvo)/2 
                            right_speed = 10 + (AnguloRobot-alvo)/2  
                                    
                elif (robot_pos ['x'] * lado > 0.48 and robot_pos ['x'] * lado < 0.55) or DistBall < 0.15:
                        print("fecha o angulo")
                        #print(DistBall)
                        FechaBola = 0
                           
                        if ball_pos['x'] * lado < 0 and robot_pos['y'] > 0.3: 
                                  AnguloABS = 100 
                                  print(AnguloABS)
                                   
                                    
                        if ball_pos['x'] * lado < 0 and robot_pos['y'] < -0.3: 
                                  AnguloABS = 80 
                                  print(AnguloABS)  
                                   
                        
                        
                        if (AnguloABS >= 85 and AnguloABS <= 95):
                           if dir == 0:
                               left_speed  = -5 
                               right_speed = -5 
                           else:
                               left_speed  = 5 
                               right_speed = 5 
                        else:
                        
                      
                            if AnguloABS > 90:
                              print("tras")  
                              left_speed  =  10 - AnguloRobot/2 
                              right_speed =  10 + AnguloRobot/2
                              
                            else:
                              print("frente")
                              left_speed  =  -10 - AnguloRobot/2 
                              right_speed =  -10 + AnguloRobot/2
                                 
                else:
                    print("Vai para a posição")
                    
                    if robot_pos['x'] * lado > 0.55:
                        dir = -1 
                    else:
                        dir = 1 
                    
                    if robot_pos ['y'] * lado < 0.05 and robot_pos ['y'] * lado > -0.05:
                         alvo = -90 * lado
                
                         left_speed  = dir * 10 - (AnguloRobot-alvo)/2 
                         right_speed = dir * 10 + (AnguloRobot-alvo)/2                       
                              
                    elif robot_pos ['y'] > 0:
                                          
                       alvo = -50 * lado
                
                       left_speed  = dir * 10 - (AnguloRobot-alvo)/2 
                       right_speed = dir * 10 + (AnguloRobot-alvo)/2  
                                                
                    else:
                    
                       alvo = -140 * lado
                
                       left_speed  = dir * 10 - (AnguloRobot-alvo)/2 
                       right_speed = dir * 10 + (AnguloRobot-alvo)/2  
          
    
                # posiciona em -0,9 e -1,1
                # Set the speed to motors
                if left_speed > 10:
                    left_speed = 10
                    
                if left_speed < -10:
                    left_speed = -10
                        
                if right_speed > 10:
                    right_speed = 10
                        
                if right_speed < -10:
                    right_speed = -10
                    
                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)
                

Goleiro = Goleiro()
Goleiro.PosDef(counter, score, goal_time, GOAL_FLAG, TIME_FLAG, IMPORT_FLAG, KICK_FLAG, CONTANDO_FLAG, BALL_AREA, INICIO)