import csv
import numpy as np
from helper import *

all_roll_lengths = []
with open('df_for_nn.csv', 'r') as f:
    csv_reader = csv.reader(f, delimiter=',')
    for row in csv_reader:

        if 'playResult' in row:
            label_row = row
            proper_length = len(row)
            continue

        if len(row) != proper_length:
            continue

        if 'NA' == extract('kickLength', row, label_row) or 'NA' == extract('nn_vertical_distance', row, label_row):
            continue

        if extract('is_returned', row, label_row) == '[0, 0, 1]' and extract('is_in_play', row, label_row) == '1' and 'Touchback' not in extract('playDescription', row, label_row):
            kick_length = float(extract('kickLength', row, label_row))
            air_length = float(extract('nn_vertical_distance', row, label_row))
            all_roll_lengths.append(air_length - kick_length)
            
avg_roll_length = 4.12

classification_parameters = load_network('classify_parameters.csv')
return_length_parameters = load_network('return_parameters.csv')

### Returns 'NA' if unable to calculate
##def expected_net_yards(combined_play_id, classification_params, return_params):
##    play_data = find_play_data(combined_play_id, 'plays.csv')
##    
##    if extract('specialTeamsPlayType', play_data, PD_HEADER) != 'Punt':
##        return 'NA'
##
##    tracking_data = load_play_of_trimmed_data('punt_tracking_data.csv', combined_play_id)
##    returner_id = extract('returnerId', play_data, PD_HEADER)
##    kicker_id = extract('kickerId', play_data, PD_HEADER)
##    present_events = list(set([r[1][7] for r in tracking_data]))
##
##    if 'punt' not in present_events or 'ball_snap' not in present_events:
##        return 'NA'
##
##    if ";" in returner_id or returner_id == 'NA':
##        returner_id = find_returner_id(tracking_data, kicker_id)
##    
##
##    if not list_overlap(present_events, ['punt_land', 'punt_received', 'fair_catch',
##                                     'out_of_bounds', 'touchback', 'punt_muffed'], boolean=True):
##        return 'NA'
##
##    x_vector = []
##    for stat in ['nn_hang_time', 'nn_vertical_distance', 'nn_yards_to_sideline',
##                 'nn_yards_to_goal_line', 'nn_returner_displacement']:
##        x_vector.append(globals()[stat](tracking_data, present_events, returner_id, play_data))
##
##    if 'NA' in x_vector or None in x_vector:
##        return 'NA'
##
##    in_play = is_in_play(tracking_data, present_events, returner_id, play_data)
##
##    if in_play == 0:
##        return float(extract('kickLength', play_data, PD_HEADER))
##
##    else:
##        x_array = np.array(x_vector)
##        classification_prediction = forward_propogation_classification(x_array.T, classification_params)['A3']
##        return_length_prediction = forward_propogation_returns(x_array.T, return_length_params)['A3']
##
##        kick_contribution = x_vector[1]
##        return_contribution = classification_prediction[0] * return_length_prediction
##        roll_contribution = classification_prediction[1] * avg_roll_length
##
##        return kick_contribution - return_contribution - roll_contribution
    
def calculate_eny_ery(play_tracking_data, play_data, c_parameters, r_parameters):
    returner_id = extract('returnerId', play_data, PD_HEADER)
    kicker_id = extract('kickerId', play_data, PD_HEADER)
    present_events = list(set([r[1][7] for r in play_tracking_data[1:]]))
    
    if 'punt' not in present_events or 'ball_snap' not in present_events:
        return ('NA', 'NA')

    if ";" in returner_id or returner_id == 'NA':
        returner_id = find_returner_id(play_tracking_data, kicker_id)

    if not list_overlap(present_events, ['punt_land', 'punt_received', 'fair_catch',
                                     'out_of_bounds', 'touchback', 'punt_muffed'], boolean=True):
        return ('NA', 'NA')

    x_vector = []
    for stat in ['nn_hang_time', 'nn_vertical_distance', 'nn_yards_to_sideline',
                 'nn_yards_to_goal_line', 'nn_returner_displacement']:
        x_vector.append(globals()[stat](play_tracking_data, present_events, returner_id, play_data))

    if 'NA' in x_vector or None in x_vector:
        return ('NA', 'NA')
    in_play = is_in_play(play_tracking_data, present_events, returner_id, play_data)

    if in_play == 0:
        return (float(extract('playResult', play_data, PD_HEADER)), 'NA')

    else:
        x_array = np.array([x_vector])
        classification_prediction = list(forward_propogation_classification(x_array.T, c_parameters)['A3'][:, 0])
        return_length_prediction = forward_propogation_returns(x_array.T, r_parameters)['A3'][0, 0]

        kick_contribution = x_vector[1]
        return_contribution = classification_prediction[0] * return_length_prediction
        if x_vector[3] < avg_roll_length:
            roll_contribution = 20 - x_vector[3]
        else:
            roll_contribution = classification_prediction[1] * avg_roll_length

        eny = kick_contribution - return_contribution - roll_contribution

        return (round(eny, 2), round(return_length_prediction, 2))

    
play_tracking_grid = []
evaluation = []
combined_play_id = None

with open('punt_tracking_data.csv', 'r') as f:
    csv_reader = csv.reader(f, delimiter = ',')
    for row in csv_reader:
        row = fix_iterables_in_grid(row)
        row = [string_to_iterable(r) for r in row]
        if len(row) == 1:
            if play_tracking_grid == []:
                combined_play_id = row[0]
                continue
            play_data = find_play_data(combined_play_id)
            if extract('specialTeamsPlayType', play_data, PD_HEADER) != 'Punt' or extract('penaltyCodes', play_data, PD_HEADER) != 'NA':
                play_tracking_grid = []
                combined_play_id = row[0]
                continue


            eny, ery = calculate_eny_ery(play_tracking_grid, play_data, classification_parameters, return_length_parameters)
            if eny == 'NA':
                play_tracking_grid = []
                combined_play_id = row[0]
                continue

            
            actual_net_yards = float(extract('playResult', play_data, PD_HEADER))
            actual_return_yards = extract('kickReturnYardage', play_data, PD_HEADER)
            if actual_return_yards != 'NA':
                actual_return_yards = float(actual_return_yards)

            kicker_id = extract('kickerId', play_data, PD_HEADER)
            returner_id = extract('returnerId', play_data, PD_HEADER)
            if ';' in returner_id:
                returner_id = find_returner_id(play_tracking_grid, kicker_id)
            play_outcome = extract('specialTeamsResult', play_data, PD_HEADER)
            kick_team = extract('possessionTeam', play_data, PD_HEADER)
            if play_outcome == 'Blocked Punt':
                kick_length = 'NA'
            else:
                kick_length = float(extract('kickLength', play_data, PD_HEADER))

            if play_outcome != 'Return':
                ery = 'NA'
            
            new_row = [combined_play_id, kicker_id, returner_id, eny, actual_net_yards, ery, actual_return_yards, kick_length, kick_team, play_outcome]
            evaluation.append(new_row)
            
            combined_play_id = row[0]
            play_tracking_grid = []
        else:
            play_tracking_grid.append(row)

##evaluation = []
##with open('plays.csv', 'r') as f:
##    csv_reader = csv.reader(f, delimiter=',')
##    for row in csv_reader:
##        combined_play_id = row[0] + row[1]
##        if extract('specialTeamsPlayType', row, PD_HEADER) == 'Punt' and extract('penaltyCodes', row, PD_HEADER) == 'NA':
##            real_net_yards = float(extract('playResult', row, PD_HEADER))
##            predicted_net_yards = expected_net_yards(combined_play_id, classification_parameters, return_length_parameters)
##            kicker_id = extract('kickerId', row, PD_HEADER)
##            returner_id = extract('returnerId', row, PD_HEADER)
##            new_row = [combined_play_id, kicker_id, returner_id, real_net_yards, predicted_net_yards]
##            evaluation.append(new_row)

evaluation_file_name = 'raw_evaluation.csv'
with open(evaluation_file_name, 'w') as f:
    csv_writer = csv.writer(f, delimiter = ',')
    csv_writer.writerow(['Combined Play ID', 'Kicker Id', 'Returner Id', 'Expected Net Yards', 'Real Net Yards', 'Expected Return Yards', 'Real Return Yards', 'Kick Length', 'Kick Team', 'Play Result'])
    csv_writer.writerows(evaluation)
print('Finished writing evaluation to', evaluation_file_name)
