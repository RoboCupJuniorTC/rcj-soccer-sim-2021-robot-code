import math

def get_direction(ball_angle: float) -> int:
	return -1 if ball_angle <= 360-90 else 1

def new_roles(data, name):
	team = name[0]
	pos = {}
	for i in range(3):
		pos[team + str(i+1)] = [data[team + str(i+1)]['x'], data[team + str(i+1)]['y']]
	if team == "Y":
		for i in pos:
			for j in pos[i]:
				j = -j

	#find distance from home side
	x = [abs(pos[team + "1"][0] - 0.75), abs(pos[team + "2"][0] - 0.75), abs(pos[team + "3"][0] - 0.75)]
	#finds distance from center
	y = [abs(pos[team + "1"][1]), abs(pos[team + "2"][1]), abs(pos[team + "3"][1])]

	distance = [0, 0, 0]
	m = 0
	for i in range(3):
		print(i)
		distance[i] = math.sqrt(x[i]**2 + y[i]**2)
		if distance[i] < distance[m]: m = i

	ball_pos = [data['ball']['x'], data['ball']['y']]
	ball_distance = [0, 0, 0]

	m2 = 0
	for i in range(3):
		ball_distance[i] = math.sqrt(abs(x[i] - ball_pos[0])**2 + abs(y[i] - ball_pos[1])**2)
		if ball_distance[i] < ball_distance[m2] and m2 != m: m2 = i

	m3 = 3 - m - m2

	return m+1, m2+1, m3+1;