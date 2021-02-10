import math
from typing import Tuple


# Proportional Factor to reach the ball faster
P_FACTOR = 40;
OP_GOAL = [-0.856, 0] # Opponent's goal position [x, y] (for Blue team)
OWN_GOAL = [0.856, 0] # Own's goal position [x, y] (for Blue team)
MINIMUM_SPEED = 6
AMP_CURVE = 10
OP_GOAL_ANGLE = 270
OP_GOAL_ANGLE_Y = 90

    
def game_time(counter) -> Tuple[int, int]:
    counter += 1
    cross_rule = 10 * counter/9373
    min = math.floor(cross_rule) # tempo em segundos
    seg = math.floor((cross_rule - min) * 60)
    game_clock = [9 - min, 59 - seg]
    return game_clock, counter


def countGoal(ball_pos, score, GOAL_FLAG) -> Tuple[int, bool]:
# vector[1] = blue team score; vector[0] = yellow team score
    gol_b = score[0]
    gol_y = score[1]
    if ball_pos > 0.743:
        gol_b += 1
        GOAL_FLAG = True
    elif ball_pos < -0.743:
        gol_y += 1
        GOAL_FLAG = True
        
    return [gol_b, gol_y], GOAL_FLAG


def scoreboard(data, SCORE, game_clock, goal_time, GOAL_FLAG, TIME_FLAG) -> Tuple[int, int, bool, bool]:
    clock_sec = game_clock[0] * 60 + game_clock[1]
    if GOAL_FLAG == False:
        SCORE, GOAL_FLAG = countGoal(data['ball']['x'], SCORE, GOAL_FLAG)
    else:
        if not TIME_FLAG:
            goal_time = clock_sec
            TIME_FLAG = True
            
        if clock_sec < goal_time - 4: #se passaram-se 4 segundos após o gol
            GOAL_FLAG = False
            TIME_FLAG = False
            print(SCORE)
            
    return SCORE, goal_time, GOAL_FLAG, TIME_FLAG

