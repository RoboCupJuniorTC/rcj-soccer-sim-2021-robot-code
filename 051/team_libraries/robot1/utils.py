import math

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

def angle_filter(angle):

    if angle > 180:
        angle -= 360

    return angle

def get_distance(pointA, pointB):

    return math.sqrt(math.pow(pointA['x'] - pointB['x'], 2) + math.pow(pointA['y'] - pointB['y'], 2))

def get_sign(number):

    if number < 0:
        return -1

    return 1
