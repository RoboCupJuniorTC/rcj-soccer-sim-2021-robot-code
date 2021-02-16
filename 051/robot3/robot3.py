# rcj_soccer_player controller - ROBOT B3

###### REQUIRED in order to import files from B1 controller
import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
# You can now import scripts that you put into the folder with your
# robot B1 controller
from team_051_libraries.robot1 import rcj_soccer_robot, utils
######

# Feel free to import built-in libraries
import math
import time

class MyRobot(rcj_soccer_robot.RCJSoccerRobot):
    def run(self):

        while self.robot.step(rcj_soccer_robot.TIME_STEP) != -1:
            if self.is_new_data():
                
                data = self.get_new_data()
                
                # Get the position of our robot
                robot_pos = data[self.name]
                robot_pos['x'] *= self.color
                robot_pos['y'] *= self.color
                # Get the position of the ball
                ball_pos = data['ball']
                ball_pos['x'] = min(0.75, max(ball_pos['x'], -0.7)) * self.color
                ball_pos['y'] = min(0.57, max(ball_pos['y'], -0.57)) * self.color
                b_y = ball_pos['y']
                b_x = ball_pos['x']
                # Get angle between the robot and the ball
                # and between the robot and the north
            
                if robot_pos['x'] < 0.5 :
                    #print("Estoy afuera")
                    new_setpoint = {'x': 0.65, 'y': b_y}

                else:
                    new_setpoint = ball_pos #{'x': 0.6, 'y': b_y}

                        
                point_angle, robot_angle = self.get_angles(new_setpoint, robot_pos)
        
                robot_angle = math.degrees(robot_angle) + (90 * self.color)    

                if robot_angle > 360:
                    robot_angle -= 360

                if(self.initial):

                    self.initial_time = time.time()
                    self.initial = False

                timer = time.time() - self.initial_time
                speed = self.goTo(new_setpoint, robot_pos, point_angle, ball_pos, robot_angle, robot_pos, timer) 
                self.left_motor.setVelocity(min(10.0, max(speed[0], -10.0)))
                self.right_motor.setVelocity(min(10.0, max(speed[1], -10.0)))

    def goTo(self, setPoint, actualPoint, pointAngle, ballPos, robotAngle, robotPos, timer):

        goal_line = 0.55

        max_x = 0.4 #1.98 #0.6
        max_y = 180
        porteria = 0.7

        left_velocity = 0
        right_velocity = 0

        #Translation
        kp_x = 1.2
        kd_x = 1
        correction_x = 0
        error_x = 0

        #Rotation
        kp_y = 3
        kd_y = 1.2
        correction_y = 0
        error_y = 0

        distance = utils.get_distance(actualPoint, setPoint)

        if ballPos['x'] < -0.75:

            left_velocity = -10
            right_velocity = 10

            velocity = [left_velocity, right_velocity]

            return velocity            

        if ballPos['x'] < goal_line:

            distance = -goal_line + robotPos['x'] #abs
            error_y = robotAngle

            if distance <= 0.01 and distance >= -0.01:

                distance = (ballPos['y'] - robotPos['y']) #* utils.get_sign(-ballPos['y']) #goal_line + robotPos['x'] #abs
                error_y = robotAngle - 90

        else:

            if self.color == -1:

                if ballPos['y'] > robotPos['y']:
                    error_y = pointAngle - 180

                else:
                    
                    distance *= -1
                    error_y = pointAngle

            else:
                if ballPos['y'] > robotPos['y']:
                    error_y = pointAngle

                else:
                    
                    distance *= -1
                    error_y = pointAngle - 180


        #Translation
        error_x = distance
        p_x = kp_x * (error_x / max_x * 10)

        #Rotation
        error_y = utils.angle_filter(error_y)
        p_y = kp_y * (error_y / max_y * 10)

        #Prioritize rotation over translation
        if error_y <= 20 and error_y >= -20:
            correction_x = min(10.0, max(p_x, 8)) * utils.get_sign(p_x) * -1
        
        correction_y = p_y

        #Calculate the velocities for each motors
        left_velocity = correction_x - correction_y
        right_velocity = correction_x + correction_y

        velocity = [left_velocity, right_velocity]

        return velocity
                
my_robot = MyRobot()
my_robot.run()
