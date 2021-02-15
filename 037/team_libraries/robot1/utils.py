def get_direction(ball_angle: float) -> int:
    """Get direction to navigate robot to face the ball

    Args:
        ball_angle (float): Angle between the ball and the robot

    Returns:
        int: 0 = forward, -1 = right, 1 = left
    """
    if ball_angle >= 345 or ball_angle <= 15:
        return 0
    elif ball_angle >= 165 and ball_angle <= 195:
        return 2
    elif ball_angle <= 90:
        return -1
    elif ball_angle >= 180 and ball_angle <= 270:
        return -1
    else:
        return 1
    # return -1 if ball_angle < 180 else 1
