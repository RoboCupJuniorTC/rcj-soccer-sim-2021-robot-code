# rcj_soccer_player controller - ROBOT B2

###### REQUIRED in order to import files from B1 controller
import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
# You can now import scripts that you put into the folder with your
# robot B1 controller

# tries to import from rcj_soccer_player_b1 first then from rcj_soccer_player_b1 and then from i_bots_2_robot_1
try:
    from rcj_soccer_player_b1 import asdf45s3df45
    print("blue")
    from rcj_soccer_player_b1 import rcj_soccer_robot, utils, coords
except:
    try:
        from rcj_soccer_player_b1 import asdf45s3df45
        print("yellow")
        from rcj_soccer_player_y1 import rcj_soccer_robot, utils, coords
    except:
        from i_bots_2_robot_1 import rcj_soccer_robot, utils, coords

import math

#####

CORRIDOR_LENGTH = 0.4
CORRIDOR_WIDTH = 0.2

AREA_BEHIND_BALL_LENGTH = 0.1
AREA_BEHIND_BALL_WIDTH = 0.1

EVADE_SPOTS = [{"x": -0.1, "y": 0.15}, {"x": -0.1, "y": -0.15}]
POSITION_BEHIND_BALL = {"x": -0.2, "y":0}



class MyRobot(rcj_soccer_robot.RCJSoccerRobot):

    VELOCITY_MULTIPLIER = 10
    ENEMY_ROBOT_NAMES = []
    waiting_position_reached = 0
    
    
    def attack(self, robot_pos, ball_pos):
        robot_pos_relative_to_ball = {"x": robot_pos["x"] - 0, "y": robot_pos["y"] - 0}
        goal_spot = None
        if robot_pos_relative_to_ball["x"] > 0:
            goal_spot = EVADE_SPOTS[0]
            if robot_pos_relative_to_ball["y"]< 0:
                goal_spot = EVADE_SPOTS[1]
        elif - AREA_BEHIND_BALL_WIDTH/2 < robot_pos["y"] - ball_pos["y"] < AREA_BEHIND_BALL_WIDTH/2 and robot_pos["x"] - ball_pos["x"] > -AREA_BEHIND_BALL_LENGTH:
            goal_spot = {"x": 0, "y": 0}
            leftSpeed, rightSpeed = utils.driveToCoords(robot_pos, {"x": ball_pos["x"] + goal_spot["x"],
                                                                    "y": ball_pos["y"] + goal_spot["y"]})
            return leftSpeed, rightSpeed
        # in position behind ball
        elif - AREA_BEHIND_BALL_WIDTH/2 < robot_pos_relative_to_ball["y"] < AREA_BEHIND_BALL_WIDTH/2 and robot_pos_relative_to_ball["x"] > -AREA_BEHIND_BALL_LENGTH:
            if self.waiting_position_reached + 3 < self.robot.getTime():
                self.waiting_position_reached = self.robot.getTime()  
                return 0,0              
            if self.waiting_position_reached + 2 < self.robot.getTime():
                goal_spot = {"x": -0.2, "y": 0}    
            else:
                return 0,0
        # in corridor behind ball
        elif -CORRIDOR_WIDTH/2 < robot_pos_relative_to_ball["y"] < CORRIDOR_WIDTH/2 and robot_pos_relative_to_ball["x"]>-CORRIDOR_LENGTH:
            # how far in the middle is the robot
            in_middle = abs(robot_pos_relative_to_ball["y"]) / (CORRIDOR_WIDTH / 2)
            goal_spot = {"x": in_middle * POSITION_BEHIND_BALL["x"], "y": 0}
        # drive to spot behind ball
        else:
            goal_spot = POSITION_BEHIND_BALL
        leftSpeed, rightSpeed = utils.driveToCoords(robot_pos, {"x": 0 + goal_spot["x"],
                                                                      "y": 0 + goal_spot["y"]})
        return leftSpeed, rightSpeed

    def block_attack(self, robot_pos, ball_pos):
        # position relative to ball
        robot_pos_relative_to_ball = {"x": robot_pos["x"] - ball_pos["x"], "y": robot_pos["y"] - ball_pos["y"]}
        angle = math.atan2(coords.TOR_POS_MIDDLE['y'] - ball_pos['y'],
                            coords.TOR_POS_MIDDLE['x'] - ball_pos['x'])
        angle *= -1
        
        # if ball to close to wall
        if not (ball_pos["x"] < 0.3 and -0.53< ball_pos["y"] < 0.53):
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
        
        leftSpeed, rightSpeed = utils.driveToCoords(robot_pos, {"x": ball_pos["x"] + rotatedX,
                                                                              "y": ball_pos["y"] + rotatedY})

        return leftSpeed, rightSpeed

    def run(self):

        if 'B' in self.name:
            self.ENEMY_ROBOT_NAMES = ["Y1", "Y2", "Y3"]
        else:
            self.ENEMY_ROBOT_NAMES = ["B1", "B2", "B3"]

        while self.robot.step(rcj_soccer_robot.TIME_STEP) != -1:
            if self.is_new_data():
                data = utils.normalisePositions(self.get_new_data(),self.name)
                # data = self.get_new_data()

                # Get the position of our robot
                robot_pos = data[self.name]
                # Get the position of the ball
                ball_pos = data['ball']
                
                #keeper positions
                keeper_pos_x = -0.7
                center_keeper_pos_x = -0.565
                striker_pos_x = -0.1
                striker_pos_y = 0
                keeper_pos_y_left = 0.35
                keeper_pos_y_right = -0.35

                left_side_keeper_pos_y = 0.365
                right_side_keeper_pos_y = -0.365

                pos_before_center_ball_x = -0.75
                pos_before_center_ball_y = 0

                #ball distance
                center_ball_distance_x = ball_pos["x"] - coords.center_pos["x"]
                center_ball_distance_y = ball_pos["y"] - coords.center_pos["y"]

                ball_distance_to_goal_x = ball_pos["x"] - coords.own_goal_pos["x"]
                robot_distance_to_goal_x = robot_pos["x"] - coords.own_goal_pos["x"]

                #extras
                comingball_pos_x = ball_pos["x"]
                comingball_pos_y = ball_pos["y"]

                comingball_pos_x_one = coords.own_goal_pos["x"] - ball_pos["x"]
                comingball_pos_x_two = 0.5 * comingball_pos_x_one

                goalball_pos_x = coords.own_goal_pos["x"] - comingball_pos_x_two
                goalball_pos_y = 0.5 * ball_pos["y"]

                goalball_pos_y_right = ball_pos["y"] - keeper_pos_y_right
                goalball_pos_y_left = ball_pos["y"] - keeper_pos_y_left

        ############
                

                leftSpeed = 0
                rightSpeed = 0
                isRobot1AtBall = utils.isAtGoal(data[self.ENEMY_ROBOT_NAMES[0]],{"x": 0, "y": 0}, maxDistance=0.2)
                isRobot2AtBall = utils.isAtGoal(data[self.ENEMY_ROBOT_NAMES[1]],{"x": 0, "y": 0}, maxDistance=0.2)
                isRobot3AtBall = utils.isAtGoal(data[self.ENEMY_ROBOT_NAMES[2]],{"x": 0, "y": 0}, maxDistance=0.2)

                if (-0.05 < center_ball_distance_x < 0.05 and -0.05 < center_ball_distance_y < 0.05) and not(isRobot1AtBall or isRobot2AtBall or isRobot3AtBall):
                    leftSpeed, rightSpeed = self.attack(robot_pos, ball_pos)
                elif ball_pos["x"] >= -0.0005:
                    leftSpeed, rightSpeed = utils.driveToCoords(robot_pos, x = center_keeper_pos_x, y =  pos_before_center_ball_y)
                elif ball_pos["y"] <= -0.45 and ball_pos["x"] < -0.0005 and ball_pos["x"] > -0.475:
                    leftSpeed, rightSpeed = utils.driveToCoords(robot_pos,x = center_keeper_pos_x, y = goalball_pos_y_right)
                elif ball_pos["y"] >= 0.45 and ball_pos["x"] < -0.0005 and ball_pos["x"] > -0.475:
                    leftSpeed, rightSpeed = utils.driveToCoords(robot_pos,x = center_keeper_pos_x, y = goalball_pos_y_left)
                elif ball_pos["x"] <= -0.0005 and ball_pos["x"] > -0.58 and ball_pos["y"] < 0.45 and ball_pos["y"] > -0.45:
                    leftSpeed, rightSpeed = utils.driveToCoords(robot_pos,x = center_keeper_pos_x, y = ball_pos["y"])
                elif ball_pos["x"] < -0.58 and ball_pos["y"] < 0.5 and ball_pos["y"] > -0.5:
                    leftSpeed, rightSpeed = utils.driveToCoords(robot_pos,x = keeper_pos_x, y = ball_pos["y"])

                elif ball_pos["x"] < -0.475 and ball_pos["y"] < -0.5:
                    leftSpeed, rightSpeed = utils.driveToCoords(robot_pos,x = ball_pos["x"], y = right_side_keeper_pos_y)
                elif ball_pos["x"] < -0.475 and ball_pos["y"] > 0.5:
                    leftSpeed, rightSpeed = utils.driveToCoords(robot_pos,x = ball_pos["x"], y = left_side_keeper_pos_y)

                elif ball_distance_to_goal_x < robot_distance_to_goal_x:
                    leftSpeed, rightSpeed = self.block_attack(robot_pos,ball_pos)
                    
                if ball_pos["x"] > 0.35 and ball_pos["y"] > 0.35 and not(isRobot1AtBall or isRobot2AtBall or isRobot3AtBall):
                    leftSpeed, rightSpeed = self.attack(robot_pos, ball_pos)
                elif ball_pos["x"] > 0.35 and ball_pos["y"] <-0.35 and not(isRobot1AtBall or isRobot2AtBall or isRobot3AtBall):
                    leftSpeed, rightSpeed = self.attack(robot_pos, ball_pos)

                #####
                if ball_pos["x"] < -0.675 and ball_pos["y"] < 0.5 and ball_pos["y"] > -0.5 and utils.isAtGoal(robot_pos, ball_pos, maxDistance = 0.1):
                    print("ich bin drinjadksfhdsjklfahdf")
                    angle = math.atan2(
                        ball_pos['y'] - robot_pos['y'],
                        ball_pos['x'] - robot_pos['x'],
                    )

                    if angle < 0: angle += math.pi * 2
                    
                    # calculate difference between current angle and goal angle
                    ball_goal_angle_diff = angle - robot_pos['orientation']

                    if ball_goal_angle_diff > math.pi: ball_goal_angle_diff -= 2 * math.pi
                    if ball_goal_angle_diff < -math.pi:ball_goal_angle_diff += 2 * math.pi

                    # convert ball_goal_angle_diff to degrees
                    ball_goal_angle_diff = math.degrees(ball_goal_angle_diff)

                    # choose direction in which the robot is driving: 1 -> forwards, -1 -> backwards
                    direction = -1
                    if abs(ball_goal_angle_diff) > 90:
                        direction = 1
                    leftSpeed, rightSpeed = direction, direction


                
                #####

                # Set the speed to motors
                self.left_motor.setVelocity(leftSpeed * self.VELOCITY_MULTIPLIER)
                self.right_motor.setVelocity(rightSpeed * self.VELOCITY_MULTIPLIER)

my_robot = MyRobot()
my_robot.run()