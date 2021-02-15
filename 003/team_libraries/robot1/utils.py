import math
from typing import Tuple

# define constants
ROBOT_SPEED = 0.1
RADIUS_AROUND_BALL = 0.1
FIELD_SIZE = [1.5, 1.3]

# define global variables
last_ball_pos = {"x": 0, "y": 0}
current_ball_pos = {"x": 0, "y": 0}

def frange(start: float, stop: float, step: float=1):
    """This function has the same functionality as the range() funciton, but works with floats too.

    Args:
        start (float): start value
        stop (float): stop value
        step (float, optional): step size. Defaults to 1.

    Yields:
        Iterator[float]: iterator
    """
    r = start
    while r < stop:
        yield r
        r += step

def normalisePositions(positions: dict, team: str) -> dict:
    """normalise coords, so that positive x is always
       in the direction of the goal of the other team.
       It also saves the last ball_pos to determine the speed of the ball


    Args:
        positions (dict): dict with positions which should be normalised
        team (str): team of the robot

    Returns:
        dict: normalised position
    """
    global last_ball_pos
    global current_ball_pos

    if 'B' in team:
        for position in positions.values():
            position['x'] *= -1
            position['y'] *= -1
            if len(position) > 2:
                position['orientation'] += math.pi
                if position['orientation'] > 2 * math.pi:
                    position['orientation'] -= 2 * math.pi
    for position in positions.values():
        if len(position) > 2:
            position['orientation'] -= math.pi / 2
            if position['orientation'] < 0:
                position['orientation'] += 2 * math.pi
            position['orientation'] = 2 * math.pi - position['orientation']
    last_ball_pos = current_ball_pos
    current_ball_pos = positions["ball"]
    return positions

def turnToCoords(robotPosition: dict, position: dict = None, x=0, y=0) -> Tuple[float, float]:
    """This function uses a p-controller to determine the speed 
       in which the robot should drive to turn to the specified coords.

    Args:
        robotPosition (dict): the postition of the robot.
        position (dict, optional): position of the coords. If it isn't specified x and y must be specified. Defaults to None.
        x ([type], optional): x position of coords. Defaults to 0.
        y ([type], optional): y position of coords. Defaults to 0.

    Returns:
        Tuple[float, float]: The left speed and right speed normalized(-1 - 1).
    """

    # create position if x and y where specified
    if position is None:
        position = {}
        position['x'] = x
        position['y'] = y

    # get angle from robot to goal position
    angle = math.atan2(
        position['y'] - robotPosition['y'],
        position['x'] - robotPosition['x'],
    )

    if angle < 0:
        angle += math.pi * 2
    
    # compute robot_goal_angle_diff
    robot_goal_angle_diff = angle - robotPosition['orientation']

    if robot_goal_angle_diff > math.pi: robot_goal_angle_diff -= 2 * math.pi
    if robot_goal_angle_diff < -math.pi:robot_goal_angle_diff += 2 * math.pi

    # convert robot_goal_angle_diff to degrees
    robot_goal_angle_diff = math.degrees(robot_goal_angle_diff)

    # calculate velocity
    vel = min(1, max(-1, robot_goal_angle_diff / 40))

    return (- vel, vel)

def driveToCoordsKeeper(robotPosition: dict, position: dict = None, x=0, y=0) -> Tuple[float, float]:
    """Drive to coords using a different approach then driveToCoords(). 
       The robot turns around itself to face the correct direction and then starts driving forward.

    Args:
        robotPosition (dict): current position of the robot
        position (dict, optional): position of the coords. If it isn't specified x and y must be specified. Defaults to None.
        x ([type], optional): x position of coords. Defaults to 0.
        y ([type], optional): y position of coords. Defaults to 0.

    Returns:
        Tuple[float, float]: The left speed and right speed normalized(-1 - 1).
    """
    # create position if x and y where specified
    if position is None:
        position = {}
        position['x'] = x
        position['y'] = y

    # get angle from robot to goal position
    angle = math.atan2(
        position['y'] - robotPosition['y'],
        position['x'] - robotPosition['x'],
    )

    if angle < 0: angle += math.pi * 2

    # calculate difference between current angle and goal angle
    robot_goal_angle_diff = angle - robotPosition['orientation']

    if robot_goal_angle_diff > math.pi: robot_goal_angle_diff -= 2 * math.pi
    if robot_goal_angle_diff < -math.pi:robot_goal_angle_diff += 2 * math.pi

    # convert robot_goal_angle_diff to degrees
    robot_goal_angle_diff = math.degrees(robot_goal_angle_diff)

    # choose direction in which the robot is driving: 1 -> forwards, -1 -> backwards
    direction = -1
    if abs(robot_goal_angle_diff) > 90:
        direction = 1
        robot_goal_angle_diff += 180
        if robot_goal_angle_diff > 180:
            robot_goal_angle_diff -= 360

    # if robot_goal_angle_diff is smaller than 20 degrees: p-controller
    if abs(robot_goal_angle_diff) < 20:
        velocity = (1 * direction - robot_goal_angle_diff / 15,
                    1 * direction + robot_goal_angle_diff / 15)
        # normalize the velocity to the max of 1
        normalizer_quotient = max(abs(velocity[0]), abs(velocity[1]))

        velocity = (velocity[0] / normalizer_quotient,
                    velocity[1] / normalizer_quotient)
    # if robot_goal_angle_diff is greater than 90 degrees: turning on max speed
    elif abs(robot_goal_angle_diff) > 90:
        vel = 1 * (robot_goal_angle_diff / abs(robot_goal_angle_diff))
        velocity = (-vel, vel)
    # if robot_goal_angle_diff is between 20 and 90 degrees: use a faster p-controller
    else:
        vel = robot_goal_angle_diff / 90
        velocity = (-vel, vel)

    return (velocity[0], velocity[1])

def driveToCoords(robotPosition: dict, position: dict = None, x = None, y = None) -> Tuple[float, float]:
    """Computes the right and left speed to drive the robot to the specified position by using a p-controller.

    Args:
        robotPosition (dict): current position of the robot
        position (dict, optional): position of the coords. If it isn't specified x and y must be specified. Defaults to None.
        x ([type], optional): x position of coords. Defaults to 0.
        y ([type], optional): y position of coords. Defaults to 0.

    Returns:
        Tuple[float, float]: The left speed and right speed normalized(-1 - 1).
    """

    # create position if x and y where specified
    if position is None:
        position = {}
        position['x'] = x
        position['y'] = y

    # get angle from robot to goal position
    angle = math.atan2(
        position['y'] - robotPosition['y'],
        position['x'] - robotPosition['x'],
    )

    if angle < 0: angle += math.pi * 2

    # compute robot angle diff
    robot_goal_angle_diff = angle - robotPosition['orientation']

    if robot_goal_angle_diff > math.pi: robot_goal_angle_diff -= 2 * math.pi
    if robot_goal_angle_diff < -math.pi:robot_goal_angle_diff += 2 * math.pi

    # convert robot angle diff to degrees
    robot_goal_angle_diff = math.degrees(robot_goal_angle_diff)

    # choose direction in which the robot is driving: 1 -> forwards, -1 -> backwards
    direction = -1

    if abs(robot_goal_angle_diff) > 90:
        direction = 1
        robot_goal_angle_diff += 180
        if robot_goal_angle_diff > 180:
            robot_goal_angle_diff -= 360

    # convert robot angle diff back to radians
    robot_goal_angle_diff = math.radians(robot_goal_angle_diff)

    # calculate velocity by using a p-controller
    velocity = 0
    if robot_goal_angle_diff > 0:
        velocity = (1 - min(robot_goal_angle_diff, 2),
                    1 )
    else:
        velocity = (1 ,
                    1 - max(abs(robot_goal_angle_diff), 2))
    # applies the direction to the calculated speed
    if direction == -1:
        velocity = (velocity[1]*-1, velocity[0]*-1)
    return velocity

def isAtGoal(robotPosition: dict, goal: dict = None, x: float=0, y: float=0, maxDistance: float = 0.01) -> bool:
    """This function checks if the distance between robotPosition and goal is greater than maxDistance.

    Args:
        robotPosition (dict): the postition of the robot.
        goal (dict, optional): position of the coords. If it isn't specified x and y must be specified. Defaults to None.
        x ([type], optional): x position of coords. Defaults to 0.
        y ([type], optional): y position of coords. Defaults to 0.
        maxDistance (float, optional): The distance in which the goal is still reached. Defaults to 0.01.

    Returns:
        bool: True if goal is reached
    """
    # create position if x and y where specified
    if goal is None:
        goal = {}
        goal['x'] = x
        goal['y'] = y
    # calculate cartesian distance and compare it to maxDistance
    if math.sqrt(abs(goal['x']-robotPosition['x'])**2 + abs(goal['y']-robotPosition['y'])**2) < maxDistance:
        return True
    return False

def getBallSpeed() -> dict:
    """Returns the speed of the ball since the last step.

    Returns:
        dict: vector with x and y component which represents the speed
    """

    ball_speed = {}
    ball_speed["x"] = (current_ball_pos["x"] - last_ball_pos["x"]) / (64 / 1000)
    ball_speed["y"] = (current_ball_pos["y"] - last_ball_pos["y"]) / (64 / 1000)

    return ball_speed

def ballPositionIn(ball_pos: dict, ball_speed: dict, time: float) -> dict:
    """calculates the position of the ball in the specified time based 
       on the current ball position and ball speed. Takes the walls into account.

    Args:
        ball_pos (dict): current ball position
        ball_speed (dict): current ball speed
        time (float): time

    Returns:
        dict: the calculated future position 
    """

    # compute position in future
    ball_delta_y = ball_speed['y'] * time
    ball_delta_x = ball_speed['x'] * time

    new_ball_pos = {}

    new_ball_pos['x'] = ball_delta_x + ball_pos['x']
    new_ball_pos['y'] = ball_delta_y + ball_pos['y']

    # if computed coords are out of bounds, the ball bounces from the wall.
    if not (-FIELD_SIZE[0] / 2 < new_ball_pos['x'] < FIELD_SIZE[0] / 2 and -FIELD_SIZE[1] / 2 < new_ball_pos['y'] < FIELD_SIZE[0] / 2):
        if -FIELD_SIZE[0] / 2 > new_ball_pos['x']:
            x_distance_out_of_bounds = new_ball_pos['x'] - (-FIELD_SIZE[0] / 2)
            new_ball_pos['x'] = -FIELD_SIZE[0] / 2 - x_distance_out_of_bounds

        elif FIELD_SIZE[0] / 2 < new_ball_pos['x']:
            x_distance_out_of_bounds = new_ball_pos['x'] - (FIELD_SIZE[0] / 2)
            new_ball_pos['x'] = FIELD_SIZE[0] / 2 - x_distance_out_of_bounds
        
        elif -FIELD_SIZE[1] / 2 > new_ball_pos['y']:
            y_distance_out_of_bounds = new_ball_pos['y'] - (-FIELD_SIZE[1] / 2)
            new_ball_pos['y'] = -FIELD_SIZE[0] / 2 - y_distance_out_of_bounds

        elif FIELD_SIZE[1] / 2 < new_ball_pos['y']:
            y_distance_out_of_bounds = new_ball_pos['y'] - (FIELD_SIZE[1] / 2)
            new_ball_pos['y'] = FIELD_SIZE[0] / 2 - y_distance_out_of_bounds

    if not (-FIELD_SIZE[0] / 2 < new_ball_pos['x'] < FIELD_SIZE[0] / 2 and -FIELD_SIZE[1] / 2 < new_ball_pos['y'] < FIELD_SIZE[0] / 2):
        if -FIELD_SIZE[0] / 2 > new_ball_pos['x']:
            x_distance_out_of_bounds = new_ball_pos['x'] - (-FIELD_SIZE[0] / 2)
            new_ball_pos['x'] = -FIELD_SIZE[0] / 2 - x_distance_out_of_bounds

        elif FIELD_SIZE[0] / 2 < new_ball_pos['x']:
            x_distance_out_of_bounds = new_ball_pos['x'] - (FIELD_SIZE[0] / 2)
            new_ball_pos['x'] = FIELD_SIZE[0] / 2 - x_distance_out_of_bounds
        
        elif -FIELD_SIZE[1] / 2 > new_ball_pos['y']:
            y_distance_out_of_bounds = new_ball_pos['y'] - (-FIELD_SIZE[1] / 2)
            new_ball_pos['y'] = -FIELD_SIZE[0] / 2 - y_distance_out_of_bounds

        elif FIELD_SIZE[1] / 2 < new_ball_pos['y']:
            y_distance_out_of_bounds = new_ball_pos['y'] - (FIELD_SIZE[1] / 2)
            new_ball_pos['y'] = FIELD_SIZE[0] / 2 - y_distance_out_of_bounds


    return new_ball_pos

def calculateTimeFromBotToPosition(robot_pos: dict, position: dict, v: float) -> float:
    """estimates the time from the current robot position to the 
       specified position by using a fixed velocity for the robot.

    Args:
        robot_pos (dict): current robot position
        position (dict): goal position
        v (float): speed of the robot

    Returns:
        float: the time needed to travel to other point
    """

    # calculate euclidean distance
    s = getDistanceBetweenPoints(robot_pos, position)
    
    # uses formula time = distance / velocity to compute and returntime
    return (s/v)

def getDistanceBetweenPoints(point1: dict, point2: dict) -> float:
    """calculates the euclidean distance between the first and the second point.

    Args:
        point1 (dict): first point
        point2 (dict): second point

    Returns:
        float: euclidean distance
    """
    return math.sqrt(abs(point2['x']-point1['x'])**2 + abs(point2['y']-point1['y'])**2)

def calculatePositionBehindBall(ball_position: dict, target_position: dict) -> dict:
    """calculate position in which the ball is between the robot and the target
       and the distance to the ball is equal to RADIUS_AROUND_BALL. 

    Args:
        ball_position (dict): position of the ball
        target_position (dict): position of the target

    Returns:
        dict: position behind ball
    """

    # using trigonometrie to calculate point on a circle with the radius RADIUS_AROUND_BALL
    alpha = math.atan2(target_position["y"] - ball_position["y"], target_position["x"] - ball_position["x"])
    y = math.sin(alpha+math.pi)*RADIUS_AROUND_BALL
    x = math.cos(alpha+math.pi)*RADIUS_AROUND_BALL

    # add this point to the current ball position
    return {"x": ball_position["x"] + x, "y": ball_position["y"] + y}

def nearestPoint(position:dict, point1: dict, point2: dict) -> dict:
    """This function returns the point which has the smaller distance to the specified position.

    Args:
        position (dict): position to which the distance is measured
        point1 (dict): first point
        point2 (dict): second point

    Returns:
        dict: the point which distance to the specified position is smaller
    """
    if getDistanceBetweenPoints(point1, position) < getDistanceBetweenPoints(point2, position):
        return point1
    else:
        return point2