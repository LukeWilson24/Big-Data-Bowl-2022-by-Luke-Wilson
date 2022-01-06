from helper import *

team_names = {'NE': 'New England Patriots',
              'BUF': 'Buffalo Bills',
              'MIA': 'Miami Dolphins',
              'NYJ': 'New York Jets',
              'PIT': 'Pittsburgh Steelers',
              'BAL': 'Baltimore Ravens',
              'CIN': 'Cincinati Bengals',
              'CLE': 'Cleveland Browns',
              'IND': 'Indianapolis Colts',
              'TEN': 'Tennessee Titans',
              'HOU': 'Houston Texans',
              'JAX': 'Jacksonville Jaguars',
              'KC': 'Kansas City Chiefs',
              'LAC': 'Las Angeles Chargers',
              'LV': 'Las Vegas Raiders',
              'OAK': 'Oakland Raiders',
              'DEN': 'Denver Broncos',
              'DAL': 'Dallas Cowboys',
              'WAS': 'Washington Football Team',
              'PHI': 'Philadelphia Eagles',
              'NYG': 'New York Giants',
              'GB': 'Green Bay Packers',
              'MIN': 'Minnesota Vikings',
              'CHI': 'Chicago Bears',
              'DET': 'Detroit Lions',
              'TB': 'Tampa Bay Buccaneers',
              'NO': 'New Orleans Saints',
              'CAR': 'Carolina Panthers',
              'ATL': 'Atlanta Falcons',
              'ARI': 'Arizona Cardinals',
              'SF': 'San Franciso 49ers',
              'LA': 'Las Angeles Rams',
              'SEA': 'Seattle Seahawks'}

punter_dict = {}
returner_dict = {}
coverage_dict = {}
proportion_evaluation = []
return_yards = []
expected_return_yards = []

with open('raw_evaluation.csv', 'r') as f:
    csv_reader = csv.reader(f, delimiter = ',')
    for row in csv_reader:
        
        if 'Combined Play ID' in row: # Only true for top row
            label_row = row
            continue
        
        punter_id = extract('Kicker Id', row, label_row)
        returner_id = extract('Returner Id', row, label_row)
        team = extract('Kick Team', row, label_row)

        # Add to Punter
        eny = extract('Expected Net Yards', row, label_row)
        py = extract('Kick Length', row, label_row)
        rny = extract('Real Net Yards', row, label_row)
        outcome = extract('Play Result', row, label_row)
        if eny != 'NA' and py != 'NA' and rny != 'NA' and outcome != 'NA':
            if punter_id in punter_dict.keys():
                punter_dict[punter_id]['ENY'].append(float(eny))
                punter_dict[punter_id]['PY'].append(float(py))
                punter_dict[punter_id]['RNY'].append(float(rny))
                punter_dict[punter_id]['Outcome'].append(outcome)
            else:
                punter_dict[punter_id] = {'ENY': [float(eny)],
                                          'PY': [float(py)],
                                          'RNY': [float(rny)],
                                          'Outcome': [outcome]}
            

        # Add to Returner
        ery = extract('Expected Return Yards', row, label_row)
        ry = extract('Real Return Yards', row, label_row)
        if ery != 'NA' and ry != 'NA':
            ryoe = float(ry) - float(ery)
            proportion_evaluation.append(ryoe)
            return_yards.append(ry)
            expected_return_yards.append(ery)
            if returner_id in returner_dict.keys():
                returner_dict[returner_id]['RYOE'].append(float(ryoe))
                returner_dict[returner_id]['RY'].append(float(ry))
                
            else:
                returner_dict[returner_id] = {'RYOE': [float(ryoe)],
                                              'RY': [float(ry)]}

            if team in coverage_dict.keys():
                coverage_dict[team]['RYOE'].append(float(ryoe))
                coverage_dict[team]['RY'].append(float(ry))
            else:
                coverage_dict[team] = {'RYOE': [float(ryoe)],
                                        'RY': [float(ry)]}

p = len([k for k in proportion_evaluation if k > 0]) / len(proportion_evaluation)
print('Proportion of Returns Over Expected Length:', p)

def pull_player_info(nfl_id, file='players.csv'):
    with open(file, 'r') as f:
        csv_reader = csv.reader(f, delimiter=',')
        for row in csv_reader:
            if row[0] == nfl_id:
                name = row[6]
                position = row[5]
                college = row[4]
                birthday = row[3]
                height = row[1]
                weight = row[2]
                return [name, nfl_id] # Add more variables to export more info
    print('Failed to find player with nflId', nfl_id)


punter_eval = [['Name', 'NFL Id Number', 'Punts', 'Average ENY', 'Median ENY',
               'SD ENY', 'Q3 ENY', 'Q1 ENY', 'Adjusted Average ENY', 'Punt Yards',
                'Avg Punt Yards', 'Net Yards', 'Average Net Yards',
                'Return %', 'Fair Catch %', 'Downed %']] # Add labels if using more player data
for nfl_id, stat_dict in punter_dict.items():
    
    eny_list = stat_dict['ENY']
    py_list = stat_dict['PY']
    rny_list = stat_dict['RNY']
    outcome_list = stat_dict['Outcome']
    
    player_info = pull_player_info(nfl_id)
    punts = len(eny_list)
    avg_eny = round(sum(eny_list) / len(eny_list), 2)
    median_eny = round(np.median(eny_list), 2)
    stdev_eny = round(np.std(eny_list), 2)
    upper_quartile_eny = round(np.percentile(eny_list, 75, interpolation = 'midpoint'), 2)
    lower_quartile_eny = round(np.percentile(eny_list, 25, interpolation = 'midpoint'), 2)
    adj_avg_eny = round(sum(eny_list) / (len(eny_list) + 1), 2)
    
    total_py = round(sum(py_list), 2)
    avg_py = round(sum(py_list) / len(py_list), 2)
    
    total_rny = round(sum(rny_list), 2)
    avg_rny = round(sum(rny_list) / len(rny_list), 2)

    return_perc = round(len([k for k in outcome_list if k == 'Return']) / len(outcome_list), 2)
    fair_catch_perc = round(len([k for k in outcome_list if k == 'Fair Catch']) / len(outcome_list), 2)
    land_perc = round(len([k for k in outcome_list if k not in ('Return', 'Fair Catch')]) / len(outcome_list), 2)
    
    export_row = player_info + [punts, avg_eny, median_eny, stdev_eny,
                                upper_quartile_eny, lower_quartile_eny, adj_avg_eny, total_py, avg_py, total_rny, avg_rny, return_perc, fair_catch_perc,
                                land_perc]
    punter_eval.append(export_row)

    


returner_eval = [['Name', 'NFL Id Number', 'Returns', 'Average RYOE', 'Median RYOE',
               'SD RYOE', 'Q3 RYOE', 'Q1 RYOE', 'Adjusted Average RYOE','Returns Over Expected',
                  'Return Proportion Over Expected', 'Return Yards', 'Average Return Yards']] # Add labels if using more player data
for nfl_id, stat_dict in returner_dict.items():

    ryoe_list = stat_dict['RYOE']
    print(sum(ryoe_list))
    ry_list = stat_dict['RY']
    
    player_info = pull_player_info(nfl_id)
    returns = len(ryoe_list)
    avg_ryoe = round(sum(ryoe_list) / len(ryoe_list), 2)
    median_ryoe = round(np.median(ryoe_list), 2)
    stdev_ryoe = round(np.std(ryoe_list), 2)
    upper_quartile_ryoe = round(np.percentile(ryoe_list, 75, interpolation = 'midpoint'), 2)
    lower_quartile_ryoe = round(np.percentile(ryoe_list, 25, interpolation = 'midpoint'), 2)
    adj_avg_ryoe = round(sum(ryoe_list) / (len(ryoe_list) + 1), 2)
    over_expected_returns = len([x for x in ryoe_list if x > 0])
    over_expected_proportion = round(over_expected_returns / returns, 3)

    total_ry = sum(ry_list)
    avg_ry = round(sum(ry_list) / len(ry_list), 2)
    
    export_row = player_info + [returns, avg_ryoe, median_ryoe, stdev_ryoe,
                                upper_quartile_ryoe, lower_quartile_ryoe, adj_avg_ryoe,
                                over_expected_returns, over_expected_proportion, total_ry, avg_ry]
    returner_eval.append(export_row)

team_eval = [['Team', 'Abbreviation', 'Returns Against', 'Average RYOE', 'Median RYOE',
               'SD RYOE', 'Q3 RYOE', 'Q1 RYOE', 'Adjusted Average RYOE','Returns Under Expected',
                  'Return Proportion Under Expected', 'Return Yards Against', 'Avg Return Yards Against']] # Add labels if using more player data
for abbr, stat_dict in coverage_dict.items():

    ryoe_list = stat_dict['RYOE']
    ry_list = stat_dict['RY']
    
    team = team_names[abbr]
    returns = len(ryoe_list)
    avg_ryoe = round(sum(ryoe_list) / len(ryoe_list), 2)
    median_ryoe = round(np.median(ryoe_list), 2)
    stdev_ryoe = round(np.std(ryoe_list), 2)
    upper_quartile_ryoe = round(np.percentile(ryoe_list, 75, interpolation = 'midpoint'), 2)
    lower_quartile_ryoe = round(np.percentile(ryoe_list, 25, interpolation = 'midpoint'), 2)
    adj_avg_ryoe = round(sum(ryoe_list) / (len(ryoe_list) + 1), 2)
    under_expected_returns = len([x for x in ryoe_list if x < 0])
    under_expected_proportion = round(under_expected_returns / returns, 3)

    total_ry = sum(ry_list)
    avg_ry = round(sum(ry_list) / len(ry_list), 2)
    
    export_row = [team, abbr, returns, avg_ryoe, median_ryoe, stdev_ryoe,
                  upper_quartile_ryoe, lower_quartile_ryoe, adj_avg_ryoe,
                  under_expected_returns, under_expected_proportion, total_ry, avg_ry]
    
    team_eval.append(export_row)   


punter_evaluation_file = 'evaluated_punters.csv'
returner_evaluation_file = 'evaluated_returners.csv'
team_evaluation_file = 'evaluated_teams.csv'

file_names = [punter_evaluation_file, returner_evaluation_file, team_evaluation_file]
evaluations = [punter_eval, returner_eval, team_eval]
for n in range(3):
    with open(file_names[n], 'w') as f:
        csv_writer = csv.writer(f, delimiter=',')
        csv_writer.writerows(evaluations[n])
        print('Finished export to', file_names[n])


with open('evaluate_ery.csv', 'w') as f:
    csv_writer = csv.writer(f, delimiter = ',')
    csv_writer.writerow(['ry', 'ery'])
    for i in range(len(return_yards)):
        csv_writer.writerow([return_yards[i], expected_return_yards[i]])
