import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
sys.path.append('/app/controllers')


#---------------------------------TATU F.C. ROBOT 1----------------------------------------
import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))

from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP

from team_027_libraries.robot1 import tatu_fc
import math

LADO_CAMPO = True
CONTANDO_FLAG = False
GOAL_FLAG = False
TIME_FLAG = False
IMPORT_FLAG = False
BALL_AREA = [0, 0, 0, 0]
ataque = [0,0]
GOL_ADVERSARIO = [-0.856, 0]
MEU_GOL = [0.856, 0]
score = [0, 0]
GOAL_DEFAULT_DIST = 0.4
INICIO = 0
contador = 0
N_ROBOT = 0
modo_jogo = 0
goal_time = 0
KICK_FLAG = 0
TEAM = 0
KICK_INTENSITY_DEFAULT = 5
GOLS_DEFENSIVA = 3
GOLS_OFENSIVA = 2

class MyRobot(RCJSoccerRobot):
    def run(self, contador, score, goal_time, GOAL_FLAG, TIME_FLAG, IMPORT_FLAG, KICK_FLAG, CONTANDO_FLAG, BALL_AREA, INICIO, GOLS_DEFENSIVA, GOLS_OFENSIVA):     
        while self.robot.step(TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()

                ball_pos = data['ball']
                robot_pos = data[self.name]

                if self.name[0] =='Y':
                    lado = -1
                    TEAM = ["Y1", "Y2", "Y3"]
                else:
                    lado = 1
                    TEAM = ["B1", "B2", "B3"]

                DistBall = math.sqrt(((robot_pos['x']*lado)-(ball_pos['x']*lado))**2 + ((robot_pos['y']*lado)-(ball_pos['y']*lado))**2)

                vector, min_valor = tatu_fc.perto_bola(self, data)
                goal = tatu_fc.perto_gol(self, data)

                R1 = vector[0]
                R2 = vector[1]
                R3 = vector[2]

                if R1 == min_valor:

                    ataque[0] = 0

                    if R2 - min_valor < R3 - min_valor:

                        ataque[1] = 1

                    else:

                        ataque[1] = 2

                elif R2 == min_valor:
                    ataque[0] =1

                    if R1 - min_valor < R3 - min_valor:

                        ataque[1] = 0

                    else:

                        ataque[1] = 2

                else: 

                    ataque[0] =2

                    if R2 - min_valor < R1 - min_valor:

                        ataque[1] = 1

                    else:

                        ataque[1] = 0

                

                if ataque[0] == goal and ataque[1] == N_ROBOT:

                    segundo = True

                    #print('B1')
                else:
                    segundo = False   


                tempo_jogo, contador = tatu_fc.relogio (contador) 
                #score, GOAL_FLAG = tatu_fc.conta_gol (ball_pos['x'], score, GOAL_FLAG)
                score, goal_time, GOAL_FLAG, TIME_FLAG = tatu_fc.placar (data, score, tempo_jogo, goal_time, GOAL_FLAG, TIME_FLAG)
                #print(tatu_fc.placar (data, score, tempo_jogo, goal_time, GOAL_FLAG, TIME_FLAG)) 
                TRUNCAMENTO_FLAG, CONTANDO_FLAG, BALL_AREA, INICIO = tatu_fc.bola_travada(data, tempo_jogo, CONTANDO_FLAG, BALL_AREA, INICIO)


                if lado < 0:

                    if score[1]-score[0] >=GOLS_OFENSIVA:
                        modo_jogo = "ofensiva"
                        GOLS_OFENSIVA = 0
                    elif score[0]-score[1] >=GOLS_DEFENSIVA:
                        modo_jogo = 'defensiva'
                    else:
                        modo_jogo = 'normal'
                        GOLS_OFENSIVA = 2
                else:

                    if score[0]-score[1] >=GOLS_OFENSIVA:
                        modo_jogo = "ofensiva"
                        GOLS_OFENSIVA = 0
                    elif score[1]-score[0] >=GOLS_DEFENSIVA:
                        modo_jogo = 'defensiva'
                    else:
                        modo_jogo = 'normal'
                        GOLS_OFENSIVA = 2

                print(modo_jogo)
                print(score)

                if modo_jogo == 'normal':

                    if goal == N_ROBOT:

                        if ball_pos ["x"] * lado > -0.2:

                            #tatu_fc.goleiro_reta(self, data, 0.55, 0.5)
                            
                            if ball_pos ["x"] * lado > 0.6 and (robot_pos['y']* lado  > 0.05 or robot_pos['y']* lado  <-0.05):

                                tatu_fc.atacante(self, data, True, KICK_FLAG, 10)
                            else:

                                tatu_fc.goleiro_arco(self, data, 0.35)

                        else:

                            tatu_fc.goleiro_reta(self, data, 0.5, 0.05)
                            #tatu_fc.goleiro_arco(self, data, 0.3)
                            #tatu_fc.espera_bola(self, data, [0.5, 0.0],'f', 0.0)
                            
                    elif ataque[0] == N_ROBOT or segundo:

                        if ball_pos ["x"] * lado > 0.5 or robot_pos['x']*lado > 0.35:

                            tatu_fc.espera_bola(self, data, [0.1, 0.0],'f', 0.0)


                        else:
                            #tatu_fc.goleiro_reta(self, data, 0.35 , 0.0)

                            if ball_pos['x']* lado  < -0.5 and (ball_pos['y']* lado  > 0.2 or ball_pos['y']* lado  <-0.2):

                                #tatu_fc.espera_bola(self, data, [0.243, 0.0])

                                #tatu_fc.espera_bola(self, data,[ball_pos ["x"] + 0.4 * lado, 0,0], 'f')
                                if ball_pos ["y"]* lado < 0:

                                    if robot_pos['x']* lado  > -0.7 or DistBall < 0.1:

                                        tatu_fc.espera_bola(self, data,[(ball_pos ["x"]* lado )+0.1, 0.2],'angle', 0)
                                    else:
                                        tatu_fc.atacante(self, data, True, KICK_FLAG, 10)

                                elif ball_pos ["y"] * lado> 0:

                                    if robot_pos['x'] * lado > -0.7 or DistBall < 0.1:
                                        
                                        tatu_fc.espera_bola(self, data,[(ball_pos ["x"] * lado)+ 0.1 , -0.2],'angle', 1)

                                    else:
                                        tatu_fc.atacante(self, data, True, KICK_FLAG, 10)
                            else:

                                tatu_fc.atacante(self, data, True, KICK_FLAG, 10)

                    else:

                        if ball_pos ["x"]* lado > -0.3:

                            if ball_pos ["y"]* lado  < 0:

                                if robot_pos['x']* lado  > -0.7 or DistBall < 0.1:
                                    if  ball_pos ["x"]* lado < -0.0:
                                        tatu_fc.espera_bola(self, data, [ -0.68, 0.2],'angle', 0)
                                    else:
                                        tatu_fc.espera_bola(self, data, [ -0.55, 0.2],'f', 0)

                                else:
                                    tatu_fc.atacante(self, data, True, KICK_FLAG, 10)

                            elif ball_pos ["y"]* lado > 0:

                                if robot_pos['x'] * lado > -0.7 or DistBall < 0.1:
                                    
                                    if  ball_pos ["x"]* lado < -0.0:
                                        tatu_fc.espera_bola(self, data, [ -0.68, -0.2],'angle', 0)
                                    else:
                                        tatu_fc.espera_bola(self, data, [ -0.55, -0.2],'f', 0)
                                else:
                                    tatu_fc.atacante(self, data, True, KICK_FLAG, 10)

                        else:

                            if ball_pos ["y"]* lado < -0.3:

                                if robot_pos['x']* lado  > -0.7 or DistBall < 0.1:

                                    tatu_fc.espera_bola(self, data,[(ball_pos ["x"] * lado) -0.05, 0.2],'angle', 0)
                                else:
                                    tatu_fc.atacante(self, data, True, KICK_FLAG, 10)

                            elif ball_pos ["y"]* lado > 0:

                                if robot_pos['x'] * lado > -0.7 or DistBall < 0.1:
                                    
                                    tatu_fc.espera_bola(self, data,[(ball_pos ["x"] * lado) -0.05, -0.2],'angle', 1)

                                else:
                                    tatu_fc.atacante(self, data, True, KICK_FLAG, 10)

                elif modo_jogo == 'defensiva':

                    if data[TEAM[2]]['x']*lado > 0.6 and data[TEAM[1]]['x']*lado  > 0.6:

                        if TRUNCAMENTO_FLAG:

                            if ataque[0] == N_ROBOT:

                                if ball_pos['x']*lado > -0.2:

                                    tatu_fc.atacante(self, data, True, KICK_FLAG, 10)
                                else: 
                                    tatu_fc.espera_bola(self, data, [0.2, 0.0],'f', 0.0)

                        elif ball_pos['x'] * lado < 0.55:
                            
                            tatu_fc.espera_bola(self, data, [0.55, 0.0],'f', 0.0)

                        else:
                            
                            tatu_fc.atacante(self, data, True, KICK_FLAG, 10)


                    else:

                        tatu_fc.goleiro_reta(self, data, 0.75, 1)

                elif modo_jogo == "ofensiva":

                    if ball_pos ["x"] * lado > -0.2:

                            #tatu_fc.goleiro_reta(self, data, 0.55, 0.5)
                            
                            if ball_pos ["x"] * lado > 0.6 and (robot_pos['y']* lado  > 0.05 or robot_pos['y']* lado  <-0.05):

                                tatu_fc.atacante(self, data, True, KICK_FLAG, 10)
                            else:

                                tatu_fc.goleiro_arco(self, data, 0.35)

                    else:

                        tatu_fc.goleiro_reta(self, data, 0.5, 0.05)
                        #tatu_fc.goleiro_arco(self, data, 0.3)
                        #tatu_fc.espera_bola(self, data, [0.5, 0.0],'f', 0.0)
                           

                # ********************************************************************

my_robot = MyRobot()
my_robot.run(contador, score, goal_time, GOAL_FLAG, TIME_FLAG, IMPORT_FLAG, KICK_FLAG, CONTANDO_FLAG, BALL_AREA, INICIO, GOLS_DEFENSIVA, GOLS_OFENSIVA)
