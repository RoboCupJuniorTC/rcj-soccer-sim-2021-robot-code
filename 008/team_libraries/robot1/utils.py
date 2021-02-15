import math
from . import helveticmath


def get_direction(ball_angle: float) -> int:
    """Get direction to navigate robot to face the ball

    Args:
        ball_angle (float): Angle between the ball and the robot

    Returns:
        int: 0 = forward, -1 = right, 1 = left, 2 = backwards
    """

    if ball_angle >= 90 and ball_angle <= 270:
        if ball_angle >= 165 and ball_angle <= 195:
            return 2
        return -1 if ball_angle > 180 else 1
    else:
        if ball_angle >= 345 or ball_angle <= 15:
            return 0
        return -1 if ball_angle < 180 else 1


def get_nearest_position(current_pos, target_positions):
    target_position = None
    for tp in target_positions:
        if not target_position:
            target_position = tp
        else:
            if helveticmath.distance(current_pos, tp) < helveticmath.distance(current_pos, target_position):
                target_position = tp
    return target_position
