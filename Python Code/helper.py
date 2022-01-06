import math
import csv
import numpy as np

event_numbers = {'None': 0,
'kickoff': 1,
'kick_received': 2,
'first_contact': 3,
'tackle': 4,
'ball_snap': 5,
'field_goal_attempt': 6,
'field_goal': 7,
'touchback': 8,
'extra_point_attempt': 9,
'extra_point': 10,
'punt': 11,
'fair_catch': 12,
'line_set': 13,
'punt_land': 14,
'punt_downed': 15,
'field_goal_missed': 16,
'punt_received': 17,
'kickoff_land': 18,
'out_of_bounds': 19,
'field_goal_play': 20,
'field_goal_fake': 21,
'pass_forward': 22,
'pass_arrived': 23,
'pass_outcome_touchdown': 24,
'fumble': 25,
'fumble_offense_recovered': 26,
'punt_muffed': 27,
'fumble_defense_recovered': 28,
'extra_point_missed': 29,
'handoff': 30,
'punt_fake': 31,
'pass_outcome_caught': 32,
'onside_kick': 33,
'kickoff_play': 34,
'drop_kick': 35,
'punt_blocked': 36,
'kick_recovered': 37,
'touchdown': 38,
'penalty_flag': 39,
'field_goal_blocked': 40,
'run': 41,
'xp_fake': 42,
'extra_point_fake': 43,
'pass_outcome_incomplete': 44,
'punt_play': 45,
'huddle_break_offense': 46,
'snap_direct': 47,
'lateral': 48,
'man_in_motion': 49,
'safety': 50,
'free_kick': 51,
'extra_point_blocked': 52,
'two_point_conversion': 53,
'free_kick_play': 54,
'play_action': 55,
'huddle_start_offense': 56,
'shift': 57,
'pass_shovel': 58,
'pass_outcome_interception': 59,
'qb_strip_sack': 60,
'penalty_accepted': 61,
'qb_sack': 62,
'timeout_home': 63,
'autoevent_kickoff': 64,
'field_goal_miseed': 65}

# ------------------ Lists ---------------- #

PD_HEADER = ['gameId', 'playId', 'playDescription', 'quarter', 'down',
             'yardsToGo', 'possessionTeam', 'specialTeamsPlayType',
             'specialTeamsResult', 'kickerId', 'returnerId', 'kickBlockerId',
             'yardlineSide', 'yardlineNumber', 'gameClock', 'penaltyCodes',
             'penaltyJerseyNumbers', 'penaltyYards', 'preSnapHomeScore',
             'preSnapVisitorScore', 'passResult', 'kickLength',
             'kickReturnYardage', 'playResult', 'absoluteYardlineNumber']

TRACKING_CELL_LABELS = ['x', 'y', 's', 'a', 'dis', 'o', 'dir', 'event', 'nflId']

# ------------------ Functions for working with iterables ------------------ #

# Function list_overlap
# Takes two lists as input and an optional boolean toggle. If not boolean,
# returns a list containing all elements in both lists. Otherwise, returns
# True if overlap is present and False if no overlap is present.
def list_overlap(a, b, boolean=False):
    result = []
    for a_ele in a:
        for b_ele in b:
            if a_ele == b_ele and a_ele not in result:
                result.append(a_ele)
    if boolean and result == []:
        return False
    elif boolean:
        return True
    else:
        return result

# Function extract
# Takes a column header and a row and returns the cell in the row corresponding
# to the column header. Of course, the header row must also be passed in. Simply
# converts the column name to an index and uses it on the row.
def extract(column_name, row_to_search, header_row):
    try:
        index = header_row.index(column_name)
    except ValueError:
        print('Function extract() was passed a column_name', column_name,
              'not present in the header row:', header_row)
        raise ValueError

    return row_to_search[index]

def string_to_iterable(string):
    if string[0] == '(' and string[-1] == ')':
        inner_string = string[1:-1].replace('\'', '')
        split_string = inner_string.split(', ')
        correct_tuple = tuple(split_string)
        good_type = correct_tuple
    elif string[0] == '[' and string[-1] == ']':
        inner_string = string[1:-1].replace('\'', '')
        split_string = inner_string.split(', ')
        good_type = split_string
    else:
        return string
    return good_type

# Function fix_iterable_in_grid
# Takes a grid with strings in each cell. If the strings should be lists or
# tuples, turns each string into list or tuple and returns the grid.
def fix_iterables_in_grid(grid):
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c][0] == '(' and grid[r][c][-1] == ')':
                inner_string = grid[r][c][1:-1].replace('\'', '')
                split_string = inner_string.split(', ')
                correct_tuple = tuple(split_string)
                grid[r][c] = correct_tuple
            elif grid[r][c][0] == '[' and grid[r][c][-1] == ']':
                inner_string = grid[r][c][1:-1].replace('\'', '')
                split_string = inner_string.split(', ')
                grid[r][c] = split_string
    return grid

# --------------------- Functions for working with time --------------------- #

def process_raw_time(string):
    if type(string) == float:
        return string
    time = string.split('T')[1]
    split_time = time.split(':')
    result = float(split_time[-1]) + float(split_time[-2]) * 60 + float(split_time[-3]) * 3600
    return result

def find_land_event(present_events):
    landings = ['punt_land', 'punt_received', 'punt_muffed',
                'fair_catch', 'out_of_bounds', 'touchback']
    for l in landings:
        if l in present_events:
            return l

def find_event_time(play_tracking_grid, event):
    for row in play_tracking_grid:
        if row[3] == event_numbers[event]:
            return process_raw_time(row[0])

# Function time_in_s
# Takes a time of the form (HR) (MN) . (SC) m as float or string and returns
# that time in plain seconds.
def time_in_s(time):
    t_string = str(time)
    while len(t_string.split('.')[0]) < 4:
        t_string = '0' + t_string
    while len(t_string.split('.')[1]) < 3:
        t_string = t_string + '0'
    try:
        number = int(t_string[:2]) * 3600 + int(t_string[2:4]) * 60 + int(t_string[5:7]) + int(t_string[7]) / 10
    except:
        print(time)
        raise ValueError
    return number


# Function time_to_number
# Takes a time string and returns (HR) (MN) . (SC) m number.
def time_to_number(time_string):
    running_value = int(time_string[0] + time_string[1]) * 100
    running_value += int(time_string[3] + time_string[4])
    running_value += int(time_string[6] + time_string[7] + time_string[9]) * 0.001
    running_value = round(running_value, 3)
    return running_value

# Function unpack_date_time
# Takes a row of data with a date-time as the first cell. Returns time string by
# default.
def unpack_date_time(row, return_date=False):
    if type(row) == str:
        print('STRING ALERT:')
        print(row)
        raise ValueError
    critical_cell = row[0]
    try:
        if return_date:
            return critical_cell.split('T')[0]
        else:
            return critical_cell.split('T')[1]
    except:
        print(row)
        raise TypeError

# Function increment_time
# Takes a number of (HR) (MN) . (SC) m format and returns number 0.1s later.
def increment_time(time_number):
    time_string = str(time_number)
    time_list = time_string.split('.')
    while len(time_list[0]) < 4:
        time_list[0] = '0' + time_list[0]
    while len(time_list[1]) < 3:
        time_list[1] = time_list[1] + '0'
    time_string = time_list[0] + '.' + time_list[1]
    first_place = time_string[0] + time_string[1]
    second_place = time_string[2] + time_string[3]
    third_place = time_string[5] + time_string[6]
    fourth_place = time_string[7]
    try:
        number_list = [int(first_place), int(second_place), int(third_place), int(fourth_place)]
    except ValueError:
        print(time_string)
        print(first_place, second_place, third_place, fourth_place)
        raise ValueError


    if number_list[-1] == 9:
        number_list[-1] = 0
        number_list[-2] += 1
        if number_list[-2] == 60:
            number_list[-2] = 00
            number_list[-3] += 1
            if number_list[-3] == 60:
                number_list[-3] = 00
                number_list[-4] += 1
    else:
        number_list[-1] += 1

    final_number = number_list[0] * 100 + number_list[1] + number_list[2] * 0.01 + number_list[3] * 0.001
    return round(final_number, 3)

# ----------------------- Functions for working with tracking data ----------------------- #

# Function nn_los
# Takes a grid of tracking data and returns the x-position of the line
# of scrimmage.
# Returns a float.
def los(play_tracking_grid):
    first_time_row = play_tracking_grid[1]
    first_fb_cell = first_time_row[-1]
    los = extract('x', first_fb_cell, TRACKING_CELL_LABELS)
    return float(los)

def distance(x1, y1, x2, y2):
    return math.sqrt( (x2-x1)**2 + (y2-y1)**2 )

def find_returner_id(play_tracking_grid, kicker_id):
    x_positions = []
    player_ids = []
    snap_tracking_data = pull_tracking_data(play_tracking_grid, 'ball_snap', football_only=False,
                                            cols_to_return=['x', 'nflId'])
    for cell in snap_tracking_data:
        x_positions.append(float(cell[0]))
        player_ids.append(cell[1])
        
    kicker_position = x_positions[player_ids.index(kicker_id)]
    x_distances = [abs(kicker_position - p) for p in x_positions]
    x_max = max(x_distances)
    returner_id = player_ids[x_distances.index(x_max)]
    return returner_id


# Function pull_tracking_data
# Takes one play of tracking data, an event to analyze in that data, whether to
# look at the football only, and which columns in each player to synthesize and
# return. If football only, returns just a list of pertinent football info. If
# all players, returns a list of sublists, where each sublist is one player's
# (plus the football's) pertinent columns
def pull_tracking_data(play_tracking_grid, event_to_accept,
                       football_only=False, cols_to_return=[], teamed=False,
                       by_time=False):
    if 'team' not in cols_to_return:
        teamed = False
    else:
        cols_to_return.remove('team')
    build_row = []
    for time_row in play_tracking_grid[1:]:
            if time_row[1][7] == event_to_accept or (by_time and time_row[0] == event_to_accept):
                if football_only:
                    
                    if 'time' in cols_to_return:
                        build_row.append(time_row[0])
                        cols_to_return.remove('time')
                    for tracking_ele in [extract(k, time_row[-1], TRACKING_CELL_LABELS) for k in cols_to_return]:
                        build_row.append(tracking_ele)
                    if teamed:
                        build_row.append(time_row[-1])
                else:
                    if 'time' in cols_to_return:
                        build_row.append(time_row[0])
                        cols_to_return.remove('time')
                    for cell in time_row[1:]:
                        cell_row = []
                        for tracking_ele in [extract(k, cell, TRACKING_CELL_LABELS) for k in cols_to_return]:
                            cell_row.append(tracking_ele)
                        if teamed:
                            cell_row.append(cell[-1])
                        build_row.append(cell_row) 
    if build_row == []:
        print('We got an empty!')
        print('event_to_accept:', event_to_accept)
        print('present_events:', [k[1] for k in play_tracking_grid])
        return 'NA'
        #print_grid(play_tracking_grid)
    return build_row

# Function load_play_of_trimmed_data
# Takes the name of the import file name (must be a csv) and the combined
# game + play id and loads all tracking rows under that play into a grid.
# Does NOT include the header row of length 1 with combined id.
def load_play_of_trimmed_data(import_file_name, combined_id):
    grid = []
    now_in_play = False
    with open(import_file_name, 'r') as f:
        csv_reader = csv.reader(f, delimiter = ',')
        for row in csv_reader:
            if now_in_play:
                grid.append(row)
                
            if len(row) == 1:
                if row[0] == combined_id:
                    now_in_play = True
                elif now_in_play == True:
                    break
                else:
                    now_in_play = False
    grid.pop(0)
    grid.pop(-1)
    return fix_iterables_in_grid(grid)

# -------------------- Functions for working with play data --------------------- #

# Function test_play_data_for_penalty
# Takes a row of play data and whether or not to exclude plays with penaties. If
# not ecluding penalties, returns True regardless. Otherwise, returns True only
# if play data penalty code is 'NA', and False otherwise.
def test_play_data_for_penalty(row, remove_penalties):
    if not remove_penalties:
        return True
    else:
        if row[15] == 'NA':
            return True
        else:
            return False

# Function find_play_data
# Takes a combined game + play id and returns the row of the plays.csv
# file associated with that play.
def find_play_data(combined_id, import_file_name='plays.csv'):
    game_id = combined_id[:10]
    play_id = combined_id[10:]
    with open(import_file_name, 'r') as f:
        csv_reader = csv.reader(f, delimiter=',')
        for row in csv_reader:
            if game_id == row[0] and play_id == row[1]:
                return row


# ------------- Functions to evaluate tracking data for the neural network ----------------- #

def is_returned(play_tracking_grid, present_events, *args):
    if 'punt_blocked' in present_events:
        return 'NA'
    if 'punt_received' in present_events or 'punt_muffed' in present_events or 'fumble' in present_events:
        return [1, 0, 0]
    elif 'fair_catch' in present_events:
        return [0, 1, 0]
    else:
        return [0, 0, 1]

def is_in_play(play_tracking_grid, present_events, *args):
    land_event = find_land_event(present_events)
    fb_at_land = pull_tracking_data(play_tracking_grid, land_event, football_only=True,
                                    cols_to_return=['x', 'y'])
    land_x = float(fb_at_land[0])
    land_y = float(fb_at_land[1])

    if land_x <= 10 or land_x >= 110:
        return 0
    elif land_y <= 0 or land_y >= 53.3:
        return 0
    else:
        return 1

# Function nn_hang_time
# Takes a grid of tracking data and returns the hang time of the punt. If
# punt is not received.
# Returns a float.
# Note: Must have a 'punt' event and either a 'punt_received' or 'punt_land'
# event. Prefers 'punt_land'.
def nn_hang_time(play_tracking_grid, present_events, *args):
    land_event = find_land_event(present_events)
    first_time = pull_tracking_data(play_tracking_grid, 'punt', football_only=True, cols_to_return=['time'])[0]
    second_time = pull_tracking_data(play_tracking_grid, land_event, football_only=True, cols_to_return=['time'])[0]
    result = time_in_s(float(second_time)) - time_in_s(float(first_time))
    return round(result, 1)

# Function nn_total_distance
# Takes ax grid of tracking data and returns the vertical distance
# of the punt. 
# Returns a float.
# Note: Must have a 'punt' event and either a 'punt_received' or 'punt_land'
# event. Prefers 'punt_land'.
def nn_vertical_distance(play_tracking_grid, present_events, *args):
    land_event = find_land_event(present_events)
    initial_x = los(play_tracking_grid)
    final_x = pull_tracking_data(play_tracking_grid, land_event, football_only=True, cols_to_return=['x'])[0]
    result = abs(float(final_x) - float(initial_x))
    return round(result, 1)

# Function nn_yards_to_sideline
# Takes a grid of tracking data and returns the ball's distance to the sideline
# when it lands or is received. 
# Returns a float.
# Note: Must
# have a 'punt' event and either a 'punt_received' or 'punt_land'
# event. Prefers 'punt_land'.
def nn_yards_to_sideline(play_tracking_grid, present_events, *args):
    land_event = find_land_event(present_events)
    final_y = pull_tracking_data(play_tracking_grid, land_event, football_only=True, cols_to_return=['y'])[0]
    return round(min(53.3 - float(final_y), float(final_y)), 1)

# Function find_back_goal_line
# Takes a grid of tracking data and list of present events. Returns the
# x-value of the goal line behind the returner. Depends on direction the
# punt travels.
# Returns a float.
# Note: Must have a 'punt' event and either a 'punt_received' or 'punt_land'
# event. Prefers 'punt_land'.
def find_back_goal_line(play_tracking_grid, present_events, *args):
    land_event = find_land_event(present_events)
    initial_x = pull_tracking_data(play_tracking_grid, 'punt', football_only=True, cols_to_return=['x'])[0]
    final_x = pull_tracking_data(play_tracking_grid, land_event, football_only=True, cols_to_return=['x'])[0]
    if (float(final_x) - float(initial_x)) > 0:
        return 110
    else:
        return 10

# Function nn_yards_to_goal_line
# Takes a grid of tracking data and returns the distance to the back goal
# line.
# Returns a float.
# Note: Must have a 'punt' event and either a 'punt_received' or 'punt_land'
# event. Prefers 'punt_land'.
def nn_yards_to_goal_line(play_tracking_grid, present_events, *args):
    land_event = find_land_event(present_events)
    final_x = pull_tracking_data(play_tracking_grid, land_event, football_only=True, cols_to_return=['x'])[0]
    goal_line = find_back_goal_line(play_tracking_grid, present_events)
    return round(abs(float(final_x) - float(goal_line)), 2)

# Function nn_returner_displacement
# Takes a grid of tracking data, a list of present_events, and the returner id
# and returns the distance between the returner's position at punt and the ball's
# landing position.
# Returns a float.
# Note: Must have a 'punt' event and either a 'punt_received' or 'punt_land'
# event. Prefers 'punt_land'.
def nn_returner_displacement(play_tracking_grid, present_events, returner_id, play_data):
    land_event = find_land_event(present_events)
    if land_event == None:
        return 'NA'
    players_at_land = pull_tracking_data(play_tracking_grid, land_event, football_only=False,
                                              cols_to_return=['x', 'y', 'nflId'])
    players_at_punt = pull_tracking_data(play_tracking_grid, 'punt', football_only=False,
                                              cols_to_return=['x', 'y', 'nflId'])
    football_at_land = pull_tracking_data(play_tracking_grid, land_event, football_only=True,
                                              cols_to_return=['x', 'y', 'nflId'])
    for player in players_at_land:
        if player[2] == 'NA':
            returner_at_land = player
            break
    if returner_id == 'NA':
        return 'NA'
    
    for player in players_at_punt:
        if player[2] == returner_id:
            returner_at_punt = player
            break
    
    final_x = float(returner_at_land[0])
    final_y = float(returner_at_land[1])
    initial_x = float(returner_at_punt[0])
    initial_y = float(returner_at_punt[1])
    return round(distance(initial_x, initial_y, float(final_x), float(final_y)), 1)

# ------------------ Functions for saving and loading neural network parameters ----------------------#

def save_network(network_parameters, file):
    with open(file, 'w') as f:
        csv_writer = csv.writer(f, delimiter=',')
        for key, item in network_parameters.items():
            csv_writer.writerow([key])
            csv_writer.writerows(item)
    print('Saved network to', file)
    
def load_network(file):
    parameters = {}
    with open(file, 'r') as f:
        csv_reader = csv.reader(f, delimiter=',')
        for row in csv_reader:
            if len(row) == 1 and ('B' in row[0] or 'W' in row[0]):
                current_key = row[0]
                parameters[current_key] = []
            else:
                parameters[current_key].append([float(r) for r in row])

    for key, item in parameters.items():
        parameters[key] = np.array(item)

    return parameters

# ---------------- Forward Propogation functions for neural networks ---------------- #

def forward_propogation_classification(learn_x_T, parameters):
    layers = int(len(parameters) / 2)
    predicted_values = {}
    
    for i in range(1, int(layers + 1)):
        if i == 1:
            predicted_values['Z' + str(i)] = np.dot(parameters['W' + str(i)], learn_x_T) + parameters['B' + str(i)]
            predicted_values['A' + str(i)] = relu_nozero(predicted_values['Z' + str(i)])
        else:
            predicted_values['Z' + str(i)] = np.dot(parameters['W' + str(i)], predicted_values['A' + str(i - 1)]) + parameters['B' + str(i)]
            if i == layers:
                predicted_values['A' + str(i)] = relu_nozero(predicted_values['Z' + str(i)])
                predicted_values['A' + str(i)] = np.true_divide(predicted_values['A' + str(i)], predicted_values['A' + str(i)].sum(axis=0, keepdims=1))
            else:
                predicted_values['A' + str(i)] = relu_nozero(predicted_values['Z' + str(i)])
    return predicted_values

def forward_propogation_returns(learn_x_T, parameters):
    layers = int(len(parameters) / 2)
    predicted_values = {}
    for i in range(1, int(layers + 1)):
        if i == 1:
            predicted_values['Z' + str(i)] = np.dot(parameters['W' + str(i)], learn_x_T) + parameters['B' + str(i)]
            predicted_values['A' + str(i)] = relu(predicted_values['Z' + str(i)])
        else:
            predicted_values['Z' + str(i)] = np.dot(parameters['W' + str(i)], predicted_values['A' + str(i - 1)]) + parameters['B' + str(i)]
            if i == layers:
                predicted_values['A' + str(i)] = predicted_values['Z' + str(i)]
            else:
                predicted_values['A' + str(i)] = relu(predicted_values['Z' + str(i)])
    return predicted_values

# ------------------ Additional functions for creating neural networks --------------------- #

def relu(x):
    return np.maximum(0, x)

def relu_nozero(x):
    return np.maximum(0.001, x)
