from enum import Enum
import sys
from pathlib import Path

sys.path.append(str(Path(".").absolute().parent))

from team_007_libraries.robot1.europa.europa import Europa
from team_007_libraries.robot1.europa.vector import Vector, angle, distance, is_angle_between


class StrikerState(Enum):
    FOLLOWING_BALL = 0
    GOING_FOR_GOAL = 1


class Striker(Europa):
    def __init__(self, blue: bool = True):
        super(Striker, self).__init__(blue, striker=True)
        self.goal_corner_1 = self.target_goal_pos + Vector(0, 0.4)
        self.goal_corner_2 = self.target_goal_pos + Vector(0, -0.4)
        self.state: StrikerState = StrikerState.FOLLOWING_BALL

    def on_tick(self):
        predicted = self.predict_mod(
            (300 * distance(self.ball_pos, self.pos)),
            self.ball_pos,
            self.ball_pos - self.previous_ball_pos,
        )
        if self.state == StrikerState.FOLLOWING_BALL:
            if self.stars_have_aligned(predicted):
                self.state = StrikerState.GOING_FOR_GOAL
            offset = self.ball_offset(predicted)
            if abs(self.pos.y) >= 0.55:
                offset *= -1
            self.go_to_angle(offset)
        elif self.state == StrikerState.GOING_FOR_GOAL:
            if not self.stars_have_aligned(predicted):
                self.state = StrikerState.FOLLOWING_BALL
            if abs(distance(self.pos, predicted)) < 0.3:
                self.go_to(self.target_goal_pos)
            else:
                self.go_to(predicted)

    def stars_have_aligned(self, ball_pos: Vector) -> bool:
        return is_angle_between(
            (self.pos.angle_to(self.ball_pos) + 450) % 360,
            (self.pos.angle_to(self.goal_corner_1) + 450) % 360,
            (self.pos.angle_to(self.goal_corner_2) + 450) % 360,
        )
