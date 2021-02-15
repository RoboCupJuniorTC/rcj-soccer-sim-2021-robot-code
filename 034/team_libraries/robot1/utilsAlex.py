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

def calculateAngle(goToPos, robot_pos):
    robot_angle: float = robot_pos['orientation']

    # Get the angle between the robot and the ball
    angle = math.atan2(
        goToPos[1] - robot_pos['y'],
        goToPos[0] - robot_pos['x'],
    )

    if angle < 0:
        angle = 2 * math.pi + angle

    if robot_angle < 0:
        robot_angle = 2 * math.pi + robot_angle

    robotGTPAngle = math.degrees(angle + robot_angle)

    # Axis Z is forward
    # TODO: change the robot's orientation so that X axis means forward
    robotGTPAngle -= 90
    if robotGTPAngle > 360:
        robotGTPAngle -= 360

    return robotGTPAngle
def calculateGBRLine(ball_pos):
    xCoor = ball_pos['x']
    yCoor = ball_pos['y']

    ballPos = [xCoor, yCoor]
    goalPos = [-0.75, 0]

    slopeY = ballPos[1] - goalPos[1]
    slopeX = ballPos[0] - goalPos[0]
    length = calculateVecLength(slopeX, slopeY)

    botPos = {'x':ballPos[0] + 0.1*(slopeX/length), 'y': ballPos[1] + 0.1*(slopeY/length)}
    return botPos

def calculateVecLength(x, y):
    length = math.sqrt(x**2 + y**2)
    return length
