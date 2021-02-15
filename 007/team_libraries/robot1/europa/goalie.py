import sys
from pathlib import Path
from enum import Enum
from typing import Tuple

sys.path.append(str(Path(".").absolute().parent))
from team_002_libraries.robot1.europa.consts import BLUE_PENALTY_AREA, YELLOW_PENALTY_AREA
from team_002_libraries.robot1.europa.europa import Europa
from team_002_libraries.robot1.europa.vector import Vector, distance


class GoalieState(Enum):
    GOING_TO_GOAL = 0
    DEFENDING_GOAL = 1
    BYPASSING_PENALTY = 2


class Goalie(Europa):
    def __init__(self, blue: bool = True):
        super(Goalie, self).__init__(blue)
        self.state: GoalieState = GoalieState.GOING_TO_GOAL
        self.our_goal_pos = Vector(0.72, 0) if self.is_blue else Vector(-0.72, 0)
        self.goal_bound = -0.07 if self.is_blue else 0.07

    def is_in_penalty(self, area: Tuple) -> bool:
        vertical, lower, upper = area
        return self.pos.x > vertical and lower < self.pos.y < upper

    def is_in_yellow_penalty(self) -> bool:
        vertical, lower, upper = YELLOW_PENALTY_AREA
        return self.pos.x < vertical and lower < self.pos.y < upper

    def is_in_blue_penalty(self) -> bool:
        vertical, lower, upper = BLUE_PENALTY_AREA
        return self.pos.x > vertical and lower < self.pos.y < upper

    def is_outside_penalty(self):
        return (
            self.pos.x < self.our_goal_pos.x + self.goal_bound
            if self.is_blue
            else self.pos.x > self.our_goal_pos.x + self.goal_bound
        )

    def on_tick(self):
        print(self.team, self.state)
        # predicted = self.predict_mod(
        #     50,
        #     self.ball_pos,
        #     self.ball_pos - self.previous_ball_pos,
        # )
        predicted = self.ball_pos
        if self.is_in_blue_penalty() or self.is_in_yellow_penalty():
            if not self.time_penalty_enter:
                self.time_penalty_enter = self.sim_time
            elif self.sim_time - self.time_penalty_enter >= 11000:
                self.state = GoalieState.BYPASSING_PENALTY
        else:
            self.time_penalty_enter = None
            self.state = GoalieState.GOING_TO_GOAL
        if self.state == GoalieState.GOING_TO_GOAL:
            if self.is_outside_penalty() or abs(self.pos.y) > 0.2:
                self.move_vec = self.our_goal_pos
                self.rotation = None
            elif not self.is_rotated_at(180):
                self.rotation = 180
            else:
                self.state = GoalieState.DEFENDING_GOAL
        elif self.state == GoalieState.DEFENDING_GOAL:
            if self.is_outside_penalty():
                self.state = GoalieState.GOING_TO_GOAL
            if abs(predicted.y - self.pos.y) > 0.01:
                if not -0.2 < predicted.y < 0.2 and not -0.2 < self.pos.y < 0.2:
                    self.stop()
                elif predicted.y - self.pos.y > 0:
                    self.backward()
                else:
                    self.forward()
        elif self.state == GoalieState.BYPASSING_PENALTY:
            if self.time_penalty_enter:
                self.go_to(predicted)
