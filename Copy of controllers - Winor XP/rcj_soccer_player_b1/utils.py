import math
from typing import Tuple

def get_direction(ball_angle: float) -> int:
    """Get direction to navigate robot to face the ball

    Args:
        ball_angle (float): Angle between the ball and the robot

    Returns:
        int: 0 = forward, -1 = right, 1 = left
    """
    if ball_angle >= 345 or ball_angle <= 15:
        return 0
    return -1 if ball_angle < 180 else 1

def p_regler(ball_pos: dict, robot_pos: dict, verschiebungX: float, verschiebungY: float) -> Tuple[float, int]:
    if ((robot_pos['x'] - ball_pos['x']) - verschiebungX) != 0:
        direction_new =  -1 * math.atan((robot_pos['y'] - ball_pos['y'] - verschiebungY)/((robot_pos['x'] - ball_pos['x']) - verschiebungX))
    else:
        direction_new = 0
    
    if (robot_pos['x'] - ball_pos['x'] - verschiebungX) > 0:
        direction_new -= math.pi / 2
    else:
        direction_new += math.pi / 2

    orientation_robot = robot_pos['orientation']
    pRegler_one = direction_new - orientation_robot

    if direction_new > 0:
        direction_new -= math.pi
    else:
        direction_new += math.pi

    if orientation_robot > 0:
        orientation_robot -= math.pi
    else:
        orientation_robot += math.pi

    pRegler_two = direction_new - orientation_robot

    if abs(pRegler_one) < abs(pRegler_two):
        pRegler = pRegler_one
    else:
        pRegler = pRegler_two


    orientation_robot += math.pi
    if orientation_robot > math.pi:
        orientation_robot - (2*math.pi)

    pRegler_one_backwards = direction_new - orientation_robot

    if direction_new > 0:
        direction_new -= math.pi
    else:
        direction_new += math.pi

    if orientation_robot > 0:
        orientation_robot -= math.pi
    else:
        orientation_robot += math.pi

    pRegler_two_backwards = direction_new - orientation_robot

    if abs(pRegler_one_backwards) < abs(pRegler_two_backwards):
        pRegler_backwards = pRegler_one_backwards
    else:
        pRegler_backwards = pRegler_two_backwards
    
    print(pRegler)
    print(pRegler_backwards)
    if abs(pRegler) < abs(pRegler_backwards):
        return pRegler, 1
    else:
        return pRegler_backwards, -1
    

def p_regler_drive(pRegler: float, faktor: int, direction: int) -> Tuple[float, float]:
    pRegler *= faktor * direction

    if pRegler > 20:
        pRegler = 20
    if pRegler < -20:
        pRegler = -20

    if pRegler > 0:
        left_speed = (-10 + round(pRegler)) * direction
        right_speed = -10 * direction
    else:
        left_speed = -10 * direction
        right_speed = (-10 - round(pRegler)) * direction

    return left_speed, right_speed