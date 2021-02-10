# rcj_soccer_player controller - ROBOT B1
team = "BLUE"

# Feel free to import built-in libraries
import math

# You can also import scripts that you put into the folder with controller
import rcj_soccer_robot
import utilsAlex

teamMod = 1
if team == "BLUE":
    teamMod = -1


class MyRobot(rcj_soccer_robot.RCJSoccerRobot):
    def findGoalSlope(self, ball_pos):
        ball_distanceY = 0-ball_pos['y']
        ball_distanceX = 0.75-ball_pos['x']
        ball_slope = ball_distanceY/ball_distanceX


        return ball_slope

    def findDistance(self, point1, point):
        a = point1['x']-point['x']
        b = point['y']-point['y']
        a= abs(a)
        b= abs(b)



        return a, b
    def isBallRespawning(self, robot_pos, ball_pos, i):
        origin = {'x': 0, 'y': 0}
        xDistance, yDistance = self.findDistance(origin, ball_pos)
        xDistance2, yDistance2 = self.findDistance(robot_pos, ball_pos)

        ballRespawn = False
        if teamMod == -1:
            if i > 30 and xDistance < 0.01 and yDistance < 0.01:
                ballRespawn = True
        if teamMod == 1:
            if i > 30 and xDistance > 0.01 and yDistance > 0.01:
                ballRespawn = True
        return ballRespawn

    def isGoalScore(self, ball_pos):
        goalScored = False
        if ball_pos['x'] > 0.75 or ball_pos['x'] < -0.75:
            goalScored = True
        return goalScored

    def goToPoint(self, robot_pos, point):
        "Returns left and right speed to go to a certain point"

        pointAngle, robot_angle = self.get_angles(point, robot_pos)
        # print(pointAngle)
        direction = utilsAlex.get_direction(pointAngle)


        if direction == 0:
            left_speed = -10
            right_speed = -10
        elif pointAngle > 15 and pointAngle <= 180:
            left_speed = -8
            right_speed = 8
        elif pointAngle < 345 and pointAngle >= 180:
            left_speed = 8
            right_speed = -8



        return left_speed, right_speed




    def goToPosition(self, robot_pos, point):
        point1 = {'x':robot_pos['x'], 'y':point['y']}
        point2 = {'x':point['x'], 'y':robot_pos['y']}

        yDistance = robot_pos['y']-point['y']
        xDistance = robot_pos['x']-point['x']
        yDistance = abs(yDistance)
        xDistance = abs(xDistance)

        pointAngle1, robot_angle = self.get_angles(point1, robot_pos)
        pointAngle2, robot_angle = self.get_angles(point2, robot_pos)

        yDirection = utilsAlex.get_direction(pointAngle1)
        xDirection = utilsAlex.get_direction(pointAngle2)

        left_speed = 0
        right_speed = 0
        if yDistance > 0.01:
            if yDirection == 0:
                left_speed = -10
                right_speed = -10
            else:
                left_speed = -6
                right_speed = 6
        elif xDistance > 0.1:

            if xDirection == 0:
                left_speed = -10
                right_speed = -10
            else:
                left_speed = -6
                right_speed = 6
        elif xDistance < 0.1:
            if xDirection == 0:
                left_speed = -3
                right_speed = -3
            else:
                left_speed = -6
                right_speed = 6

        return left_speed, right_speed


    def findPushPoints(self, ball_pos, ball_slope):
        pass


    def findBallVelocity(self, ballList):
        lastIndex = len(ballList)
        if lastIndex > 1:
            point1 = ballList[lastIndex-1]
            point2 = ballList[lastIndex-1]

        return ballVelocity


    def predictBallPoint(self, ballVelocity):
        pass


    def run(self):
        ballList = []
        left_speed = 0
        right_speed = 0
        i= 0
        while self.robot.step(rcj_soccer_robot.TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()

                # Get the position of our robot
                robot_pos = data[self.name]
                i += 1
                # Get the position of the ball
                ball_pos = data['ball']
                ballRespawn = self.isBallRespawning(robot_pos, ball_pos, i)
                goalScored = self.isGoalScore(ball_pos)
                ballList.append(ball_pos)
                goalPos = {'x': teamMod * 0.75, 'y': -0.01}

                # Distance from the robot to the bal
                rb_DistanceX = abs(robot_pos['x']-ball_pos['x'])
                rb_DistanceY = abs(robot_pos['y']-ball_pos['y'])
                point = {'x': teamMod * -0.2, 'y': 0.0}
                if ballRespawn:
                    left_speed, right_speed = self.goToPoint(robot_pos, goalPos)
                else:
                    left_speed, right_speed = self.goToPoint(robot_pos, point)
                if goalScored:
                    i = 0
                """
                goalPosition = {'x':teamMod * 0.75,'y':0}
                ball_slope = self.findGoalSlope(ball_pos)
                point = utils.calculateGBRLine(ball_pos)
                print(point)
                # Get angle between the robot and the ball
                # and between the robot and the north
                ball_angle, robot_angle = self.get_angles(ball_pos, robot_pos)
                goal_angle, robot_angle = self.get_angles(goalPosition, robot_pos)



                # Compute the speed for motors
                xDistance, yDistance = self.findDistance(robot_pos, point)


                if yDistance > 0.01 and xDistance > 0.01:
                    left_speed, right_speed = self.goToPoint(robot_pos, point)
                else:
                   left_speed, right_speed = self.goToPoint(robot_pos, goalPosition)

                # If the robot has the ball right in front of it, go forward,
                # rotate otherwise
                """
                """
                if ball_pos["y"] > 0:
                    point1 = {'x':robot_pos['x'],'y':ball_pos["y"]}
                    point1_angle, robot_angle = self.get_angles(point1, robot_pos)
                    point_direction = utils.get_direction(point1_angle)
                    if robot_pos["y"] != ball_pos["y"]+0.5 and point_direction == 0:
                        left_speed = -10
                        right_speed = -10
                        print("going down")
                    else:
                        left_speed = point_direction * 10
                        right_speed = point_direction * -10
                        print("turning")
                elif ball_pos["y"] < -0:
                    point1 = {'x':robot_pos['x'],'y':ball_pos["y"]}
                    point1_angle, robot_angle = self.get_angles(point1, robot_pos)
                    point_direction = utils.get_direction(point1_angle)
                    if robot_pos["y"] != ball_pos["y"]+0.5 and point_direction == 0:
                        left_speed = -10
                        right_speed = -10
                        print("going up")
                    else:
                        left_speed = point_direction * 10
                        right_speed = point_direction * -10
                        print("turning")
                """






                # Set the speed to motors
                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)


my_robot = MyRobot()
my_robot.run()
