import csv
import math
from helper import *


# Function import_file
# Takes name (minus .csv) of file to read and an optional cap on the number of
# rows to read, plus several other vestigial default inputs. Returns a grid
# with plain csv data.
def import_file(bare_name, cap=100000):
    counts = 0
    
    grid = []

    print("Beginning to read csv " + bare_name + " now.")
    with open(bare_name + '.csv', 'r') as f:
        csv_reader = csv.reader(f, delimiter = ',')
        for row in csv_reader:
                grid.append(row)
                counts += 1
                if counts >= cap:
                    break
    print("Finished reading csv " + bare_name + "! :)")
    return grid



class Play:
    def __init__(self, id_):
        self.id = id_
        self.players = []
        self.grid = []
        self.type = 'not yet found'

    def is_during_play(self, row):
        for cell in row:
            if cell == self.id:
                return True
        return False

    def is_player_in_play(self, player_id):
        for man in self.players:
            if man[0] == player_id:
                return True
        return False

    def add_player(self, row):
        player_tuple = (row[9], row[10], row[12], row[13])
        self.players.append(player_tuple)
        return 0

    def add_row(self, row):
        row_player = row[9]
        row_event = row[8]
        row_player_tuple = [row[9], row[10], row[12], row[13]]

        if row_player_tuple in self.players:
            critical_player_index = self.players.index(row_player_tuple)


        else:
            self.players.append(row_player_tuple)
            self.grid.append([])
            critical_player_index = -1

        self.grid[critical_player_index].append(row)

        if row_event in ['punt', 'kickoff', 'field_goal', 'extra_point']:
            self.type = row_event

        return 0

    def process_grid(self):
        min_time = 99999999
        max_time = 0

        number_of_players = len(self.players)
        for player_number in range(number_of_players):
            for old_grid_row in self.grid[player_number]:
                old_row_time = time_to_number(unpack_date_time(old_grid_row))
                if old_row_time < min_time:
                    min_time = old_row_time
                if old_row_time > max_time:
                    max_time = old_row_time

        new_grid = []
        head_row = [self.id] + self.players
        new_grid.append(head_row)
        running_time_to_make_grid = min_time
        while running_time_to_make_grid <= max_time:
            blank_row_to_add = [str(running_time_to_make_grid)] + ['NA' for k in range(number_of_players)]
            #print('Adding blank row to new grid now')
            new_grid.append(blank_row_to_add)
            running_time_to_make_grid = increment_time(running_time_to_make_grid)
            #print('The new runnning time to make grid is', running_time_to_make_grid)

        for player_number in range(number_of_players):

            for old_grid_row in self.grid[player_number]:
                added_old_row_to_new_grid = False

                old_grid_row_time = time_to_number(unpack_date_time(old_grid_row))

                new_grid_length = len(new_grid)
                for new_grid_row in range(new_grid_length):
                    #print(new_grid[new_grid_row])
                    new_grid_time = float(new_grid[new_grid_row][0])
                    if new_grid_time == old_grid_row_time:
                        #print('match!')
                        gold_tuple = (old_grid_row[1], old_grid_row[2], old_grid_row[3], old_grid_row[4],
                                      old_grid_row[5], old_grid_row[6], old_grid_row[7], old_grid_row[8],
                                      old_grid_row[9])
                        new_grid[new_grid_row][player_number + 1] = gold_tuple
                        added_old_row_to_new_grid = True
                        break

                if not added_old_row_to_new_grid:
                    print('ALERT: Failed to add row of time', old_grid_row_time, '...')
                    print(old_grid_row)
                    print('... to new grid. More info...')
                    print('Min time: ', min_time, '  Max time: ', max_time, '  ...')
                    print('Length of new_grid:', new_grid_length, ' ...')
                    print('Head of new_grid: ')
                    print(new_grid[:5])
                    raise TypeError
                
        #print('Finished processing grid for play', self.id)
        self.grid = new_grid
        return 0


# Function load_plays
# Takes a file name, the name of an event in the desired plays, and an optional
# cap. Returns a list of play objects.
def load_plays(filename, event_in_wanted_plays):
    plays = []
    used_play_ids = []
    unwanted_play_ids = []
    play_count = 0
    with open(filename, 'r') as f:
        csv_reader = csv.reader(f, delimiter=',')
        for row in csv_reader:
            

            if row[15] + row[16] in unwanted_play_ids:
                continue

            if 'time' in row: # Does not read label row
                continue


            if row[15] + row[16] not in used_play_ids:
                new_play_id = row[15] + row[16]
                new_play = Play(new_play_id)
                used_play_ids.append(new_play_id)
                new_play.add_row(row)
                plays.append(new_play)
                play_in_list_index = -1
                play_count += 1

            else:
                current_play_id = row[15] + row[16]
                play_index = used_play_ids.index(current_play_id)
                current_play = plays[play_index]
                current_play.add_row(row)
                plays[play_index] = current_play
                play_in_list_index = play_index
            

            if plays[play_in_list_index].type not in ['not yet found', event_in_wanted_plays]:
                #print('unwanted play of type', plays[play_in_list_index].type)
                plays.pop(play_in_list_index)
                used_play_ids.pop(play_in_list_index)
                unwanted_play_ids.append(row[15] + row[16])
    return plays

# Function restore
# Takes a list of play objects and a file name. Returns nothing. Writes each
# play's grid to the file.
def restore(play_list, new_file_name):
    write_grid = []
    for play in play_list:
        write_grid.append([play.id])
        for grid_row in play.grid:
            write_grid.append(grid_row)

    with open(new_file_name, 'w') as f:
        csv_writer = csv.writer(f, delimiter=',')
        for row in write_grid:
            csv_writer.writerow(row)

    return 0
        


        
# interactive_package()
# No parameters. Asks the user for a list of file names, an event to watch for,
# a maximum number of plays to load from each file, and an export file name.
# Writes the tracking data to the export file.
# Enter load files: <Files names seperated with a space only. Include .csv>
# Wanted event: <Event that must appear in a play in order to load it (None for all plays)>
# Maximum Plays per File: <Integer maximum number of plays to load from each file>
# NEW file name: <Name of csv file for saving. Include .csv>
def interactive_package():
    
    file_names = input("Enter load files: ")
    wanted_event = input("Wanted event: ")

    critical_plays = []
    file_name_list = file_names.split(' ')
    for one_file_name in file_name_list:
        these_critical_plays = load_plays(one_file_name, wanted_event)
        critical_plays = critical_plays + these_critical_plays
        print('Finished loading critical plays in file', one_file_name, '...')
    print('Finished loading ALL critical plays...')

    for play in critical_plays:
        play.process_grid()
    print('Finished processing all grids')

    new_file_name = input("NEW file name: ")
    restore(critical_plays, new_file_name)
    print('Completed export to', new_file_name)



file_names = ['tracking2018.csv', 'tracking2019.csv', 'tracking2020.csv']
wanted_event = 'punt'

critical_plays = []
for one_file_name in file_names:
    these_critical_plays = load_plays(one_file_name, wanted_event)
    critical_plays = critical_plays + these_critical_plays
    print('Finished loading critical plays in file', one_file_name, '...')
print('Finished loading ALL critical plays...')

for play in critical_plays:
    play.process_grid()
print('Finished processing all grids')

new_file_name = 'punt_tracking_data.csv'
restore(critical_plays, new_file_name)
print('Completed export to', new_file_name)
    
