import math
import struct
from typing import Tuple
from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP
from controller import Robot

dist1 = 1
dist2 = 1
dist3 = 1

dist1b = 1

def get_near():
    def run(B1):
        while B1.robot.step(TIME_STEP) != -1:
            if B1.is_new_data():
                data = B1.get_new_data()
                print('contenido data', data)
    return
    
def get_direction(ball_angle: float) -> int:
    if ball_angle >= 345 or ball_angle <=15:
        return 0
    return -1 if ball_angle < 180 else 1
        
def get_dist1(ball_pos1: dict, robot_pos1: dict) -> Tuple[float, float]:
    global dist1
    dist1 =  math.sqrt((ball_pos1['y'] - robot_pos1['y'])*(ball_pos1['y'] - robot_pos1['y'])+(ball_pos1['x'] - robot_pos1['x'])*(ball_pos1['x'] - robot_pos1['x']))
    return dist1
        
def get_dist2(ball_pos2: dict, robot_pos2: dict) -> Tuple[float, float]:
    global dist2
    dist2 =  math.sqrt((ball_pos2['y'] - robot_pos2['y'])*(ball_pos2['y'] - robot_pos2['y'])+(ball_pos2['x'] - robot_pos2['x'])*(ball_pos2['x'] - robot_pos2['x']))
    return dist2

def get_dist3(ball_pos3: dict, robot_pos3: dict) -> Tuple[float, float]:
    global dist3
    dist3 =  math.sqrt((ball_pos3['y'] - robot_pos3['y'])*(ball_pos3['y'] - robot_pos3['y'])+(ball_pos3['x'] - robot_pos3['x'])*(ball_pos3['x'] - robot_pos3['x']))
    return dist3
   
def update_dist1(dist1):
    global dist1b
    dist1b=dist1
    return

def get_nearball():
    print('Buscando pelota', dist1, dist1b, dist3)
    if dist1<dist2 and dist1<dist3:
        return 1
    elif dist2<dist1 and dist2<dist3:
        return 2
    elif dist3<dist1 and dist3<dist2:          
        return 3
    else:
        return 0
