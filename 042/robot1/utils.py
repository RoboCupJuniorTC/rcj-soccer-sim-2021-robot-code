import math
from typing import Tuple

def get_direction(ball_angle: float) -> int:
    if ball_angle >= 345 or ball_angle <= 15:
        return 0
    return -1 if ball_angle < 180 else 1

def map_pwr(pwr:float or bool) -> float:
    if pwr > 10:
        pwr = 10
    if pwr <= -10:
        pwr = -10
    return pwr

def sign(value:float) -> int:
    if value == 0:
        return 1
    return abs(value) / value

def Team_dis(data:dict, name:str) -> dict:
    team_data = {}
    # bx, by = 0.0
    for i in data:
        if i[0] == name[0]:
            team_data[i] = {
                'x': data[i]['x'],
                'y': data[i]['y']
            }
        if i == 'ball':
            bx = data[i]['x']
            by = data[i]['y']
    Min_bot = {"Min":{"name":"", 'dis':999}, "Max":{"name":"", 'dis':0}}
    for i in [ name[0]+str(1), name[0]+str(2), name[0]+str(3)]:
        x = team_data[i]['x']
        y = team_data[i]['y']
        dis = math.sqrt((x-bx)**2 + (y-by)**2)
        if Min_bot['Min']['dis'] > dis:
            Min_bot['Min']['name'] = i
            Min_bot['Min']['dis'] = dis
        if Min_bot['Max']['dis'] < dis:
            Min_bot['Max']['name'] = i
            Min_bot['Max']['dis'] = dis
    return Min_bot


def ploy(team:str, role:str, ori:int, position:dict, ball:dict) -> Tuple[float, float]:
    left_speed = right_speed = 0.0
    angle = int(math.degrees(position['bot']['orientation']))
    line_pos = 0.55
    way = -1
    if team == "B":
        way = 1

    if role == "Attack":
        if (position['ball']['x'] > position['bot']['x'] - (0.075 / 2) and team == "B") or (position['ball']['x'] < position['bot']['x'] + (0.075 / 2) and team == "Y"):
            left_speed = right_speed = 10
            dy = position["ball"]["y"] - position["bot"]["y"]
            if abs(dy) > 0.5:
                theta = -45 * sign(dy) * way
            elif abs(dy) > 0.25:
                theta = -22.5 * sign(dy) * way
            elif abs(dy) < 0.075 / 2:
                return 8, -10
            else:
                theta = 0
            left_speed  += math.sin(math.radians(abs(angle) - 90 - theta)) * 20 * way
            right_speed -= math.sin(math.radians(abs(angle) - 90 - theta)) * 20 * way
        elif (int(angle) <= 0 and team=="B") or (int(angle) >= 0 and team=="Y"):      #face goal
            left_speed = right_speed = -10
            ratio = 5
            theta = 0
            if ball['angle'] < 12.5 or ball['angle'] > 360 - 12.5:   #345 ~ 15
                ratio = 10
            elif ball['angle'] < 60:                        # 15 ~ 60
                right_speed += 5 * abs(math.sin(math.radians(ball['angle'])))
            elif ball['angle'] > 300:                       #345 ~ 300
                left_speed  += 5 * abs(math.sin(math.radians(ball['angle'])))
            else:
                left_speed = right_speed = 10
                dy = position["ball"]["y"] - position["bot"]["y"]
                if abs(dy) > 0.5:
                    theta = -45 * sign(dy) * way
                elif abs(dy) > 0.25:
                    theta = -22.5 * sign(dy) * way
            #face front
            if ratio == 10:
                dx = (-5*math.cos(math.radians(abs(angle) - 90)) + 5) * way
                dy = ( 5*math.sin(math.radians(abs(angle) - 90)) - 0) * way
                theta = math.degrees(math.atan2(dy , dx))
                if abs(theta) < 5:
                    theta = 0
                elif theta > 0:
                    theta =  90 - theta
                else:
                    theta = -90 - theta
            left_speed  += math.sin(math.radians(abs(angle) - (90 + theta))) * ratio * way
            right_speed -= math.sin(math.radians(abs(angle) - (90 + theta))) * ratio * way
        else: # fixed to goal
            if (angle > -90 and angle < 90 and team == "B") or ((angle > -90 or angle < 90) and team == "Y"):
                clockwise = -1
            else:
                clockwise = 1
            left_speed  =  10 * clockwise
            right_speed = -10 * clockwise

    elif role == "Defense":
        if (position['bot']['x'] + line_pos * int(ori) < 0 and team == "B") or (position['bot']['x'] + line_pos * int(ori) > 0 and team == "Y"): #回場防守的方向修正要修
            if (position['bot']['x'] * int(ori) > 0 and team == "B") or (position['bot']['x'] * int(ori) < 0 and team == "Y"):
                ratio = 2
            else:
                ratio = 20
            left_speed  = 10 + math.sin(math.radians(abs(angle) - 90)) * ratio * way
            right_speed = 10 - math.sin(math.radians(abs(angle) - 90)) * ratio * way
        elif abs(angle) > 10:
            if angle < 0:
                clockwise = 1
            else:
                clockwise = -1
            left_speed  =  10 * clockwise
            right_speed = -10 * clockwise 
        else:
            ratio = 8
            dy = (position['ball']['y'] - position['bot']['y'])
            if (position['ball']['x'] > position['bot']['x'] and team == "B") or (position['ball']['x'] < position['bot']['x'] and team == "B"):
                offset = 0.075 * sign(dy)
            else:
                offset = 0
            dy += offset
            if int(ori) * position['ball']['x'] > 0:
                left_speed = right_speed = -10 * dy * 10 + sign(dy) * (-10)
            else:
                left_speed = right_speed = -10 * dy * 100
            left_speed  -= math.sin(math.radians(angle)) * ratio * way
            right_speed += math.sin(math.radians(angle)) * ratio * way
    else:#游擊
        if (position['ball']['x'] > position['bot']['x'] + (0.075 / 2) and team == "B") or (position['ball']['x'] < position['bot']['x'] + (0.075 / 2) and team == "Y"):
            left_speed = right_speed = 10
            dy = position["ball"]["y"] - position["bot"]["y"]
            if abs(dy) > 0.5:
                theta = -45 * sign(dy) * way
            elif abs(dy) > 0.25:
                theta = -22.5 * sign(dy) * way
            elif abs(dy) < 0.075 / 2:
                return 8, 10 
            else:
                theta = 0
            left_speed  += math.sin(math.radians(abs(angle) - 90 - theta)) * 20 * way
            right_speed -= math.sin(math.radians(abs(angle) - 90 - theta)) * 20 * way
        elif (int(angle) <= 0 and team=="B") or (int(angle) >= 0  and team=="Y"):
            if (position['ball']['x'] < 0.4 and team == "B") or (position['ball']['x'] > 0.4 and team == "Y"):
                left_speed  =  10 * get_direction(ball['angle'])
                right_speed = -10 * get_direction(ball['angle'])
                if left_speed == 0:
                    left_speed = right_speed = -10
                    if (position['bot']['x'] < 0.2 and team == "B") or (position['bot']['x'] > -0.2 and team == "Y"):
                        left_speed = right_speed = 10
                    left_speed  += math.sin(math.radians(abs(angle) - 90)) * 20 * way
                    right_speed -= math.sin(math.radians(abs(angle) - 90)) * 20 * way
            else:
                left_speed  =  10 * get_direction(ball['angle'])
                right_speed = -10 * get_direction(ball['angle'])
                if left_speed == 0:
                    left_speed = right_speed = -10
        else:
            if angle > -90 and angle < 90:
                clockwise = -1
            else:
                clockwise = 1
            left_speed  =  10 * clockwise * way
            right_speed = -10 * clockwise * way
    left_speed  = map_pwr(left_speed)
    right_speed = map_pwr(right_speed)
    return left_speed, right_speed

