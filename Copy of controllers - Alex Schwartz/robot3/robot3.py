# rcj_soccer_player controller - ROBOT B3

###### REQUIRED in order to import files from B1 controller
import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
# You can now import scripts that you put into the folder with your
# robot B1 controller
from rcj_soccer_player_b1 import rcj_soccer_robot, utils
######

# Feel free to import built-in libraries
import math

class MyRobot(rcj_soccer_robot.RCJSoccerRobot):
    def run(self):
        i = 0
        pastPos = [0.0, 0.0] #must be run before the loop starts
        pastvel = [0.0, 0.0]
        ballvel = [0.0, 0.0]
        sameOrientation = 0
        time = 0
        speed = .0128 #hardcoded max speed per tick
        rotationalSpeed = .22 #hardcode average rotational speed per tick (in radians)
        forward = False #range = .5 (fairly far)
        defender = True #range = .1 (pretty close)
        goalie = False #range = .05 (basically in contact)
                
        yellow = False
        blue = False
        if (not (forward ^ defender ^ goalie)):
            print ("preset values error")
            x = 1/0
        
        if forward:#All the initial targets, most important for goalie
            sameTarget = [0.0, 0.0]
        if defender:
            if yellow:
                sameTarget = [-.25, 0.0]
            else:
                sameTarget = [0.25, 0.0]    
        else:
            if yellow:
                sameTarget = [-.55, 0.01]
            else:
                sameTarget = [0.55, 0.01]
        
        while self.robot.step(rcj_soccer_robot.TIME_STEP) != -1:
            if self.is_new_data():
                def forwardMovement(ballPos, ballvel, botPos):
                    tick = timeToCollision(ballvel, botPos)
                    #print ("Time to collision = ", tick)
                    if tick == -1:
                        if (blue):
                            return [[-0.25, 0.0], [-0.25, 0.0], [-0.25, 0.0]] #if the bot cannot reach the ball in time, predict side in 60 ticks, move forward center
                        return [[0.25, 0.0], [0.25, 0.0], [0.25, 0.0]] #theres a more efficient way to do the color thing but I cba
                    else:
                        futureBallPos = ballPos
                        #print("Ball Velocity for prediction = ", ballvel)
                        futureBallPos[0] = ballvel[0] * tick + ballPos[0]
                        futureBallPos[1] = ballvel[1] * tick + ballPos[1]
                        futureBallPos = bounce(futureBallPos)
                        #print ("In ", tick, " ticks the ball will be at ", futureBallPos)
                    return calColinear(futureBallPos)

                def defenderMovement(ballPos, ballvel, botPos):
                    tick = timeToCollision(ballvel, botPos)
                    #print ("Time to collision = ", tick)
                    if tick == -1 :
                        if blue:
                            return [0.25, 0.0]  # if the bot cannot reach the ball in time, predict side in 60 ticks, move center back
                        return [-.25, 0.0]
                    else:
                        futureBallPos = ballPos
                        futureBallPos[0] = ballvel[0] * tick + ballPos[0]
                        futureBallPos[1] = ballvel[1] * tick + ballPos[1]
                        futureBallPos = bounce(futureBallPos)
                    return calColinearDef(futureBallPos)
                
                def goalieMovement(ballPos, ballvel, botPos, close):
                    if close:
                        m = ballvel[1]/ballvel[0]
                        im = - 1/m
                        #print ("m =", m, " im = ", im)
                        x = (-im * botPos[0] + botPos[1] + m * ballPos[0] - ballPos[1])/m-im
                        y = m * (x - ballPos[0]) + ballPos[1]
                        return [x,y]
                    else:
                        if blue:
                            x = 0.55
                        else:
                            x = -.55
                    m = ballvel[1]/ballvel[0]
                    y = m * (x - ballPos[0]) + ballPos[1]
                    return [x, y] #target position
                
                def bounce(futureBallPos):
                    if futureBallPos[0] < -.73:
                        futureBallPos[0] = -1.46 - futureBallPos[0] # bounce off the left wall
                    elif futureBallPos[0] > .73:
                        futureBallPos[0] = 1.46 - futureBallPos[0] # bounce off the right wall
                    if futureBallPos[1] < -.62:
                        futureBallPos[1] = -1.24 - futureBallPos[1]  # bounce off the bottom wall
                    elif futureBallPos[1] > .62:
                        futureBallPos[1] = 1.24 - futureBallPos[1]  # bounce off the top wall
                    return futureBallPos
                
                def timeToCollision(ballvel, botPos):
                    #rereun only if vel changes significantly
                    holding = ballvel
                    futurePos = [ballPos[0], ballPos[1]]
                    distance = 0
                    for tick in range(120): #looking 60 ticks ahead
                        futurePos[0] += holding[0]
                        futurePos[1] += holding[1]
                        if math.sqrt((futurePos[0] - botPos[0]) ** 2) + ((futurePos[0] - botPos[0]) ** 2) <= .0128 * tick:
                            return tick
                    return -1 #not within the given number of ticks
                
                def isBallProgressing(ballvel):
                    if (ballvel[0] > 0.01): #0.1 should be altered, its the minimum speed moving right to assume its progressing
                        return True
                    return False
                
                def calColinear(ballPos):
                    # score at (.71, +-.15) & (.71, 0)
                    targetY = [-.15, 0, .15]
                    r = .05 #radius of both robot & ball & some wiggle room
                    targetPos = [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0]]
                
                    if yellow:
                        for i in range(len(targetY)):
                            ratio = math.sqrt(((-.71 - ballPos[0]) ** 2) + ((targetY[i] - ballPos[1]) ** 2)) / r
                            targetPos[i][0] = ballPos[0] + ((ballPos[0] - .71) / ratio)
                            targetPos[i][1] = ballPos[1] + ((ballPos[1] - targetY[i]) / ratio)
                    else:
                        for i in range(len(targetY)):
                            ratio = math.sqrt(((.71 - ballPos[0]) ** 2) + ((targetY[i] - ballPos[1]) ** 2)) / r
                            targetPos[i][0] = ballPos[0] - ((ballPos[0] - .71) / ratio)
                            targetPos[i][1] = ballPos[1] - ((ballPos[1] - targetY[i]) / ratio)
                    return targetPos
                    
                def calColinearDef(ballPos):
                    # score at (.71, +-.15) & (.71, 0)
                    targetY = 0
                    r = .05 #radius of both robot & ball & some wiggle room
                    targetPos = [0.0, 0.0]
                
                    if blue:#flipped for defenders goal
                        ratio = math.sqrt(((-.71 - ballPos[0]) ** 2) + ((targetY - ballPos[1]) ** 2)) / r
                        targetPos[0] = ballPos[0] - ((ballPos[0] - .71) / ratio)
                        targetPos[1] = ballPos[1] - ((ballPos[1] - targetY) / ratio)
                    else: #                       ^ flipped to be on the close side
                        ratio = math.sqrt(((.71 - ballPos[0]) ** 2) + ((targetY - ballPos[1]) ** 2)) / r
                        targetPos[0] = ballPos[0] + ((ballPos[0] - .71) / ratio)
                        targetPos[1] = ballPos[1] + ((ballPos[1] - targetY) / ratio)
                    return targetPos
                
                def inside2pi(difference): #make it inside the +- pi circle
                    if difference < -1 * math.pi:
                        difference += 2 * math.pi
                    elif difference > math.pi:
                        difference -= 2 * math.pi
                    return difference
                    
                def inCone(ballPos, botPos, range):
                    if yellow: #since the y axis is upside-down
                        isAbove = (((-.15 - ballPos[1]) / ( .71-ballPos[0])) * (botPos[0] - ballPos[0]) + ballPos[1]) > botPos[1]
                        isBelow = (((.15 - ballPos[1]) / ( .71-ballPos[0])) * (botPos[0] - ballPos[0]) + ballPos[1]) < botPos[1]
                        farSide = botPos[0] < ballPos[0] #should be nessesary
                    else:
                        isAbove = (((-.15 - ballPos[1]) / (-.71-ballPos[0])) * (botPos[0] - ballPos[0]) + ballPos[1]) > botPos[1]
                        isBelow = ((( .15 - ballPos[1]) / (-.71-ballPos[0])) * (botPos[0] - ballPos[0]) + ballPos[1]) < botPos[1]
                        farSide = botPos[0] > ballPos[0]
                    #checking the inequalities to see if its inline
                    #print("Cone: isAbove ", isAbove, " isBelow ", isBelow, " Farside ", farSide)
                    return (isAbove and isBelow and farSide and math.sqrt((ballPos[0] - botPos[0] )**2 + (ballPos[1] - botPos[1])**2) <= range) #try to score sooner
                
                def driver(botPos, targetPos, orientation, targetOrientation): #! use target orientation
                    if abs(botPos[0] - targetPos[0]) < .01 and abs(botPos[1] - botPos[1]) < .01:
                        #its real close
                        #print("Targeted Direction = ", targetOrientation)
                        direction = targetOrientation
                        if targetPos[1] > botPos[1]:
                            direction -= math.pi
                            #print("direction flipped")
                        direction = inside2pi(direction)
                        #print("Direction = ", direction)
                        difference1 = inside2pi(direction - orientation)
                        difference2 = inside2pi(direction - orientation - math.pi)
                        backwards = False
                        if abs(difference2) < abs(difference1):
                            difference = difference2
                            backwards = True
                        else:
                            difference = difference1
                        #print("difference1 = ", difference1, " Difference2 = ", difference2)
                        #print ("Difference = ", difference, " Backwards = ", backwards)
                        if abs(difference) <= .1:
                            self.left_motor.setVelocity(0)
                            self.right_motor.setVelocity(0)
                            #print("moters 0 0")
                        elif difference > .22:
                            self.left_motor.setVelocity(10)
                            self.right_motor.setVelocity(-10)
                            #print("moters +10 -10")
                        elif difference < -.22:
                            self.left_motor.setVelocity(-10)
                            self.right_motor.setVelocity(10)
                            #print("moters -10 +10")
                        elif difference > .1:
                            self.left_motor.setVelocity(5)
                            self.right_motor.setVelocity(-5)
                        elif difference < -.1:
                            self.left_motor.setVelocity(-5)
                            self.right_motor.setVelocity(5)
                        else:
                            print("error: rotation difference not understood")
                        return
                    else:
                        #print("Targeted Position = ", targetPos)
                        direction = math.atan((targetPos[0] - botPos[0]) / (targetPos[1] - botPos[1]))
                        #print("Arctan of -", botPos[1], " / -", botPos[0], " = ", direction)
                        if targetPos[1] > botPos[1]:
                            direction -= math.pi
                            #print("direction flipped")
                        direction = inside2pi(direction)
                        #print("Direction = ", direction)
                        difference1 = inside2pi(direction - orientation)
                        difference2 = inside2pi(direction - orientation - math.pi)
                        backwards = False
                        if abs(difference2) < abs(difference1):
                            difference = difference2
                            backwards = True
                        else:
                            difference = difference1
                        #print("difference1 = ", difference1, " Difference2 = ", difference2)
                        #print ("Difference = ", difference, " Backwards = ", backwards)
                        if abs(difference) <= .15:
                            if not backwards:
                                self.left_motor.setVelocity(-10)
                                self.right_motor.setVelocity(-10)
                                #print("moters -10 -10")
                            else:
                                self.left_motor.setVelocity(10)
                                self.right_motor.setVelocity(10)
                                #print("moters +10 +10")
                        elif difference > .22:
                            self.left_motor.setVelocity(10)
                            self.right_motor.setVelocity(-10)
                            #print("moters +10 -10")
                        elif difference < -.22:
                            self.left_motor.setVelocity(-10)
                            self.right_motor.setVelocity(10)
                            #print("moters -10 +10")
                        elif difference > .1:
                            self.left_motor.setVelocity(5)
                            self.right_motor.setVelocity(-5)
                        elif difference < -.1:
                            self.left_motor.setVelocity(-5)
                            self.right_motor.setVelocity(5)
                        else:
                            print("error: rotation difference not understood")
                        return
                    
                def score(botPos, ballPos, orientation):
                    #if ball slips out from infront recalculate!!!!!!!!!!!!
                    direction = math.atan((ballPos[0] - botPos[0]) / (ballPos[1] - botPos[1]))
                    #print("Arctan of -", botPos[1], " / -", botPos[0], " = ", direction)
                    if ballPos[1] > botPos[1]:
                        direction -= math.pi
                        #print("direction flipped")
                    direction = inside2pi(direction)
                    #print("Direction = ", direction)
                    difference1 = inside2pi(direction - orientation)
                    difference2 = inside2pi(direction - orientation - math.pi)
                    backwards = False
                    if abs(difference2) < abs(difference1):
                        difference = difference2
                        backwards = True
                    else:
                        difference = difference1
                    #print("difference1 = ", difference1, " Difference2 = ", difference2)
                    #print ("Difference = ", difference, " Backwards = ", backwards)
                    if abs(difference) <= .1:
                        if not backwards:
                            self.left_motor.setVelocity(-10)
                            self.right_motor.setVelocity(-10)
                            #print("moters -10 -10")
                        else:
                            self.left_motor.setVelocity(10)
                            self.right_motor.setVelocity(10)
                            #print("moters +10 +10")
                    elif difference > .22:
                        self.left_motor.setVelocity(10)
                        self.right_motor.setVelocity(-10)
                        #print("moters +10 -10")
                    elif difference < -.22:
                        self.left_motor.setVelocity(-10)
                        self.right_motor.setVelocity(10)
                        #print("moters -10 +10")
                    elif difference > .1:
                        self.left_motor.setVelocity(5)
                        self.right_motor.setVelocity(-5)
                    elif difference < -.1:
                        self.left_motor.setVelocity(-5)
                        self.right_motor.setVelocity(5)
                    else:
                        print("error: rotation difference not understood")
                    return
                
                #Main
                
                ballPos = [0, 0]
                
                targetArray = [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0]]
                ballvel = [0.0, 0.0]
                botPos = [0.0, 0.0]
                data = self.get_new_data()
                robot_pos = data[self.name] # Get the position of our robot
                team = self.team
                if team == 'B':
                    blue = True
                else:
                    yellow = True
                #print (blue, yellow)
                botPos[0] = robot_pos['x']
                botPos[1] = robot_pos['y']
                ball_pos = data['ball'] # Get the position of the ball
                ballPos[0] = ball_pos['x']
                ballPos[1] = ball_pos['y']
                orientation = robot_pos['orientation']#in radians, 0 is down, pi is up, - is clockwise, + is counter-clockwise
                orientation += math.pi #like normal raidans
                orientation = inside2pi(orientation)#I rotated everything, it works, don't fix it
                time += 1
                #print ("orientation = ", orientation)
                #print ("Ball position = ", ballPos)
                #print ("Bot position = ", botPos)
                    
                pastvel[0] = ballvel[0]
                pastvel[1] = ballvel[1]
                
                ballvel[0] = ballPos[0] - pastPos[0]
                ballvel[1] = ballPos[1] - pastPos[1]
                pastPos[0] = ballPos[0]
                pastPos[1] = ballPos[1]
                    
                #print ("Ball velocity = ", ballvel)
                    #rerecord positions
                    
                if forward:
                    if inCone(ballPos, botPos, 1.0): #1.0 range for position
                        #print("trying to score")
                        score(botPos, ballPos, orientation)
                    elif abs(ballPos[0]) < .01 and abs(ballPos[1]) < .01 and ((blue and botPos[0] < 0) or (yellow and botPos[0] > 0)):
                        sameTarget = [0.0, .15] #when the ball respawns and the bot is on the far side
                        sameOrientation = 0
                        driver(botPos, sameTarget, orientation, sameOrientation) 
                    elif abs(ballvel[0] + ballvel[1]) - abs(pastvel[0] + pastvel[1]) < .01: #if no significant vel change
                        #print("new targeting")
                        if yellow:
                            if ballPos[0] > -.35:
                                #print("calculating new line")
                                targetArray = forwardMovement(ballPos, ballvel, botPos)
                                sameTarget = targetArray[1]
                                sameOrientation = 0
                                driver(botPos, targetArray[1], orientation, sameOrientation) # randomize the 1 to randomize the shot location, has to be held for many ticks, can be intelligently chosen (order is top to bottom)
                            else:
                                #print("returning to forward center")
                                sameTarget = [0.45, 0.0]
                                if ballPos[0] > 0:#or back center
                                    sameTarget[0] = sameTarget[0] - .65
                                sameOrientation = 0
                                driver(botPos, sameTarget, orientation, sameOrientation)
                        else:
                            if ballPos[0] < .35:
                                #print("calculating new line")
                                targetArray = forwardMovement(ballPos, ballvel, botPos)
                                sameTarget = targetArray[1]
                                sameOrientation = 0 #that angle should be specified
                                driver(botPos, sameTarget, orientation, sameOrientation) 
                            else:
                                #print("returning to forward center")
                                sameTarget = [-0.45, 0.0]
                                if ballPos[0] < 0:#or back center
                                    sameTarget[0] = sameTarget[0] + .65
                                sameOrientation = 0
                                driver(botPos, sameTarget, orientation, sameOrientation)
                    else:
                        #print("same target")
                        driver(botPos, sameTarget, orientation, sameOrientation)
                        
                        
                elif defender:
                    if inCone(ballPos, botPos, .3): #1.0 range for position
                        #print("trying to score")
                        score(botPos, ballPos, orientation)
                    elif abs(ballvel[0] - pastvel[0]) + abs(ballvel[1] - pastvel[1]) < .01: #redirected
                        #print("doing the same thing")
                        driver(botPos, sameTarget, orientation, sameOrientation)
                    elif (blue and ballvel[0] > -.01) or (yellow and ballvel[0] < .01): #approching
                        if (blue and ballPos[0] <= 0)  or (yellow and ballPos[0] >= 0):#far side
                            #print("returning to default position")
                            sameTarget = [0.25, 0.0]
                            if yellow:
                                sameTarget[0] = sameTarget[0] * -1
                            sameOrientation = 0
                            driver(botPos, sameTarget, orientation, sameOrientation)
                        else:#close and approching
                            #print("lining up defense")
                            targetArray = defenderMovement(ballPos, ballvel, botPos)
                            sameTarget = targetArray
                            sameOrientation = 0 #that angle should be specified
                            driver(botPos, sameTarget, orientation, sameOrientation) 
                    else: 
                        #print("returning to default position")
                        sameTarget = [0.25, 0.0]
                        if blue:
                            sameTarget[0] = sameTarget[0] * -1
                        sameOrientation = 0
                        driver(botPos, sameTarget, orientation, sameOrientation)
                            
                elif goalie:#THIS DOESN"T CHECK IF ITS GOING TO SCORE
                    if (ballPos[0] > 0 and ballvel[0] > 0 and yellow) or (ballPos[0] < 0 and ballvel[0] < 0 and blue):
                        #print("returning to the default positions")
                        #print(time)
                        if yellow:
                            if time % 200 <= 100:#can I call time step in B2 or B3
                                driver(botPos, [-.55, 0.05], orientation, math.pi/2)
                            else:
                                driver(botPos, [-.55, -0.05], orientation, math.pi/2)
                        else:
                            if TIME_STEP % 30 <= 15:
                                driver(botPos, [0.55, 0.05], orientation, math.pi/2) #default poition
                            else:
                                driver(botPos, [0.55, -0.05], orientation, math.pi/2) #default other side
                    elif inCone(ballPos, botPos, .05):
                        #print("pushing the ball")
                        score(botPos, ballPos, orientation) #push the ball away hopefully it is on the right side
                    elif abs(ballvel[0] - pastvel[0]) + abs(ballvel[1] - pastvel[1]) < .01: #redirected
                        #print("doing the same thing")
                        driver(botPos, sameTarget, orientation, sameOrientation)
                    elif (blue and ballPos[0] < 0.55) or (yellow and ballPos[0] > -.55):
                        #print("getting infront of the ball")
                        sameTarget = goalieMovement(ballPos, ballvel, botPos, False)
                        sameOrientation = 0
                        driver(botPos, sameTarget, orientation, sameOrientation)
                    else:
                        sameTarget = goalieMovement(ballPos, ballvel, botPos, True)
                        sameOrientation = math.atan((ballPos[0] - botPos[0]) / (ballPos[1] - botPos[1]))
                        driver(botPos, sameTarget, orientation, sameOrientation)
                #other positions
                
                #double check yellow v blue
        
my_robot = MyRobot()
my_robot.run()