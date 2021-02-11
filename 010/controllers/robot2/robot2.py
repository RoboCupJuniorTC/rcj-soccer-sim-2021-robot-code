"""rcj_soccer_player controller."""
from controller import Robot
import struct
import math


TIME_STEP = 16
ROBOT_NAMES = ["B1", "B2", "B3", "Y1", "Y2", "Y3"]
N_ROBOTS = len(ROBOT_NAMES)

switchSidesMulti = 1
firstUpdate = True

def parse_supervisor_msg(packet: str) -> dict:
    # X, Z and rotation for each robot
    # plus X and Z for ball
    struct_fmt = 'ddd' * 6 + 'dd'

    unpacked = struct.unpack(struct_fmt, packet)

    data = {}
    for i, r in enumerate(ROBOT_NAMES):
        data[r] = {
            "x": unpacked[3 * i],
            "y": unpacked[3 * i + 1],
            "orientation": unpacked[3 * i + 2]
        }
    data["ball"] = {
        "x": unpacked[3 * N_ROBOTS],
        "y": unpacked[3 * N_ROBOTS + 1]
    }
    return data


class Vector():
    i = 0
    j = 0
    mag = 0

    def __str__(self):
        return ("i and J" +  str(self.i) + str(self.j) + "Magnitude" + str(self.mag))


class Position():
    def __init__(self, ax = None,ay = None):
        self.x = ax
        self.y = ay
    x = None
    y = None

    def __str__(self):
        return "x" + str(self.x) + ", y" + str(self.y)

class BallMotionPredictor:
    prevBallPosition = Position(0.1,0.1)
    currentBallPosition = Position(0.1,0.1)
    count = 0
    velocity = Vector()
    ballMotionGradient = 0
    def updateBallVelocity(self):
        self.velocity.mag = detector.getDisBetweenPoints(self.prevBallPosition, self.currentBallPosition)
        self.velocity.i = self.currentBallPosition.x - self.prevBallPosition.x
        self.velocity.j = self.currentBallPosition.y - self.prevBallPosition.y
        self.count += 1


    def getPointOfIntWithHome(self):
        #we calculuate equation of line
        run = self.currentBallPosition.x - self.prevBallPosition.x
        rise = self.currentBallPosition.y - self.prevBallPosition.y

        if run != 0:
            self.ballMotionGradient = (self.currentBallPosition.y - self.prevBallPosition.y)/(self.currentBallPosition.x - self.prevBallPosition.x)
            c = self.currentBallPosition.y - self.currentBallPosition.x * self.ballMotionGradient

            #Then find when ball intersects home line
            yIntHome = self.ballMotionGradient * playController.home.x + c
            playController.homeBallIntPos.y = yIntHome

    def updateBallHistory(self,ball_pos):
        holder = self.currentBallPosition
        self.currentBallPosition = Position(ball_pos["x"], ball_pos["y"])
        self.prevBallPosition = holder



#Handles movement control
class Movement:
    completedAction = False
    leftSpeed = 0
    rightSpeed = 0
    turnStatus = False
    def updateMotorValues(self):
        left_motor.setVelocity(self.leftSpeed)
        right_motor.setVelocity(self.rightSpeed)

    def facePoint(self, point, robotOrientation):
        deg = detector.getRobotAngleBetweenPoint(robotPos, robotOrientation, point)
        if deg > 360:
            deg -= 360
        elif deg < 0:
            deg += 360

        if deg >= 357 or deg <= 3:
            self.leftSpeed = 0
            self.rightSpeed = 0
        else:
            multiplier = -1 if deg < 180 else 1
            self.leftSpeed = multiplier * 4
            self.rightSpeed = multiplier * -4
        self.updateMotorValues()
    moveToPointStatus = False

    def followPoint(self,robotPos, robot_angle, dest):
        degrees = detector.getRobotAngleToBall(robotPos, robot_angle, dest)
        # Axis Z is forward
        # TODO: change the robot's orientation so that X axis means forward
        if degrees > 360:
            degrees -= 360
        elif degrees < 0:
            degrees += 360
        reverseMulti = 1


        if degrees > 90 and degrees < 270:
            reverseMulti = -1
            degrees = degrees + 180

        self.leftSpeed = 10
        self.rightSpeed = -10

        # If the robot has the ball right in front of it, go forward, otherwise
        # rotate
        if degrees > 360:
            degrees -= 360
        elif degrees < 0:
            degrees += 360



        if degrees >= 357 or degrees <= 3:
            self.leftSpeed = 10 * reverseMulti
            self.rightSpeed = 10 * reverseMulti
        else:
            multiplier = -1 if degrees < 180 else 1
            self.leftSpeed = multiplier * 4
            self.rightSpeed = multiplier * -4

        self.updateMotorValues()

    def moveToPoint(self,robotPos, robot_angle, dest, prec):
        self.moveToPointStatus = False

        degrees = detector.getRobotAngleToBall(robotPos, robot_angle, dest)
        # Axis Z is forward
        # TODO: change the robot's orientation so that X axis means forward
        if degrees > 360:
            degrees -= 360
        elif degrees < 0:
            degrees += 360
        reverseMulti = 1


        if degrees > 90 and degrees < 270:
            reverseMulti = -1
            degrees = degrees + 180

        self.leftSpeed = 10
        self.rightSpeed = -10

        # If the robot has the ball right in front of it, go forward, otherwise
        # rotate
        if degrees > 360:
            degrees -= 360
        elif degrees < 0:
            degrees += 360


        if detector.getDisBetweenPoints(robotPos, dest) > prec:
            if degrees >= 345 or degrees <= 15:
                self.leftSpeed = 10 * reverseMulti
                self.rightSpeed = 10 * reverseMulti
            else:
                multiplier = -1 if degrees < 180 else 1
                self.leftSpeed = multiplier * 4
                self.rightSpeed = multiplier * -4
        else:
            self.moveToPointStatus = True
            self.leftSpeed = 0
            self.rightSpeed = 0
        self.updateMotorValues()
        return self.moveToPointStatus

    def moveToBall(self,robotPos, robot_angle, dest):
        degrees = detector.getRobotAngleToBall(robotPos, robot_angle, dest)
        # Axis Z is forward
        # TODO: change the robot's orientation so that X axis means forward
        if degrees > 360:
            degrees -= 360
        elif degrees < 0:
            degrees += 360
        reverseMulti = 1
        print(degrees)

        if degrees > 90 and degrees < 270:
            reverseMulti = -1
            degrees = degrees + 180

        self.leftSpeed = 10
        self.rightSpeed = -10

        # If the robot has the ball right in front of it, go forward, otherwise
        # rotate
        if degrees > 360:
            degrees -= 360
        elif degrees < 0:
            degrees += 360
        multiplier = -1 if degrees < 180 else 1
        if degrees >= 345 or degrees <= 15:
            self.leftSpeed = 10 * reverseMulti
            self.rightSpeed = 10 * reverseMulti
        else:
            self.leftSpeed = multiplier * 10
            self.rightSpeed = multiplier * -10

        print("L", self.leftSpeed, "R", self.rightSpeed)
        self.updateMotorValues()


    def moveForward(self, reverseMulti):
        self.leftSpeed = 10
        self.rightSpeed = 10
        self.updateMotorValues()

    def faceAngle(self, robotOrientation, angle):
        deg = convertRadiansToDegrees(robotOrientation)
        deg += 90
        deg += angle
        self.turnStatus = False
        self.turnToAngle(deg)
        return self.turnStatus



    def turnToAngle(self,degrees):
        #NEEDS TO BE UPDATES SO CAN TURN EITHER WAY LEFT OR RIGHT
        if degrees > 360:
            degrees -= 360
        elif degrees < 0:
            degrees += 360
        multiplier = -1 if degrees < 180 else 1
        if degrees >= 357 or degrees <= 3:
            self.leftSpeed = 0
            self.rightSpeed = 0
            self.turnStatus = True
        elif degrees >= 360 - 30 or degrees <= 30:
            self.leftSpeed = multiplier * 4
            self.rightSpeed = multiplier * -4
        else:
            self.leftSpeed = multiplier * 10
            self.rightSpeed = multiplier * -10
        self.updateMotorValues()

#Handles logic of detecting objects
class Detector:

    def getDisBetweenPoints(self,point1, point2):
        return ((point1.x - point2.x) ** 2 + (point1.x - point2.x) ** 2) ** (1 / 2)

    def getAngleBetweenPoints(self,point1, point2):
        return math.atan2(point2.y - point1.y,
                          point2.x - point1.x)

    def getVerticleDis(self, point1, point2):
        return abs(point1.y - point2.y)

    def gethorizontalDis(self, point1, point2):
        return abs(point1.x - point2.x)

    #Point 1 should be robot and point 2 is ball
    def getRobotAngleBetweenPoint(self, point1, robotOrientation, point2):
        angle = self.getAngleBetweenPoints(point1, point2)
        if angle < 0:
            angle = 2 * math.pi + angle

        if robotOrientation < 0:
            robot_angle = 2 * math.pi + robotOrientation

        degrees = math.degrees(angle + robotOrientation)
        degrees -= 270
        return degrees

    def getRobotAngleToBall(self,robotPos, robotOrientation, ballPos):
        angle = self.getAngleBetweenPoints(robotPos,ballPos)
        if angle < 0:
            angle = 2 * math.pi + angle

        if robotOrientation < 0:
            robot_angle = 2 * math.pi + robotOrientation

        degrees = math.degrees(angle + robotOrientation)
        degrees -= 270
        return degrees




#Handles logic of what play the robot makes
class PlayController:
    destination = Position(0,0)
    home = Position(0.6 * switchSidesMulti,0)
    homeBallIntPos = Position(0.6 * switchSidesMulti,0)
    count = 0
    moveForwardCount = 0
    def update(self, robotPos, robotAngle,ballPos):


        self.count += 1
        disFromHome = detector.getDisBetweenPoints(self.home, robotPos)
        disToBall = detector.getDisBetweenPoints(robotPos, ballPos)

        ballMotionPredictor.updateBallHistory(ball_pos)
        ballMotionPredictor.updateBallVelocity()
        ballMotionPredictor.getPointOfIntWithHome()

        horizontalDis = detector.getVerticleDis(robotPos, self.home)
        movingToDest = True
        followingPoint = False
        ballPos.x = ballPos.x * switchSidesMulti
        unadjustedBallPos = Position(ballPos.x * switchSidesMulti, ballPos.y)

        if abs(ballPos.x) < 0.05 and abs(ballPos.y) < 0.05:
            #This is the kickoff
            self.destination = Position(0.7* switchSidesMulti,0)

        elif ballPos.y > 0.3 and ballPos.x > 0.5 :
            print("CASE 6")
            #Moves to corner of box if ball stuck in corner
            self.destination = Position(0.7* switchSidesMulti, 0.25)
        elif ballPos.y < -0.3 and ballPos.x >0.5:
            print("CASE 5")
            #Moves to corner of box if ball stuck in corner
            self.destination = Position(0.7 * switchSidesMulti, -0.25)
        elif disToBall < 0.2 and robotPos.x  < ballPos.x and abs(ballPos.y) < 0.25:
            print("CASE 1")
            # Ball is between goalie and gaol
            #this means we don't want to go for it
            self.destination = self.home
        elif disToBall < 0.2 and disFromHome < 0.4:
            print("CASE 2")
            #robot should go after ball
            self.destination = unadjustedBallPos
        elif horizontalDis > 0.4 or disFromHome >  0.4:
            print("CASE 3")
            #robot needs to make way back to home
            self.destination = self.home
        elif ballPos.x > 0:
            print("CASE 4")
            #Ball close to goal so we just go to its x pos
            followingPoint = True
            self.destination = Position(robotPos.x * switchSidesMulti, ballPos.y)
        else:
            followingPoint = True
            #Robot predicts pos
            print("CASE 5")
            self.destination = self.homeBallIntPos
            disToHomeBallIntPos = detector.getDisBetweenPoints(robotPos,self.homeBallIntPos)
        print(self.homeBallIntPos)
        print("ballPos", ballPos)
        print("unballPos", unadjustedBallPos)
        print("robotPos", robotPos)
        print("Dest", self.destination)
        if followingPoint:
            movement.followPoint(robotPos, robotAngle, self.destination)
        elif movingToDest:
            movement.moveToPoint(robotPos,robotAngle,self.destination, 0)




def passDictToPositionObj(dict):
    pos = Position(0,0)
    pos.x = dict["x"]
    pos.y = dict["y"]
    return pos


def convertRadiansToDegrees(rad):
    return rad * 180 / math.pi


# create the Robot instance.
robot = Robot()

name = robot.getName()
team = name[0]
player_id = int(name[1])

ballPosHistory = [[0,0],[0,0]]
receiver = robot.getReceiver("receiver")
receiver.enable(TIME_STEP)

left_motor = robot.getMotor("left wheel motor")
right_motor = robot.getMotor("right wheel motor")

left_motor.setPosition(float('+inf'))
right_motor.setPosition(float('+inf'))

left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)


#Destinations
robotPos = Position(0,0)
ballPos = Position(0,0)

detector = Detector()
movement = Movement()
playController = PlayController()
ballMotionPredictor = BallMotionPredictor()
while robot.step(TIME_STEP) != -1:
    if receiver.getQueueLength() > 0:
        packet = receiver.getData()
        receiver.nextPacket()

        data = parse_supervisor_msg(packet)


        # Get the position of our robot
        robot_pos = data[name.upper()]
        # Get the position of the ball
        ball_pos = data['ball']

        robotPos = passDictToPositionObj(robot_pos)
        ballPos = passDictToPositionObj(ball_pos)
        if firstUpdate:
            firstUpdate = False
            if robotPos.x < 0:
                switchSidesMulti = -1

        playController.home = Position(0.6 * switchSidesMulti, 0)
        playController.homeBallIntPos = Position(0.6 * switchSidesMulti, 0)


        robot_angle = robot_pos['orientation']


        # Get the angle between the robot and the ball
        playController.update(robotPos, robot_angle, ballPos)
        #movement.moveForward(1)
        #movement.faceAngle(robot_angle,20)
        #movement.moveToBall(robotPos, robot_angle, ballPos)
        #movement.moveToPoint(robotPos, robot_angle, Position(0,0))
        #print('Robot Position:', robot_pos, 'Ball Position:', ball_pos, 'Angle', degrees)
