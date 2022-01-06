# Big-Data-Bowl-2022-by-Luke-Wilson
Code and Images from Luke Wilson's 2022 Big Data Bowl Submission, "Introducing Expected Net Punt Yards (ENY) and Return Yards Over Expected (RYOE) to Evaluate Punters, Returners, and Coverage Teams"

Thank you for reading the README! This file contains instructions for using the code in the attached files. 

## Python Code
This code works by processing the data in steps, and between each step saving the result to a CSV file. The next file then reads the CSV file(s) and proceeds to the next step.

Make sure the play data, player data, and tracking data are together in the folder with the Python code. The code assumes these are named "plays.csv", "players.csv", "tracking2018.csv", "tracking2019.csv", and "tracking2020.csv" respectively.

The files are as follows.

HDEADER FILES:
1. helper.py
2. neural_network_functions.py
3. prepare_play_data.py
Note: These files mostly contain functions and are already imported in the appropriate places in the main files.

DATA PROCESSING FILES:
Run the following files in this order.
1. raw_data_work.py - reads "tracking2018.csv", "tracking2019.csv", and "tracking2020.csv"; exports to "punt_tracking_data.csv"
2. make_dataframe.py - reads "plays.csv" and "punt_tracking_data.csv"; exports to "df_for_nn.csv"
3. create_neural_networks - reads "df_for_nn.csv"; exports to "nn_eval.csv" (Evaluation of performance on returns), "classification_evaluation_nn.csv" (Evaluation of performance on classifying punt outcomes),  "return_parameters.csv" (Return Length Neural Network Parameters), "classify_parameters.csv" (Outcome Classification Neural Network Parameters)
4. expected_net_yards - reads "return_parameters.csv", "classify_parameters.csv", "players.csv", "df_for_nn.csv", and "punt_tracking_data.csv"; exports to "raw_evaluation.csv"
5. evaluate_players.py - reads "raw_evaluation.csv", 


CSV FILES:
A number of CSV files are included in the repository. There are the files that were produces when I last ran the program. If and when you run the program yourself, some of these (post-neural network, specifically) may look a bit different. This may lead to slightly different figures and tables.
