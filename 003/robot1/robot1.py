import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
sys.path.append('/app/controllers')

# rcj_soccer_player controller - ROBOT B1

# Feel free to import built-in libraries
import math

# You can also import scripts that you put into the folder with controller
from team_003_libraries.robot1.rcj_soccer_robot import RCJSoccerRobot, TIME_STEP
from team_003_libraries.robot1 import utils

class MyRobot(RCJSoccerRobot):

    VELOCITY_MULTIPLIER = 10
    inPosition = False

    ENEMY_ROBOT_NAMES = []
    def run(self):
        if 'B' in self.name:
            self.ENEMY_ROBOT_NAMES = ["Y1", "Y2", "Y3"]
        else:
            self.ENEMY_ROBOT_NAMES = ["B1", "B2", "B3"]
        current_robot_goal_name = "B1"
        last_choosen_time = -100
        while self.robot.step(TIME_STEP) != -1:
            if self.is_new_data():
                data = utils.normalisePositions(self.get_new_data(), self.name)
                # Get the position of our robot
                robot_pos = data[self.name]

                # Get the position of the ball
                ball_pos = data['ball']

                if self.robot.getTime() > last_choosen_time + 10 or data[current_robot_goal_name]["x"] < -0.3:
                    print("Choosing robot")
                    last_choosen_time = self.robot.getTime()
                    current_robot_goal_name = self.chooseRobotToBlock(data)
                    print("Choosing finished")

                
                leftSpeed, rightSpeed = utils.driveToCoords(
                    data[self.name], data[current_robot_goal_name])

                if utils.isAtGoal(robot_pos, data[current_robot_goal_name], maxDistance = 0.1):
                    print("ich bin drin")
                    angle = math.atan2(
                        data[current_robot_goal_name]['y'] - robot_pos['y'],
                        data[current_robot_goal_name]['x'] - robot_pos['x'],
                    )

                    if angle < 0: angle += math.pi * 2

                    # calculate difference between current angle and goal angle
                    robot_goal_angle_diff = angle - robot_pos['orientation']

                    if robot_goal_angle_diff > math.pi: robot_goal_angle_diff -= 2 * math.pi
                    if robot_goal_angle_diff < -math.pi:robot_goal_angle_diff += 2 * math.pi

                    # convert robot_goal_angle_diff to degrees
                    robot_goal_angle_diff = math.degrees(robot_goal_angle_diff)

                    # choose direction in which the robot is driving: 1 -> forwards, -1 -> backwards
                    direction = -1
                    if abs(robot_goal_angle_diff) > 90:
                        direction = 1
                        leftSpeed, rightSpeed = direction, direction

                # drive to middle if robot is standing there
                isRobot1AtBall = utils.isAtGoal(data[self.ENEMY_ROBOT_NAMES[0]],{"x": 0, "y": 0}, maxDistance=0.2)
                isRobot2AtBall = utils.isAtGoal(data[self.ENEMY_ROBOT_NAMES[1]],{"x": 0, "y": 0}, maxDistance=0.2)
                isRobot3AtBall = utils.isAtGoal(data[self.ENEMY_ROBOT_NAMES[2]],{"x": 0, "y": 0}, maxDistance=0.2)

                #if ball_pos["x"] < -0.35 and abs(ball_pos["y"]) > 0.35 and (isRobot1AtBall or isRobot2AtBall or isRobot3AtBall):
                #    leftSpeed, rightSpeed = utils.driveToCoords(robot_pos, data[self.getClosestRobotToPosition(data, {"x": 0, "y": 0})])

                self.left_motor.setVelocity(leftSpeed * self.VELOCITY_MULTIPLIER)
                self.right_motor.setVelocity(rightSpeed * self.VELOCITY_MULTIPLIER)
                #c.sendPoint("position_b1", (0,0,255), data["B1"])

    def getClosestRobotToPosition(self, data, position):
        closest_distance = 100
        closest_robot_name = ""
        for name in self.ENEMY_ROBOT_NAMES:
            distance = utils.getDistanceBetweenPoints(data[name], position)
            if distance < closest_distance:
                closest_distance = distance
                closest_robot_name = name
        return closest_robot_name

    def chooseRobotToBlock(self, data):
        
        heighestXCoord = -100
        robot_to_block_name = ""
        for name in self.ENEMY_ROBOT_NAMES:
            if data[name]["x"] > heighestXCoord:
                heighestXCoord = data[name]["x"]
                robot_to_block_name = name
        print("Robot name: " + robot_to_block_name)
        return robot_to_block_name

my_robot = MyRobot()
my_robot.run()
