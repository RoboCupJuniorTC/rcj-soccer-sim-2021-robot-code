from team_025_libraries.robot1.Utils import Vector2

TIMESTEP = 64

ROBOTNAMES = ["B1", "B2", "B3", "Y1", "Y2", "Y3"]
NROBOTS = len(ROBOTNAMES)

BLUEPENALTYAREA = Vector2(0.59, -0.35)

BLUEGOAL: Vector2 = Vector2(0.65, 0.0)
YELLOWGOAL: Vector2 = Vector2(-0.7, 0.0)

#GoalKeeper Consts

GKATTACKSPOT: Vector2 = Vector2(0.5, 0.0)
GKDEFENSESPOT: Vector2 = Vector2(0.7, 0.0)
