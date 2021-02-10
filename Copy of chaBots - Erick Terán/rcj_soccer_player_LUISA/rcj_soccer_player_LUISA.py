# rcj_soccer_player controller - ROBOT B2

###### REQUIRED in order to import files from B1 controller
import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
# You can now import scripts that you put into the folder with your
# robot B1 controller
from rcj_soccer_player_KAREN import rcj_soccer_robot, utils
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

                if self.color == -1:
                    robot_pos['orientation'] += math.pi

                if robot_pos['orientation'] > 2 * math.pi:
                    robot_pos['orientation'] -= 2 * math.pi

                # Get the position of the ball
                ball_pos = data['ball']
                ball_pos['y'] = min(0.55, max(ball_pos['y'], -0.55)) * self.color
                ball_pos['x'] = min(0.7, max(ball_pos['x'], -0.75)) * self.color
                b_y = ball_pos['y']
                b_x = ball_pos['x']

                if b_x < 0.6 and b_y < 0:
                    new_setpoint = ball_pos
                    
                else:

                    new_setpoint = {'x': b_x, 'y': -0.4}

                    if b_x < -0.6:
                        new_setpoint = ball_pos

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

        #Goal line
        #0.6
        goal_line = 0.45
        goal_line_opponent = 0.6
        goal_post = 0.3

        max_x = 1.98 #0.6
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
        kd_y = 1
        correction_y = 0
        error_y = 0

        distance = utils.get_distance(actualPoint, setPoint)

        if ballPos['x'] >= goal_line or ballPos['x'] <= -goal_line_opponent:

            #print("Pelota en penalty area")

            if ballPos['x'] <= -goal_line_opponent:

                if ballPos['y'] <= goal_post and ballPos['y'] >= -goal_post:
                    
                    #print(f"Rematar {self.angle_filter(pointAngle)}")

                    error_y = pointAngle

                else:

                    #print("Reposicionar, B1")

                    distance = goal_line_opponent + robotPos['x']
                    error_y = robotAngle

                    if self.color == -1:
                        error_y += 180

                    if distance <= 0.05 and distance >= -0.05:
                        
                        #print("Sigo de mi lado 1")
                        
                        distance = 0.3 + robotPos['y']
                        error_y -= 90

                        if ballPos['x'] < -0.6 and ballPos['y'] > 0:

                            distance = (ballPos['y'] - robotPos['y']) * utils.get_sign(-ballPos['y'])

            else:

                #print("No seguir")
    
                distance = -goal_line + robotPos['x']
                
                error_y = robotAngle

                if self.color == -1:
                    error_y += 180

        elif distance <= 0.06 and self.time_limit == 0:
            
            #print("Ya la tengo!!!")

            error_y = pointAngle

            if utils.get_sign(robotPos['x']) == -1:
                self.time_limit = timer + 0.4

        elif self.time_limit >= timer:

            left_velocity = -8 - 2 * utils.get_sign(error_y)
            right_velocity = -8 + 2 * utils.get_sign(error_y)

            velocity = [left_velocity, right_velocity]

            return velocity

        else:
        
            #print("No la tengo :(")
            
            error_y = pointAngle
            self.time_limit = 0

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