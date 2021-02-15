import math

#Please subscribe to us!
#inst: @semicolon.robocup
#YouTube: https://www.youtube.com/channel/UC9m3bGAsJcVbLzjM8-gC-Kg

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



def get_vel_mult(ball_angle, robot_angle: float) -> int:
    if 10 - abs(robot_angle - ball_angle) > 0:
        return 10 - abs(robot_angle - ball_angle)
    return 3


def angle_converter(angle: float) -> float:
    while(angle > 180):
        angle-=360
    while(angle < -180):
        angle+=360
    return angle

def scalarMult(u, v: list) -> float:
  return u['x'] * v['x'] + u['y'] * v['y']

def cosSimMult(u, v: list) -> float:
  return u['x'] * v['y'] - u['y'] * v['x']

def norm(x, y: list) -> float:
  a = math.sqrt(x * x + y * y)
  return a
    
#u = [cos(agent.ang), sin(agent.ang)]
#v = [target(1)-agent.x,  target(2)-agent.y]
#angle = atan2( cosSimMult( u, v ), scalarMult(u, v ) )

def getAngleToPoint(ball_pos: dict, robot_pos: dict) -> float:
        robot_angle: float = robot_pos['orientation']

        angle = math.atan2(
            ball_pos['y'] - robot_pos['y'],
            ball_pos['x'] - robot_pos['x'],
        )

        if angle < 0:
            angle = 2 * math.pi + angle

        if robot_angle < 0:
            robot_angle = 2 * math.pi + robot_angle

        robot_ball_angle = math.degrees(angle + robot_angle)

        robot_ball_angle -= 90
        if robot_ball_angle > 360:
            robot_ball_angle -= 360

        return robot_ball_angle

def rotateOnTangent(robot: dict, point: dict, goal: dict, R: float):
  deltaX = robot['x'] - point['x']
  deltaY = robot['y'] - point['y']

  dist = math.sqrt(deltaX**2 + deltaY**2)

  a = (goal['x'] - robot['x'])  * (goal['y'] - point['y']) - (goal['y'] - robot['y']) * (goal['x'] - point['x'])
  if(dist < R):
    if(a < 0):
        alpha = 90 + math.asin(abs(R / dist) - 1)
    else:
        alpha = -90 - math.asin(abs(R / dist) - 1)
  else:
    if(a < 0):
        alpha = math.asin(R / dist)
    else:
        alpha = -math.asin(R / dist)

  dx = deltaX * math.cos(alpha) - deltaY * math.sin(alpha)
  dy = deltaX * math.sin(alpha) + deltaY * math.cos(alpha) 
  
  c = {'x': robot['x'] - dx, 'y': robot['y'] - dy}

  return getAngleToPoint(c, robot)

def getAngleBetweenVectors(a, b: list):
    sina = cosSimMult(a, b) / (norm(a["x"], a["y"]) * norm(b["x"], b["y"]))
    cosa = scalarMult(a, b) / (norm(a["x"], a["y"]) * norm(b["x"], b["y"]))
    angle = math.atan2(cosa, sina)

    return angle


