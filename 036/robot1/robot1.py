import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
sys.path.append('/app/controllers')

# rcj_soccer_player controller - ROBOT B1

# Feel free to import built-in libraries
import math

# You can also import scripts that you put into the folder with controller
from team_036_libraries.robot1 import rcj_soccer_robot
from team_036_libraries.robot1 import utils

#team = "BLUE"

class MyRobot(rcj_soccer_robot.RCJSoccerRobot):
    def run(self):
        #detect which team the robot is on
        if self.name[0] == "B":
            team = "BLUE"
        else:
            team = "YELLOW"
        # initialize variables
        frameCount = 0
        recentPos = {"x": 0, "y": 0} #some default original value, gets replaced later
        robot_movement = 0
        while self.robot.step(rcj_soccer_robot.TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()

                frameCount += 1

                # Get the position of our robot
                robot_pos = data[self.name]
                # Get the position of the ball
                ball_pos = data['ball']

                # for the vector (y is equal to x on a normal plane)
                x_pos = ball_pos.get('x') - robot_pos.get('x')
                y_pos = ball_pos.get('y') - robot_pos.get('y')
                # new x and y posititons for the ball
                newXPos = ball_pos.get('x')
                newYPos = ball_pos.get('y')

                #calculate movement of robot from 10 frames ago
                #skip the first frame bc no previous frame to go off of
                #only check/update movement every 10 frames
                if frameCount > 10 and frameCount % 10 == 0:
                    robot_movement = math.sqrt((recentPos["x"] - robot_pos["x"])**2
                                 + (recentPos["y"] - robot_pos["y"])**2)
                    #print("b1 movement " + str(robot_movement))
                    #print("b1 recent pos " + str(recentPos))
                    #print("b1 current pos " + str(robot_pos))

                # Get angle between the robot and the ball
                # and between the robot and the north
                ball_angle, robot_angle = self.get_angles(ball_pos, robot_pos)
                #print("ball_pos " + str(ball_pos))
                #print("robot_pos " + str(robot_pos))
                #print("ball_angle " + str(ball_angle))
                #print("robot_angle " + str(robot_angle))
                #print()

                # Compute the speed for motors
                direction = utils.get_direction(ball_angle)
                #print("direction: " + str(direction))

                #then if it's farther than some amount then do the default of going towards the ball
                #and if it's closer, try to get behind the ball facing the opponent's goal

                #uses distance equation to calculate distance between ball and robot
                dist = math.sqrt((ball_pos["x"] - robot_pos["x"])**2
                                 + (ball_pos["y"] - robot_pos["y"])**2)
                #print("b1 dist " + str(dist))

                #if robot isn't moving and isn't super close to the ball, probably stuck in clump and
                # should try to get unstuck by backing out
                if robot_movement < 0.017 and frameCount > 70 and dist > .1:
                    #print("b1 do ma lil dancey dance?")
                    if 0.005 < robot_movement < 0.017:
                        #reverse out
                        left_speed = 5
                        right_speed = 5
                    else:
                        #if not moving at ALL, might be stuck on wall, curve out
                        left_speed = -3
                        right_speed = 5

                    # Set the speed to motors
                    self.left_motor.setVelocity(left_speed)
                    self.right_motor.setVelocity(right_speed)

                #if robot is not close to the ball, go toward it
                elif dist > .15:
                    # If the robot has the ball right in front of it, go forward,
                    # rotate otherwise
                    if direction == 0:
                        left_speed = -9 #-5
                        right_speed = -9 #-5
                    else:
                        left_speed = direction * 4
                        right_speed = direction * -4

                    # Set the speed to motors
                    self.left_motor.setVelocity(left_speed)
                    self.right_motor.setVelocity(right_speed)

                #Emma's code
                elif .07 < dist < 0.15:
                    # tries to get the robot to move around the ball if the ball is closer to the goal
                    # may need to check some of the calculations with this one
                    if team == 'BLUE':  # instructions for blue
                        if x_pos > 0 and y_pos > 0:
                            newXPos += 0.1
                            newYPos -= 0.2
                            #print("don't kick less than")
                        elif x_pos < 0 and y_pos < 0:
                            newXPos += 0.1
                            newYPos += 0.1
                            #print("don't kick greater than")
                        elif x_pos > 0 and y_pos < 0:
                            newXPos += 0.1
                            newYPos += 0.2
                        elif x_pos < 0 and y_pos > 0:
                            newXPos += 0.1
                            newYPos += 0.1

                    elif team == 'YELLOW':  # could possibly just do else as well
                        if x_pos > 0 and y_pos > 0:
                            newXPos -= 0.1
                            newYPos -= 0.1
                            #print("don't kick less than")
                        elif x_pos < 0 and y_pos < 0:
                            newXPos -= 0.1
                            newYPos += 0.2
                            #print("don't kick greater than")
                        elif x_pos > 0 and y_pos < 0:
                            newXPos -= 0.1
                            newYPos -= 0.1
                        elif x_pos < 0 and y_pos > 0:
                            newXPos -= 0.1
                            newYPos -= 0.2

                    #print(ball_pos)
                    # changes ball_pos variable in order to change the ball_angle (and thus different directions)
                    ball_pos = {'x': newXPos, 'y': newYPos}
                    #print("X pos: " + str(newXPos) + " Y pos: " + str(newYPos))

                    # Get angle between the robot and the ball
                    # and between the robot and the north
                    ball_angle, robot_angle = self.get_angles(ball_pos, robot_pos)

                    # Compute the speed for motors
                    direction = utils.get_direction(ball_angle)

                    # If the robot has the ball right in front of it, go forward,
                    # rotate otherwise
                    if direction == 0:
                        left_speed = -7
                        right_speed = -7
                    else:
                        left_speed = direction * 5
                        right_speed = direction * -5

                    # if close:
                    #     left_speed = 0
                    #     right_speed = 0

                    # Set the speed to motors
                    self.left_motor.setVelocity(left_speed)
                    self.right_motor.setVelocity(right_speed)


                #if robot is almost touching the ball (<.07 away) move toward the goal
                else:
                    #print("b1 goal bound wheee")
                    if team == "BLUE":
                        goal_pos = {'x': 0.0, 'y': -0.75} #position of yellow/scoring goal
                    else:
                        goal_pos = {'x': 0.0, 'y': 0.75} #position of blue/scoring goal

                    goal_angle, robo_angle = self.get_angles(goal_pos, robot_pos)
                    direction = utils.get_direction(goal_angle)

                    if direction == 0:
                        left_speed = -9
                        right_speed = -9
                    else:
                        left_speed = direction * 4
                        right_speed = direction * -4

                    # Set the speed to motors
                    self.left_motor.setVelocity(left_speed)
                    self.right_motor.setVelocity(right_speed)

                if frameCount % 10 == 0:
                    recentPos = robot_pos
                    #print("b1 recentPos" + str(recentPos))



#if the ball is behind you during the going toward the goal part, go back to going toward it?


my_robot = MyRobot()
my_robot.run()
