import math

def spin(self, robot_angle, angle, left_speed, right_speed, spin_speed, angle_range):
    if robot_angle - angle >= 0:
        left_total = robot_angle - angle
    else:
        left_total = robot_angle + 360 - angle
    if angle - robot_angle >= 0:
        right_total = angle - robot_angle
    else:
        right_total = angle + 360 - robot_angle
    if robot_angle < angle - angle_range or robot_angle > angle + angle_range:
        if (left_total > right_total):
            left_speed = spin_speed
            right_speed = -spin_speed
        else:
            left_speed = -spin_speed
            right_speed = spin_speed
    # print("Spin")
    return left_speed, right_speed

def move(self, robot_angle, left_speed, right_speed, relative, absolute, straight):
    if straight == True:
        angle = direction(self, robot_angle, 0, 180)
        if angle == 180:
            left_speed = left_speed
            right_speed = right_speed
        else:
            left_speed = -left_speed
            right_speed = -right_speed
    else:
        angle = direction(self, robot_angle, relative, absolute)
        if angle == absolute:
            left_speed = left_speed
            right_speed = right_speed
        else:
            left_speed = -left_speed
            right_speed = -right_speed
    # print("Move")
    return left_speed, right_speed

def coords(self, robot_angle, robot_x, robot_y, dest_x, dest_y):
    angleA = (math.degrees(math.atan2(robot_x - dest_x, robot_y - dest_y))) % 360
    angleB = (math.degrees(math.atan2(robot_x - dest_x, robot_y - dest_y)) + 180) % 360
    if robot_angle - angleA >= 0:
        leftA_total = robot_angle - angleA
    else:
        leftA_total = robot_angle + 360 - angleA
    if angleA - robot_angle >= 0:
        rightA_total = angleA - robot_angle
    else:
        rightA_total = angleA + 360 - robot_angle
    if robot_angle - angleB >= 0:
        leftB_total = robot_angle - angleB
    else:
        leftB_total = robot_angle + 360 - angleB
    if angleB - robot_angle >= 0:
        rightB_total = angleB - robot_angle
    else:
        rightB_total = angleB + 360 - robot_angle
    if leftA_total < rightA_total:
        a_close = leftA_total
    else:
        a_close = rightA_total
    if leftB_total < rightB_total:
        b_close = leftB_total
    else:
        b_close = rightB_total
    if a_close < b_close:
        angle = angleA
    else:
        angle = angleB
    # print("Coordinates")
    return angle, angleA

def direction(self, robot_angle, angleA, angleB):
    if robot_angle - angleA >= 0:
        leftA_total = robot_angle - angleA
    else:
        leftA_total = robot_angle + 360 - angleA
    if angleA - robot_angle >= 0:
        rightA_total = angleA - robot_angle
    else:
        rightA_total = angleA + 360 - robot_angle
    if robot_angle - angleB >= 0:
        leftB_total = robot_angle - angleB
    else:
        leftB_total = robot_angle + 360 - angleB
    if angleB - robot_angle >= 0:
        rightB_total = angleB - robot_angle
    else:
        rightB_total = angleB + 360 - robot_angle
    if leftA_total < rightA_total:
        a_close = leftA_total
    else:
        a_close = rightA_total
    if leftB_total < rightB_total:
        b_close = leftB_total
    else:
        b_close = rightB_total
    if a_close < b_close:
        angle = angleA
    else:
        angle = angleB
    # print("Direction")
    return angle

def chase(self, robot_angle, robot_y, ball_y):
    if ball_y < robot_y:
        left_speed, right_speed = move(self, robot_angle, -7, -7, 0, 0, True)
    elif ball_y > robot_y:
        left_speed, right_speed = move(self, robot_angle, 7, 7, 0, 0, True)
    else:
        left_speed, right_speed =  move(self, robot_angle, 0, 0, 0, 0, True)
    # print("Chase")
    return left_speed, right_speed

def border(self, robot_angle, robot_y, left_speed, right_speed, limit1, limit2, given_range):
    if limit2 < limit1:
        limitA = limit2
        limitB = limit1
    elif limit1 < limit2:
        limitA = limit1
        limitB = limit2
    else:
        return left_speed, right_speed
    if robot_y < limitA:
        left_speed, right_speed = move(self, robot_angle, 10, 10, 0, 0, True)
    elif robot_y > limitB:
        left_speed, right_speed = move(self, robot_angle, -10, -10, 0, 0, True)
    elif robot_y > limitA and robot_y < limitA + given_range and left_speed < 0:
        angle = direction(self, robot_angle, 0, 180)
        if (angle == 180 and left_speed < 0 or angle == 0 and left_speed > 0):
            left_speed = 1
            right_speed = 1
    elif robot_y < limitB and robot_y > limitB - given_range and left_speed > 0:
        angle = direction(self, robot_angle, 0, 180)
        if (angle == 180 and left_speed > 0 or angle == 0 and left_speed < 0):
            left_speed = -1
            right_speed = -1
    return left_speed, right_speed