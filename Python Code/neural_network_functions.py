import math
from helper_functions import *

# Y-Value Functions


def is_returned(present_events):
    if event_numbers['punt_blocked'] in present_events:
        return 'NA'
    if event_numbers['punt_received'] in present_events or event_numbers['punt_muffed'] in present_events or event_numbers['fumble'] in present_events:
        return 1
    elif event_numbers['fair_catch'] in present_events:
        return 2
    else:
        return 3

def roll_yardage(play_tracking_grid, present_events, this_play_data, returner_id):
    land_event = find_land_event(present_events)
    
    kick_length = float(this_play_data[2])
    start_yl = los(play_tracking_grid)
    for row in play_tracking_grid:
        if row[3] == event_numbers[land_event] and row[4] == 0:
            end_yl = row[1]
    delta_yl = abs(end_yl - start_yl)
    #print('vd:', vertical_distance)
    #print('kl:', kick_length)
    return round(kick_length - delta_yl, 2)

def return_yardage(this_play_data):
    if this_play_data[3] == 'NA':
        return 0
    else:
        return float(this_play_data[3])

# X-Value Functions


# Function returner_displacement
# Takes a grid of tracking data, a list of present_events, and the returner id
# and returns the distance between the returner's position at punt and the ball's
# landing position.
# Returns a float.
# Note: Must have a 'punt' event and either a 'punt_received' or 'punt_land'
# event. Prefers 'punt_land'.
def returner_displacement(play_tracking_grid, present_events, returner_id):
    land_event = find_land_event(present_events)
    if land_event == None:
        return 'NA'
    if returner_id == 'NA':
        returner_id = find_returner_id(play_tracking_grid, kicker_id)
    for row in play_tracking_grid:
        if row[3] == event_numbers['punt'] and row[4] == float(returner_id):
            initial_x = row[1]
            initial_y = row[2]
        elif row[3] == event_numbers[land_event] and row[4] == float(returner_id):
            final_x = row[1]
            final_y = row[2]
    #print('Initial:  (', initial_x, ',', initial_y, ')', '   Final: (', final_x, ',', final_y, ')')
    return round(distance(initial_x, initial_y, final_x, final_y), 1)


# Function yards_to_goal_line
# Takes a grid of tracking data and returns the distance to the back goal
# line.
# Returns a float.
# Note: Must have a 'punt' event and either a 'punt_received' or 'punt_land'
# event. Prefers 'punt_land'.
def yards_to_goal_line(play_tracking_grid, present_events, returner_id=None):
    land_event = find_land_event(present_events)
    if land_event == None:
        return 'NA'
    for row in play_tracking_grid:
        if row[3] == event_numbers[land_event] and row[4] == 0: # Finds football at land
            final_x = row[1]
    goal_line = find_back_goal_line(play_tracking_grid, present_events)
    return round(abs(final_x - goal_line), 2)

# Function find_back_goal_line
# Takes a grid of tracking data and list of present events. Returns the
# x-value of the goal line behind the returner. Depends on direction the
# punt travels.
# Returns a float.
# Note: Must have a 'punt' event and either a 'punt_received' or 'punt_land'
# event. Prefers 'punt_land'.
def find_back_goal_line(play_tracking_grid, present_events, returner_id=None):
    land_event = find_land_event(present_events)
    if land_event == None:
        return 'NA'
    for row in play_tracking_grid:
        if row[3] == event_numbers['punt'] and row[4] == 0:
            initial_x = row[1]
        if row[3] == event_numbers[land_event] and row[4] == 0:
            final_x = row[1]
    if final_x - initial_x > 0:
        return 110
    else:
        return 10

# Function yards_to_sideline
# Takes a grid of tracking data and returns the ball's distance to the sideline
# when it lands or is received. 
# Returns a float.
# Note: Must have a 'punt' event and either a 'punt_received' or 'punt_land'
# event. Prefers 'punt_land'.
def yards_to_sideline(play_tracking_grid, present_events, returner_id=None):
    land_event = find_land_event(present_events)
    if land_event == None:
        return 'NA'
    for row in play_tracking_grid:
        if row[3] == event_numbers[land_event] and row[4] == 0: # Finds football at land
            final_y = row[2]
    return round(min(53.3 - final_y, final_y), 1)

# Function total_distance
# Takes a grid of tracking data and returns the vertical distance
# of the punt. 
# Returns a float.
# Note: Must have a 'punt' event and either a 'punt_received' or 'punt_land'
# event. Prefers 'punt_land'.
def vertical_distance(play_tracking_grid, present_events, returner_id=None):
    land_event = find_land_event(present_events)
    if land_event == None:
        return 'NA'
    initial_x = los(play_tracking_grid)

    for row in play_tracking_grid:
        if row[3] == event_numbers[land_event] and row[4] == 0: # Finds ball at land
            final_x = row[1]
            
    result = abs(final_x - initial_x)
    return round(result, 1)

# Function hang_time
# Takes a grid of tracking data and returns the hang time of the punt. If
# punt is not received.
# Returns a float.
# Note: Must have a 'punt' event and either a 'punt_received' or 'punt_land'
# event. Prefers 'punt_land'.
def hang_time(play_tracking_grid, present_events, returner_id=None):
    land_event = find_land_event(present_events)
    if land_event == None:
        return 'NA'
    first_time = find_event_time(play_tracking_grid, 'punt')
    second_time = find_event_time(play_tracking_grid, land_event)
    result = second_time - first_time

    return abs(round(result, 1))

# Function total_punt_distance
# Takes a grid of tracking data and returns the total air distance the ball
# travels during the punt. Returns a float.
def total_punt_distance(play_tracking_grid, present_events, returner_id=None):
    land_event = find_land_event(present_events)
    if land_event == None:
        return 'NA'
    
    for row in play_tracking_grid:
        if row[3] == event_numbers['punt'] and row[4] == 0:
            initial_x = row[1]
            initial_y = row[2]
        elif row[3] == event_numbers[land_event] and row[4] == 0:
            final_x = row[1]
            final_y = row[2]
    result = distance(initial_x, initial_y, final_x, final_y)

    return round(result, 1)
        
