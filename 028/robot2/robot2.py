from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP
import utils

import math
# You can also import scripts that you put into the folder with controller


class MyRobot(RCJSoccerRobot):
    def run(self):
        while self.robot.step(TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()

                # Get the position of our robot
                robot_pos = data[self.name]
                
                if self.name == 'B1'or self.name == 'B2' or self.name == 'B3':
                    print('Equipo Azul' )
                    Neu_posx = .1
                    Neu_posy = 0
                else:
                    print('Equipo Amarillo' )
                    Neu_posx = -.1
                    Neu_posy = 0
                # Get the position of the ball
                ball_pos = data['ball']

                ball_angle, robot_angle = self.get_angles(ball_pos, robot_pos)
                
                # Compute the speed for motors
                if ball_angle < 0:
                    ball_angle += 360
                direction = utils.get_direction(ball_angle)
                
                dist2 = utils.get_dist2(ball_pos, robot_pos)
                #dist1=  math.sqrt((ball_pos['y'] - robot_pos['y'])*(ball_pos['y'] - robot_pos['y'])+(ball_pos['x'] - robot_pos['x'])*(ball_pos['x'] - robot_pos['x']))
                # If the robot has the ball right in front of it, go forward,
                # rotate otherwise
                
                if dist2<.46:
                    if direction == 0: 
                        diff=ball_angle
                        if diff > 180:
                            diff=diff-360
                            left_speed2 = -10-(diff*.6)
                            right_speed2 = -10
                            left_speed= left_speed2
                            right_speed =right_speed2
                            #print('dist2:', dist2, 'left_speed2:', left_speed2, 'right_speed2 :', right_speed2 )
    
                        else:
                            left_speed2 = -10
                            right_speed2 = -10+(diff*.6)
                            left_speed= left_speed2
                            right_speed =right_speed2
                            #print('dist2:', dist2,'ball_angle', ball_angle, 'left_speed2:', left_speed2, 'right_speed2 :', right_speed2 )
    
                    else:
                        left_speed = direction * 10
                        right_speed = direction * -10
                else:#enviar al robot a la xzona neutra si la pelota no esta en el rango
                     
                     NeuZone_angle = self.get_NZangles(robot_pos, Neu_posx, Neu_posy)
                     direction2 = utils.get_direction(NeuZone_angle)
                     #print('zona neutra', 'NeuAngle:', NeuZone_angle,'dir2:', direction2)
                     if direction2 == 0: 
                          left_speed= -10
                          right_speed =-10
                     else:                           
                          left_speed= direction2*10
                          right_speed =direction2*-10

                # Set the speed to motors
                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)


my_robot = MyRobot()
my_robot.run()
