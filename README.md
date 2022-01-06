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
5. evaluate_players.py - reads "raw_evaluation.csv" and "players.csv", exports to "evaluated_punters.csv", "evaluated_returners.csv", and "evaluated_teams.csv"


CSV FILES:
A number of CSV files are included in the repository. There are the files that were produced when I last ran the program. If and when you run the program yourself, some of these (post-neural network, especially) may look a bit different. This may lead to slightly different figures and tables.

## R Code
To reproduce the figures in the report, see the three attached R files and "graph_me.csv." The tracking data for the relvant play is stored in this CSV file. Run R_work.R to create and save the animation. This file reads from fbf.R.

To reproduce the charts, make sure bdb_figures.R is in the same folder as all the CSV files produced by the Python code above (you will need to run that first, or use the CSV files I have attached). Then run bdb_figures.R. The following variables should now contain the plots.

1. return_plot
2. return_hist
3. c_plot
4. roll_plot
5. ny_plot
6. punters_tab
7. returners_tab
8. teams_tab

### Extra Note
I used IDLE for Python code and RStudio for R code. I am not a computer scientist - I understand *that* these things work with my configuration, not how they work. I can offer no advice on how to set up your workspace.

