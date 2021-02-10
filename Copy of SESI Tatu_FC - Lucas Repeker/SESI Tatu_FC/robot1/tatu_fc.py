#------------------------------------------ SESI TATU F.C. --------------------------------------------------
import math
from typing import Tuple


P_FACTOR = 40
VEL_MIN = 6
AMP_CURVA = 10
GOL_ADVERSARIO = [-0.856, 0]
MEU_GOL = [0.856, 0]
GOL_ADVERSARIO_ANGLE = 270
GOL_ADVERSARIO_ANGLE_Y = 90

#------------------------------------------ RELOGIO --------------------------------------------------
def relogio(contador) -> Tuple[int, int]:
    contador += 1
    cross_rule = 10 * contador/9373
    min = math.floor(cross_rule)
    seg = math.floor((cross_rule - min) * 60)
    tempo_jogo = [9 - min, 59 - seg]
    return tempo_jogo, contador

#------------------------------------------ CONTA_GOL --------------------------------------------------
def conta_gol(ball_pos, score, GOAL_FLAG) -> Tuple[int, bool]:

    gol_b = score[0]
    gol_y = score[1]
    if ball_pos> 0.743:
        gol_b += 1
        GOAL_FLAG = True
    elif ball_pos < -0.743:
        gol_y += 1
        GOAL_FLAG = True
        
    return [gol_b, gol_y], GOAL_FLAG

#------------------------------------------ PLACAR --------------------------------------------------
def placar(data, SCORE, tempo_jogo, goal_time, GOAL_FLAG, TIME_FLAG) -> Tuple[int, int, bool, bool]:
    clock_sec = tempo_jogo[0] * 60 + tempo_jogo[1]
    if GOAL_FLAG == False:
        SCORE, GOAL_FLAG = conta_gol(data['ball']['x'], SCORE, GOAL_FLAG)
    else:
        if not TIME_FLAG:
            goal_time = clock_sec
            TIME_FLAG = True
            
        if clock_sec < goal_time - 4: 
            GOAL_FLAG = False
            TIME_FLAG = False
            print(SCORE)
            
    return SCORE, goal_time, GOAL_FLAG, TIME_FLAG

#------------------------------------------ PONTO_GOL_BOLA --------------------------------------------------
def ponto_gol_bola(data, my_goal_point, radius, lado) -> Tuple[float, float]:
   
    
    ball_pos = data['ball']
    m = math.atan((ball_pos['y'] - my_goal_point[1])/(ball_pos['x'] - my_goal_point[0]))
    if lado == 1:
        ax = my_goal_point[0] - radius * math.cos(m)
        ay = my_goal_point[1] - radius * math.sin(m)
    else:
        ax = my_goal_point[0] + radius * math.cos(m)
        ay = my_goal_point[1] + radius * math.sin(m)
   
    return [ax, ay], math.degrees(m)

#------------------------------------------ get_direction --------------------------------------------------
def get_direction(ball_angle: float) -> int:

    if ball_angle >= 345 or ball_angle <= 15:
        return 0
    return -1 if ball_angle < 180 else 1

#------------------------------------------ DISTANCIA_OBJETOS --------------------------------------------------
def distancia_objetos(object_1, object_2) -> float:
    return math.sqrt((object_1['x'] - object_2['x'])**2 + (object_1['y'] - object_2['y'])**2)  

#------------------------------------------ DISTANCIA_OBJETO_PONTO --------------------------------------------------
def distancia_objeto_ponto(object_1, point_vector) -> float:
    return math.sqrt((object_1['x'] - point_vector[0])**2 + (object_1['y'] - point_vector[1])**2)  

#------------------------------------------ DIRECAO_PONTO --------------------------------------------------
def direcao_ponto(robot_pos, robot_angle, point) -> int:

        angle = math.atan2(
            point[1] - robot_pos['y'],
            point[0] - robot_pos['x'],
        )

        if angle < 0:
            angle = 2 * math.pi + angle

        if robot_angle < 0:
            robot_angle = 2 * math.pi + robot_angle

        robot_point_angle = math.degrees(angle + robot_angle)

        robot_point_angle -= 90
        if robot_point_angle > 360:
            robot_point_angle -= 360
        
        direction = get_direction(robot_point_angle) * -1 

        return direction
        
#------------------------------------------ ANGULO_GOL --------------------------------------------------            
def angulo_gol(robot_pos, robot_angle, goal_point, MEU_GOL_point, side) -> Tuple[int, float, float]:

    robot_angle = math.degrees(robot_angle)  
    phi = math.atan(abs((goal_point[0] - robot_pos['x'])/robot_pos['y']))
    own_phi = math.atan(abs((MEU_GOL_point[0] - robot_pos['x'])/robot_pos['y'])) 

    if robot_pos['y'] < 0:
        angle2goal = math.degrees(2 * math.pi - phi)
        angle2owngoal = math.degrees(own_phi)
    else:
        angle2goal = math.degrees(math.pi + phi)
        angle2owngoal = math.degrees(math.pi - own_phi)


    d_angle = angle2goal - robot_angle
    d_angle_own = angle2owngoal - robot_angle
    
    if (robot_angle > 180): 

        if abs(d_angle) < 10 and side == 1: 
            valor = 0
        else:
            if d_angle > 0:
        
                valor = -1
            else:

                valor = 1
    else: 
        if abs(d_angle_own) < 10 and side == -1:
            valor = 0
        else:
            if d_angle_own < 0:
                valor = -1
            else:
                valor = 1
         
    return valor * side, d_angle, d_angle_own

#------------------------------------------ PERTO_BOLA --------------------------------------------------    
def perto_bola(self, data) -> Tuple[bool, float]:
    if self.name[0] =='Y':
        MY_ROBOT_NAME = ["Y1", "Y2", "Y3"]
    else:
        MY_ROBOT_NAME = ["B1", "B2", "B3"]
    
    robot_name = self.name
    
    vector = [100, 100, 100]
    i = 0
    for name in MY_ROBOT_NAME:
        robot_pos = data[name]
        ball_pos = data['ball']
        vector[i] = distancia_objetos(robot_pos, ball_pos)
        i += 1  
    
    
    min_valor = min(vector)
    min_arg = -1
    for valor_i in range(3):
        if min_valor == vector[valor_i]:
            min_arg = valor_i
            break
 
    return vector, min_valor

#------------------------------------------ PERTO_GOL --------------------------------------------------        
def perto_gol(self, data) -> float:
    if self.name[0] =='Y':
        MY_ROBOT_NAME = ["Y1", "Y2", "Y3"]
        MEU_GOL = [-0.856, 0]
    else:
        MY_ROBOT_NAME = ["B1", "B2", "B3"]
        MEU_GOL = [0.856, 0]
        
    vector = [100, 100, 100]
    i = 0
    for name in MY_ROBOT_NAME:
        robot_pos = data[name]
        ball_pos = data['ball']
        vector[i] = distancia_objeto_ponto(robot_pos, MEU_GOL)
        i += 1
    
    min_valor = min(vector)
    min_arg = -1
    for valor_i in range(3):
        if min_valor == vector[valor_i]:
            min_arg = valor_i
            break
    
    return min_arg

#------------------------------------------ OLHA_FRENTE --------------------------------------------------
def olha_frente(self, data) -> bool:

    if self.name[0] =='Y':
        lado = -1
    else:
        lado = 1
        
    ball_angle, robot_angle = self.get_angles(data['ball'], data[self.name])
    robot_angle = math.degrees(robot_angle)
    FORWARD_FLAG = False
    ACEPTED_ERROR = 10
    if lado == 1:
        if robot_angle < (GOL_ADVERSARIO_ANGLE - ACEPTED_ERROR) and robot_angle > 90:
 
            left_speed = 6
            right_speed = -6
        elif robot_angle > (GOL_ADVERSARIO_ANGLE + ACEPTED_ERROR) or robot_angle < 90:
      
            left_speed = -6
            right_speed = 6
        else:
 
            FORWARD_FLAG = True
            left_speed = 3
            right_speed = 3
    else:
        if robot_angle > (GOL_ADVERSARIO_ANGLE_Y + ACEPTED_ERROR) and robot_angle < 270:

            left_speed = -6
            right_speed = 6
        elif robot_angle < (GOL_ADVERSARIO_ANGLE_Y - ACEPTED_ERROR) or robot_angle > 270:
   
            left_speed = 6
            right_speed = -6
        else:

            FORWARD_FLAG = True
            left_speed = 3
            right_speed = 3
            

    self.left_motor.setVelocity(left_speed)
    self.right_motor.setVelocity(right_speed)
    
    return FORWARD_FLAG

#------------------------------------------OLHA_ANGULO --------------------------------------------------
def olha_angulo(self, data, angle) -> bool:

    if self.name[0] =='Y':
        lado = -1
    else:
        lado = 1
        
    ball_angle, robot_angle = self.get_angles(data['ball'], data[self.name])
    robot_angle = math.degrees(robot_angle)
    FORWARD_FLAG = False
    ACEPTED_ERROR = 10
    if lado == 1:
        if angle ==1:
           
            left_speed = 8
            right_speed = -8
        else:
        
            left_speed = -8
            right_speed = 8
    else:
        if angle == 1:
            left_speed = -8
            right_speed = 8
        else:

            left_speed = 8
            right_speed = -8

    self.left_motor.setVelocity(left_speed)
    self.right_motor.setVelocity(right_speed)
    
    return FORWARD_FLAG

#------------------------------------------ OLHA_BOLA --------------------------------------------------
def olha_bola(self, data):


    robot_pos = data[self.name]

    ball_pos = data['ball']

    ball_angle, robot_angle = self.get_angles(ball_pos, robot_pos)

    direction = get_direction(ball_angle)

    if direction == 0:
        left_speed = 0
        right_speed = 0
    else:
        left_speed = direction * 5
        right_speed = direction * -5

    self.left_motor.setVelocity(left_speed)
    self.right_motor.setVelocity(right_speed)

#------------------------------------------ SEGUE_BOLA --------------------------------------------------
def segue_bola(self, data):

    
    robot_pos = data[self.name]

    ball_pos = data['ball']

    ball_angle, robot_angle = self.get_angles(ball_pos, robot_pos)
  
    direction = get_direction(ball_angle)
  
    if direction == 0:
        left_speed = -10
        right_speed = -10
    else:
        left_speed = direction * 5
        right_speed = direction * -5
   
    self.left_motor.setVelocity(left_speed)
    self.right_motor.setVelocity(right_speed)

#------------------------------------------ VAI_XY --------------------------------------------------
def vai_xy(self, data, point, lado):

    robot_pos = data[self.name]

    ball_pos = data['ball']


    if lado:
        if self.name[0] == 'Y':
            point[0] = - point[0]
            point[1] = - point[1]

            '''robot_pos['x'] = -robot_pos['x']
            robot_pos['y'] = -robot_pos['y']
            robot_pos['orientation'] = -robot_pos['orientation']

            ball_pos['x'] = -ball_pos['x']
            ball_pos['y'] = -ball_pos['y']'''

    ball_angle, robot_angle = self.get_angles(ball_pos, robot_pos)

    valor = direcao_ponto(robot_pos, robot_angle, point)

    dist_robot2point = distancia_objeto_ponto(robot_pos, point)
    
    if dist_robot2point < 0.05: 
        
        self.left_motor.setVelocity(0)
        self.right_motor.setVelocity(0)
        return True
    else:
        if valor == 0:
            self.left_motor.setVelocity(-10)
            self.right_motor.setVelocity(-10)
        elif valor == -1:
           
            self.left_motor.setVelocity(10)
            self.right_motor.setVelocity(-10)   
        else:
            self.left_motor.setVelocity(-10)
            self.right_motor.setVelocity(10)
        return False

#------------------------------------------ BOLA_TRAVADA --------------------------------------------------
def bola_travada(data, tempo_jogo, CONTANDO_FLAG, BALL_AREA, INICIO) -> Tuple[bool, bool, float, int]:
    
    TRUNCAMENTO_FLAG = False
    if not CONTANDO_FLAG:
        x_mais = abs(data['ball']['x']) + 0.08
        x_menos = abs(data['ball']['x']) - 0.08
        y_mais = abs(data['ball']['y']) + 0.08
        y_menos = abs(data['ball']['y']) - 0.08
        BALL_AREA = [x_mais, x_menos, y_mais, y_menos]
        CONTANDO_FLAG = True
        INICIO = tempo_jogo[0]*60 + tempo_jogo[1]
    else:
        if abs(data['ball']['x']) <= BALL_AREA[0] and abs(data['ball']['x']) >= BALL_AREA[1] and abs(data['ball']['y']) <= BALL_AREA[2] and abs(data['ball']['y']) >= BALL_AREA[3]:
            tempo_passou = INICIO - (tempo_jogo[0]*60 + tempo_jogo[1])
            if tempo_passou >= 2:
                TRUNCAMENTO_FLAG = True
        else:
            TRUNCAMENTO_FLAG = False
            CONTANDO_FLAG = False
    return TRUNCAMENTO_FLAG, CONTANDO_FLAG, BALL_AREA, INICIO

#------------------------------------------ ATACANTE --------------------------------------------------
def atacante(self, data, STOP_NEAR_GOALKEEPER, KICK_FLAG, kick_intensity) -> int:
    
    if self.name[0] =='Y':
        MY_ROBOT_NAMES = ["Y1", "Y2", "Y3"]
        GOL_ADVERSARIO = [0.856, 0]
        MEU_GOL = [-0.856, 0] 
        lado = -1
    else:
        MY_ROBOT_NAMES = ["B1", "B2", "B3"]
        GOL_ADVERSARIO = [-0.856, 0] 
        MEU_GOL = [0.856, 0] 
        lado = 1
    
    robot_pos = data[self.name]
    ball_pos = data['ball']

    ball_angle, robot_angle = self.get_angles(ball_pos, robot_pos)
    dist_ball2robot = distancia_objetos(ball_pos, robot_pos)          
    proportional_speed = -(VEL_MIN + P_FACTOR*dist_ball2robot)
    robot_angle_deg = math.degrees(robot_angle)
    direction = get_direction(ball_angle)
    dist2goleiro = distancia_objetos(robot_pos, data[MY_ROBOT_NAMES[0]]) 
    dist_ball2goleiro = distancia_objetos(data['ball'], data[MY_ROBOT_NAMES[0]])

    if dist2goleiro < 0.2 and dist_ball2goleiro < 0.1 and STOP_NEAR_GOALKEEPER:
        left_speed = -10
        right_speed = -10
        
    else:    
        
        CLOSE_BALL = False
        
        if dist_ball2robot <= 0.065:
            if lado == -1:
                kick_rotation, d_angle, d_angle_own = angulo_gol(robot_pos, robot_angle, MEU_GOL, GOL_ADVERSARIO, lado)
            else:             
                kick_rotation, d_angle, d_angle_own = angulo_gol(robot_pos, robot_angle, GOL_ADVERSARIO, MEU_GOL, lado)
            if KICK_FLAG == 0:  
                if kick_rotation == 0:
                    left_speed = -10
                    right_speed = -10
    
                elif kick_rotation == -1:
                    left_speed = 10
                    right_speed = -10
                    KICK_FLAG = -1
                else:           
                    left_speed = -10
                    right_speed = 10
                    KICK_FLAG = 1  
        else:           
            change_rotation = True if dist_ball2robot > 0.10 else False 
            if direction == 0:
                left_speed = proportional_speed if proportional_speed >= -10 else -10
                right_speed = left_speed    
            
            elif direction == -1:
                left_speed = -6 if change_rotation else -10
                right_speed = 6 if change_rotation else -3
        
            else:
                left_speed = 6 if change_rotation else -3
                right_speed = -6 if change_rotation else -10
    if KICK_FLAG < 0:
        left_speed = 0
        right_speed = -10
        KICK_FLAG -= 1
    elif KICK_FLAG > 0:
        left_speed = -10
        right_speed = 0
        KICK_FLAG += 1
    if KICK_FLAG == kick_intensity + 1 or KICK_FLAG == -kick_intensity - 1:
        KICK_FLAG = 0   

    self.left_motor.setVelocity(left_speed)
    self.right_motor.setVelocity(right_speed)
    
    return KICK_FLAG
   
#------------------------------------------ GOLEIRO_RETA --------------------------------------------------
def goleiro_reta(self, data, distancia_x, distancia_y):
    
    dir = 0
    DistBall = 0
    AnguloABS = 0
    AnguloRobot = 0     
    FechaBola = 0 
    lado = 0

    if self.name[0] =='Y':
        lado = -1
    else:
        lado = 1


    robot_pos = data[self.name]

    ball_pos = data['ball']


    ball_angle, robot_angle = self.get_angles(ball_pos, robot_pos)


    direction = get_direction(ball_angle)


    DistBall = math.sqrt((robot_pos['x']-ball_pos['x'])**2 + (robot_pos['y']-ball_pos['y'])**2)

    if ball_angle < 0:
        AnguloABS = 360 + ball_angle 
    else:
        AnguloABS = ball_angle
        
    if AnguloABS > 180:
        AnguloABS = AnguloABS - 360

    AnguloRobot = math.degrees(robot_pos['orientation'])

    if ball_pos['x']*lado> distancia_x:

        if robot_pos ['y'] > distancia_y:

                left_speed  = 8 - AnguloRobot/2 
                right_speed = 8 + AnguloRobot/2

        elif robot_pos ['y'] < -distancia_y:

                left_speed  = -8 - AnguloRobot/2
                right_speed = -8 + AnguloRobot/2

        elif robot_pos['y']> ball_pos['y']:
          
            if AnguloABS > 0:
                G1 = (AnguloABS - 180)/10
            else:
                G1 = (AnguloABS + 180)/10
            left_speed = 8 - G1
            right_speed = 8 + G1
            
        else:
            G1 = AnguloABS/10
            left_speed = -8 - G1
            right_speed = -8 + G1
            
    elif (robot_pos ['x'] * lado > (distancia_x - 0.02) and robot_pos ['x'] * lado < (distancia_x + 0.05)) or DistBall < 0.15:
            FechaBola = 0

            if robot_pos ['y']> distancia_y:

                left_speed  = 8 - AnguloRobot/2 
                right_speed = 8 + AnguloRobot/2

            elif robot_pos ['y']< -distancia_y:

                left_speed  = -8 - AnguloRobot/2
                right_speed = -8 + AnguloRobot/2

            elif (AnguloABS * lado >= 85 and AnguloABS * lado <= 95):
               if dir == 0:
                   left_speed  = -10
                   right_speed = -10
               else:
                   left_speed  = 10
                   right_speed = 10
            else:
                   if AnguloABS * lado > 90: 
                       left_speed  = 8 - AnguloRobot/2 
                       right_speed = 8 + AnguloRobot/2 
                       dir = 1
                   else:
                       left_speed  = -8 - AnguloRobot/2
                       right_speed = -8 + AnguloRobot/2   
                       dir = 0
            

    else:
        if robot_pos['x'] * lado > distancia_x+0.05:
            dir = -1
        else:
            dir = 1 
        if robot_pos ['y'] * lado < 0.05 and robot_pos ['y'] * lado > -0.05:
             alvo = -90 * lado
             left_speed  = dir * 8 - (AnguloRobot-alvo)/2 
             right_speed = dir * 8 + (AnguloRobot-alvo)/2                               
        elif robot_pos ['y'] > 0:                    
           alvo = -50 * lado
           left_speed  = dir * 8 - (AnguloRobot-alvo)/2 
           right_speed = dir * 8 + (AnguloRobot-alvo)/2                                   
        else:     
           alvo = -140 * lado 
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
        
    self.left_motor.setVelocity(left_speed)
    self.right_motor.setVelocity(right_speed)  

#------------------------------------------ GOLEIRO_ARCO --------------------------------------------------
def goleiro_arco(self, data, dist2mygoal):

    if self.name[0] =='Y':
        GOL_ADVERSARIO = [0.856, 0] 
        MEU_GOL = [-0.856, 0] 
        lado = -1
    else:
        GOL_ADVERSARIO = [-0.856, 0]
        MEU_GOL = [0.856, 0] 
        lado = 1
        
    desired_point, m = ponto_gol_bola(data, MEU_GOL, dist2mygoal, lado)
    
    point_reached = vai_xy(self, data, desired_point, False)

    if point_reached: 
        self.left_motor.setVelocity(5)
        self.right_motor.setVelocity(5)    

#------------------------------------------ ESPERA_BOLA --------------------------------------------------    
def espera_bola(self, data, point, look, angle):
    BANHEIRA_POINT_CENTER = point

    robot_pos = data[self.name]
 
    ball_pos = data['ball']

    if self.name[0] == 'Y':
        
        BANHEIRA_POINT_CENTER[0] = - point[0]
        BANHEIRA_POINT_CENTER[1] = - point[1]

        '''robot_pos['x'] = -robot_pos['x']
        robot_pos['y'] = -robot_pos['y']
        robot_pos['orientation'] = -robot_pos['orientation']

        ball_pos['x'] = -ball_pos['x']
        ball_pos['y'] = -ball_pos['y']'''

    ball_angle, robot_angle = self.get_angles(ball_pos, robot_pos)

    valor = direcao_ponto(robot_pos, robot_angle, BANHEIRA_POINT_CENTER)
    dist_robot2point = distancia_objeto_ponto(robot_pos, BANHEIRA_POINT_CENTER)
    
    if dist_robot2point < 0.05: 

        if look == "ball":
            is_forward = olha_bola(self, data)

        elif look == "angle":
            is_forward = olha_angulo(self, data, angle)
        else:
            is_forward = olha_frente(self, data)
    else:
        if valor == 0:
            self.left_motor.setVelocity(-10)
            self.right_motor.setVelocity(-10)
        elif valor == -1:
            # sentido anti-horario
            self.left_motor.setVelocity(2)
            self.right_motor.setVelocity(-2)   
        else: # valor == 1
            # sentido horário
            self.left_motor.setVelocity(-2)
            self.right_motor.setVelocity(2)
