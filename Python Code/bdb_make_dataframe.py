from helper import *




df = []
comb_ids = []
label_row = ['Play ID']
accepted_play_events = ['Punt']
play_columns_to_pull = [0, 1, 2, 9, 10, 21, 22, 23]
remove_penalties = True

play_data_file_name = 'plays.csv'

label_row = label_row + [PD_HEADER[int(k)] for k in play_columns_to_pull]
with open(play_data_file_name, 'r') as f:
    csv_reader = csv.reader(f, delimiter=',')
    for row in csv_reader:
        if list_overlap(row, accepted_play_events, boolean=True) and test_play_data_for_penalty(row, remove_penalties):
            combined_id_play = row[0] + row[1]
            play_data_info = [combined_id_play] + [row[int(k)] for k in play_columns_to_pull]
            df.append(play_data_info)
            comb_ids.append(combined_id_play)
            

necessary_events = [['punt'], ['ball_snap'], ['punt_land', 'punt_received', 'fair_catch', 'out_of_bounds', 'touchback']]

make_stats = ['nn_hang_time', 'nn_vertical_distance',
                       'nn_yards_to_sideline', 'nn_yards_to_goal_line',
                       'nn_returner_displacement', 'is_returned', 'is_in_play']
label_row = label_row + make_stats

tracking_import_file = 'punt_tracking_data.csv'

play_tracking_grid = []
with open(tracking_import_file, 'r') as f:
    csv_reader = csv.reader(f, delimiter = ',')
    for row in csv_reader:
        for i in range(len(row)):
            row[i] = string_to_iterable(row[i])
        if len(row) == 1:
            if play_tracking_grid != []:
                current_combined_id = play_tracking_grid[0][0]
                present_events = list(set([r[1][7] for r in play_tracking_grid[1:]]))
                this_play_data = find_play_data(current_combined_id)
                truth_list = []
                for lis in necessary_events:
                    truth_list.append(list_overlap(lis, present_events, boolean=True))

                if False in truth_list:
                    tracking_stats = ['NA' for h in make_stats]
                    
                
                else:
                    kicker_id = extract('kickerId', this_play_data, PD_HEADER)
                    returner_id = extract('returnerId', this_play_data, PD_HEADER)
                    if ";" in returner_id or returner_id == 'NA':
                        returner_id = find_returner_id(play_tracking_grid, kicker_id)
                    tracking_stats = []
                    for s in make_stats:
                        this_tracking_stat = locals()[s](play_tracking_grid, present_events, returner_id, this_play_data)
                        tracking_stats.append(this_tracking_stat)

                current_combined_id = play_tracking_grid[0][0]
                current_id_index = comb_ids.index(current_combined_id)
                current_play_data = df[current_id_index]
                df[current_id_index] = current_play_data + tracking_stats
                play_tracking_grid = []
            if row[0] in comb_ids:
                in_play = True
            else:
                in_play = False
        elif in_play:
            play_tracking_grid.append(row)
            
export_file = 'df_for_nn.csv'

df = [label_row] + df

df_count = 0
with open(export_file, 'w') as f:
    csv_writer = csv.writer(f, delimiter=',')
    for row in df:
        csv_writer.writerow(row)
        df_count += 1

print('Finished export to ' + export_file)
print('Rows:', df_count)

