team = 'BLUE'
# goalie bot
# rcj_soccer_player controller - ROBOT B2

###### REQUIRED in order to import files from B1 controller
import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
# You can now import scripts that you put into the folder with your
# robot B1 controller
if team == 'BLUE':
    from rcj_soccer_player_b1 import rcj_soccer_robot, utils
else:
    from rcj_soccer_player_y1 import rcj_soccer_robot, utils
######

# Feel free to import built-in libraries
import math

class MyRobot(rcj_soccer_robot.RCJSoccerRobot):
    def attackOrDefend(self):
        data = self.get_new_data()

        ball_pos=data['ball']

        if ball_pos['x']<=-0.2:
            return False
            # Go attack
        if ball_pos['x']>=-0.2:
            return True
            # Go defend

    def turnToPoint(self, pt, data):
        # pt = [x,y] (list of integers)
        # print('In Go to: ')
        dict = {}
        dict['x']=pt[0]
        dict['y']=pt[1]

        botInfo = data[self.name]
        dx=float(pt[0]-botInfo['x'])
        dy=float(pt[1]-botInfo['y'])

        # heading = botInfo['orientation']
        # angle = math.radians(math.atan(dx/dy))
        # angle between robot and point

        angle, robot_angle = self.get_angles(dict, botInfo)
        # print("angle between robot and point: ", angle)

        if angle>=180:
            return True
            # self.left_motor.setVelocity(-10)
            # self.right_motor.setVelocity(10)
        if angle<=180:
            return False
            # self.left_motor.setVelocity(10)
            # self.right_motor.setVelocity(-10)





    def run(self):
        frame = 0
        currentRotation=-1
        previousAngle=-1
        facing = False

        x = 1

        while self.robot.step(rcj_soccer_robot.TIME_STEP) != -1:
            if self.is_new_data():

                frame += 1

                data = self.get_new_data()
                # print('data: ', data)
                # Get the position of our robot
                robot_pos = data[self.name]
                # Get the position of the ball
                ball_pos = data['ball']

                # Get angle between the robot and the ball
                # and between the robot and the north
                ball_angle, robot_angle = self.get_angles(ball_pos, robot_pos)
                #
                # toTurn = self.turnToPoint([0.5,0.5],data)
                # angle, robot_angle = self.get_angles(ball_pos, data[self.name])
                #
                # if facing==False:
                #     self.left_motor.setVelocity(10)
                #     self.right_motor.setVelocity(-10)
                #     if abs(360-angle)>angle:
                #         self.left_motor.setVelocity(10)
                #         self.right_motor.setVelocity(-10)
                #     if angle<360-angle:
                #         self.left_motor.setVelocity(-10)
                #         self.right_motor.setVelocity(10)
                # if abs(angle)<=(12):
                #     self.left_motor.setVelocity(-10)
                #     self.right_motor.setVelocity(-10)
                #     facing=True
                #
                # if angle>=40:
                #     facing=False
                # previousAngle=ball_angle

                # if facing==True:
                #     self.left_motor.setVelocity(0)
                #     self.right_motor.setVelocity(0)


                # print("facing: ",facing)
                # if toTurn:
                #     self.left_motor.setVelocity(-10)
                #     self.right_motor.setVelocity(10)
                # if not toTurn:
                #     self.left_motor.setVelocity(10)
                #     self.right_motor.setVelocity(-10)

            #     print("ball angle: ", ball_angle)

                # print("robot angle: ", robot_angle)

                # Compute the speed for motors
                direction = utils.get_direction(ball_angle)

                # If the robot has the ball right in front of it, go forward,
                # # rotate otherwise
                if direction == 0:
                    left_speed = -10
                    right_speed = -10
                else:
                    left_speed = direction * 4
                    right_speed = direction * -4

                # Set the speed to motors
                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)
                frame += 1

                #if


my_robot = MyRobot()
my_robot.run()
