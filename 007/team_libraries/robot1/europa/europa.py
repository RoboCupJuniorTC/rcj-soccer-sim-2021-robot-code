###### REQUIRED in order to import files from B1 controller
from math import asin, degrees, pi
from typing import Union
import sys
from time import time
from pathlib import Path
from enum import Enum
import math

sys.path.append(str(Path(".").absolute().parent))
from team_002_libraries.robot1.europa.rcj_soccer_robot import RCJSoccerRobot, TIME_STEP
from team_002_libraries.robot1.europa.vector import Vector, distance, length

millis = lambda: int(round(time() * 1000))


class Europa(RCJSoccerRobot):
    def __init__(self, blue: bool = True, striker: bool = False):
        self.pos = Vector(0, 0)
        self.previous_ball_pos = Vector(0, 0)
        self.current_ball_pos = Vector(0, 0)
        if blue:
            self.target_goal_pos = Vector(0.8, 0)
        else:
            self.target_goal_pos = Vector(-0.8, 0)
        self.is_blue = blue
        self.orientation = 0.0
        self.previous_ball_pos = Vector(0, 0)
        self.ball_pos = Vector(0, 0)
        self.ball_velocity = 0.0
        self.sim_time = 0
        self.offset_dist = 0.1
        self.rotation: Union[None, float] = None
        self.move_vec: Union[None, Vector] = None
        self.striker = striker
        super().__init__()

    def predict_mod(self, elapsed: float, pos: Vector, direction: Vector) -> Vector:
        diff = self.ball_pos - self.previous_ball_pos
        try:
            if (
                abs(
                    ((self.ball_pos.x - self.pos.x) * (diff.y / diff.x))
                    - (self.ball_pos.y - self.pos.y)
                )
                < self.offset_dist
            ):
                endX = pos.x
                endY = pos.y
            else:
                endX = pos.x + (elapsed * diff.x)
                endY = pos.y + (elapsed * diff.y)
                while endX > 0.65 or endX < -0.65:
                    endX = 1.3 - endX if endX > 0.65 else -1.3 - endX
                while endY > 0.75 or endY < -0.75:
                    endY = 1.5 - endY if endY > 0.75 else -1.5 - endY
        except:
            endX = pos.x
            endY = pos.y
        return Vector(endX, endY)

    def predict_ball_pos(self, elapsed: int) -> Vector:
        painVector = self.ball_pos + (
            elapsed * (self.ball_pos - self.previous_ball_pos)
        )
        if abs(painVector.x) > 0.65 or abs(painVector.y) > 0.75:
            pass

        return painVector

    def run(self):
        while self.robot.step(TIME_STEP) != -1:
            self.sim_time += TIME_STEP
            self.rotation = None
            self.move_vec = None
            if self.is_new_data():
                data = self.get_new_data()
                self.pos = Vector(data[self.name]["x"], data[self.name]["y"])
                self.orientation = data[self.name]["orientation"]

                if self.orientation < 0:
                    self.orientation = 2 * pi + self.orientation

                self.ball_pos = Vector(data["ball"]["x"], data["ball"]["y"])

                if self.previous_ball_pos is not None:
                    self.ball_velocity = abs(
                        distance(self.ball_pos, self.previous_ball_pos) / TIME_STEP
                    )

                self.on_tick()
                if self.move_vec:
                    self.go_to(self.move_vec)
                elif self.rotation:
                    rot = self.oriented_to_robot(self.rotation)
                    rot = (rot - 360) if rot > 180 else rot
                    # self.go_to_angle(rot)
                    if rot > 0:
                        self.left_motor.setVelocity(3)
                        self.right_motor.setVelocity(-3)
                    else:
                        self.left_motor.setVelocity(-3)
                        self.right_motor.setVelocity(3)
                self.previous_ball_pos = self.ball_pos

    def set_move_vec(self, v: Vector):
        self.reached_target = False
        self.move_vec = v

    def set_rotation(self, rot: float):
        self.rotation = rot
        self.finished_rotating = False

    def is_rotated_at(self, rot: float):
        return -5 < rot - self.oriented_to_robot(rot) < 5

    def stop(self):
        self.left_motor.setVelocity(0)
        self.right_motor.setVelocity(0)

    def forward(self):
        self.left_motor.setVelocity(10)
        self.right_motor.setVelocity(10)

    def backward(self):
        self.left_motor.setVelocity(-10)
        self.right_motor.setVelocity(-10)

    def go_to(self, pt: Vector) -> None:
        target_angle = (pt.angle_to(self.pos) + degrees(self.orientation)) % 360
        self.go_to_angle(target_angle)

    def ball_offset(self, ball_pos: Vector) -> float:
        dist_vec = self.pos - ball_pos
        dist_len = length(dist_vec)
        angle = asin(self.offset_dist / max(dist_len, self.offset_dist))
        angle = degrees(angle) + 4
        if (self.is_blue and dist_vec.y < 0) or (not self.is_blue and dist_vec.y > 0):
            angle *= -1
        return self.get_ball_angle() + angle

    def go_to_angle(self, target_angle: float) -> None:
        max_speed = 5
        leftMove = 0
        rightMove = 0
        direction = -1
        target_angle = target_angle - 360 if target_angle > 180 else target_angle
        if not self.striker:
            if target_angle > 90 or target_angle < -90:
                direction *= -1
                target_angle -= 180
                if target_angle < -180:
                    target_angle += 360

        target_angle /= 14
        target_angle = min(target_angle, 10)

        leftMove = min(direction * max_speed - target_angle, max_speed)
        rightMove = min(direction * max_speed + target_angle, max_speed)
        # if target_angle <= 15 or target_angle >= 345:
        #     leftMove = -5
        #     rightMove = -5
        # elif target_angle < 180:
        #     leftMove = -4 - (9 * (target_angle / 360))
        #     rightMove = 4
        # else:
        #     leftMove = 4 + (9 * (target_angle / 360))
        #     rightMove = -4
        self.left_motor.setVelocity(leftMove)
        self.right_motor.setVelocity(rightMove)

    def oriented_to_robot(self, val: float) -> float:
        return (val + degrees(self.orientation)) % 360

    def get_ball_angle(self) -> float:
        # Get the angle between the robot and the ball
        angle = self.oriented_to_robot(self.ball_pos.angle_to(self.pos))
        return angle

    def on_tick(self):
        return
