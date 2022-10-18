import math


def reward_function(params):

    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    is_offtrack = params['is_offtrack']
    speed = params['speed']

    high = [[0, 8], [49, 84]]
    inHigh = False

    if closest_waypoints[0] > high[0][0] and closest_waypoints[0] < high[0][1]:
        inHigh = True
    elif closest_waypoints[0] > high[1][0] and closest_waypoints[0] < high[1][1]:
        inHigh = True

    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width

    if distance_from_center <= marker_1:
        reward = 1+speed
        if inHigh:
            reward += speed
    elif distance_from_center <= marker_2:
        reward = 0.5+speed*0.5
    elif distance_from_center <= marker_3:
        reward = 0.1+speed*0.2
    else:
        reward = 1e-3

    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]

    track_direction = math.atan2(
        next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    track_direction = math.degrees(track_direction)

    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    DIRECTION_THRESHOLD = 10.0
    if direction_diff > DIRECTION_THRESHOLD:
        reward *= 0.5
    else:
        reward *= 2

    if is_offtrack:
        reward = 1e-5

    return float(reward)
