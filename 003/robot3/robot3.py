import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
sys.path.append('/app/controllers')

# rcj_soccer_player controller - ROBOT B2

###### REQUIRED in order to import files from B1 controller
import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
# You can now import scripts that you put into the folder with your
# robot B1 controller


# tries to import from rcj_soccer_player_b1 first then from rcj_soccer_player_b1 and then from i_bots_2_robot_1
try:
    from team_003_libraries.robot1 import asdf45s3df45
    print("blue")
    from team_003_libraries.robot1 import rcj_soccer_robot, utils, coords
except:
    try:
        from team_003_libraries.robot1 import asdf45s3df45
        print("yellow")
        from team_003_libraries.robot1 import rcj_soccer_robot, utils, coords
    except:
        from team_003_libraries.robot1 import rcj_soccer_robot, utils, coords

import math
# Feel free to import built-in libraries
CORRIDOR_LENGTH = 0.4
CORRIDOR_WIDTH = 0.2

AREA_BEHIND_BALL_LENGTH = 0.1
AREA_BEHIND_BALL_WIDTH = 0.1

EVADE_SPOTS = [{"x": -0.1, "y": 0.15}, {"x": -0.1, "y": -0.15}]
POSITION_BEHIND_BALL = {"x": -0.2, "y":0}

class MyRobot(rcj_soccer_robot.RCJSoccerRobot):

    VELOCITY_MULTIPLIER = 10
    inPosition = False
    waiting_pos = {"x": 0, "y": 0.3}
    ENEMY_ROBOT_NAMES = []




    def run(self):

        if 'B' in self.name:
            self.ENEMY_ROBOT_NAMES = ["Y1", "Y2", "Y3"]
        else:
            self.ENEMY_ROBOT_NAMES = ["B1", "B2", "B3"]

        predict_ball_position = True
        ball_pos_predicted = {"x": 0, "y": 0}
        last_predicted = 0
        while self.robot.step(rcj_soccer_robot.TIME_STEP) != -1:

            if self.is_new_data():
                data = utils.normalisePositions(self.get_new_data(), self.name)
                # Get the position of our robot
                robot_pos = data[self.name]

                # Get the position of the ball
                ball_pos = data['ball']
                
                # start predicting again if time is up
                if self.robot.getTime() - last_predicted > 2.2:
                    predict_ball_position = True

                # predict ball position
                if predict_ball_position:
                    print("predicting")
                    ball_pos_predicted = utils.ballPositionIn(ball_pos,utils.getBallSpeed(),2)
                    # print(utils.getBallSpeed())
                else:
                    print("not predicting")

                closestRobotToBall = self.getClosestRobotToBall(data)

                if utils.isAtGoal(ball_pos, data[closestRobotToBall], maxDistance=0.3):
                    print("enemy robot to close for predict")
                    ball_pos_predicted = ball_pos
                # position relative to ball
                robot_pos_relative_to_ball = {"x": robot_pos["x"] - ball_pos_predicted["x"], "y": robot_pos["y"] - ball_pos_predicted["y"]}
                angle = math.atan2(coords.TOR_POS_MIDDLE['y'] - ball_pos_predicted['y'],
                                   coords.TOR_POS_MIDDLE['x'] - ball_pos_predicted['x'])
                angle *= -1

                # if ball to close to wall
                if not (ball_pos_predicted["x"] < 0.5 and -0.53< ball_pos_predicted["y"] < 0.53):
                    angle = 0
                print("Angle:" + str(math.degrees(angle)))
                c,s = math.cos(angle),math.sin(angle)
                rotatedX = c * robot_pos_relative_to_ball["x"] - s * robot_pos_relative_to_ball["y"]
                rotatedY = s * robot_pos_relative_to_ball["x"] + c * robot_pos_relative_to_ball["y"]
                
                robot_pos_relative_to_ball = {"x": rotatedX, "y": rotatedY}

                goal_spot = None

                if robot_pos_relative_to_ball["x"] > 0:
                    # print("in front of ball")
                    goal_spot = EVADE_SPOTS[0]
                    if robot_pos_relative_to_ball["y"]< 0:
                        goal_spot = EVADE_SPOTS[1]
                # in position behind ball
                elif - AREA_BEHIND_BALL_WIDTH/2 < robot_pos_relative_to_ball["y"] < AREA_BEHIND_BALL_WIDTH/2 and robot_pos_relative_to_ball["x"] > -AREA_BEHIND_BALL_LENGTH:
                    # print("drive to ball")
                    goal_spot = {"x": 0, "y": 0}
                # in corridor behind ball
                elif -CORRIDOR_WIDTH/2 < robot_pos_relative_to_ball["y"] < CORRIDOR_WIDTH/2 and robot_pos_relative_to_ball["x"]>-CORRIDOR_LENGTH:
                    if predict_ball_position:

                        predict_ball_position = False
                        last_predicted = self.robot.getTime()
                    # how far in the middle is the robot
                    in_middle = abs(robot_pos_relative_to_ball["y"]) / (CORRIDOR_WIDTH / 2)
                    goal_spot = {"x": in_middle * POSITION_BEHIND_BALL["x"], "y": 0}
                    # print("in corridor: " + str(in_middle))
                # drive to spot behind ball
                else:
                    # print("drive to pos behind ball")
                    goal_spot = POSITION_BEHIND_BALL
                # print(goal_spot)
                
                c,s = math.cos(-angle),math.sin(-angle)
                rotatedX = c * goal_spot["x"] - s * goal_spot["y"]
                rotatedY = s * goal_spot["x"] + c * goal_spot["y"]
                
                

                # if ball near goal of enemy               
                if ball_pos_predicted["x"]> 0.65:
                    leftSpeed, rightSpeed = utils.driveToCoords(data[self.name], {"x": ball_pos_predicted["x"],
                                                                                    "y": ball_pos_predicted["y"]})
                else:
                    leftSpeed, rightSpeed = utils.driveToCoords(data[self.name], {"x": ball_pos_predicted["x"] + rotatedX,
                                                                              "y": ball_pos_predicted["y"] + rotatedY})

                if  ball_pos["x"] < -0.35:
                    leftSpeed, rightSpeed = utils.driveToCoords(data[self.name], {"x": -0.3, "y": 0})
 
                self.left_motor.setVelocity(leftSpeed * self.VELOCITY_MULTIPLIER)
                self.right_motor.setVelocity(rightSpeed * self.VELOCITY_MULTIPLIER)

    def getClosestRobotToBall(self, data):
        closest_distance = 100
        closest_robot_name = ""
        for name in self.ENEMY_ROBOT_NAMES:
            distance = utils.getDistanceBetweenPoints(data[name], data["ball"])
            if distance < closest_distance:
                closest_distance = distance
                closest_robot_name = name
        return closest_robot_name
my_robot = MyRobot()
my_robot.run()
