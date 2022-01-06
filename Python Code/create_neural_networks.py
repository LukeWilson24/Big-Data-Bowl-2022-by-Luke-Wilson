from helper import *
from sklearn.metrics import mean_squared_error

# --------------- Universal functions for neural networks ---------------- #

def try_float(string):
    try:
        new = float(string)
        return new
    except TypeError:
        return string

def smart_enough_trim(row, labels, desired_labels):
    keep_indecies = [labels.index(l) for l in desired_labels]
    new_row = []
    for i in keep_indecies:
        entry = row[i]
        if '[' in entry and ']' in entry:
            entry = entry.replace('[', '')
            entry = entry.replace(']', '')
            entry = [try_float(k) for k in entry.split(', ')]
        else:
            entry = try_float(entry)
        new_row.append(entry)
    return new_row
            

# Takes a row of imported data, the column labels of that data, and the column
# labels corresponding to the cells that should be kept. Returns a list.
def trim_row(row, label_row, desired_labels, makefloat=True):
    trimmed_row = []
    for c in range(len(row)):
        if label_row[c] in desired_labels:
            if makefloat:
                if '[' in row[c] and ']' in row[c]:
                    row[c] = row[c][1:-1]
                    trimmed_row.append([int(k) for k in row[c].split(', ')])
                else:
                    trimmed_row.append(float(row[c]))
            else:
                trimmed_row.append(row[c])
    return trimmed_row

def init_parameters(layer_sizes):
    parameters= {}
    for i in range(1, len(layer_sizes)):
        parameters['W'+ str(i)] = np.random.randn(layer_sizes[i], layer_sizes[i-1]) / 100
        parameters['B'+ str(i)] = np.random.randn(layer_sizes[i], 1) / 100
    return parameters

def compute_cost(predicted_values, learn_y_T):
    layer_count = int(len(predicted_values) / 2)
    predict_y = predicted_values['A' + str(layer_count)]
    cost = 1 / (2 * len(learn_y_T.T)) * np.sum(np.square(predict_y - learn_y_T))
    return cost


def backward_propogation(parameters, matrix_values, learn_x_T, learn_y_T):
    layer_count = int(len(parameters) / 2)
    m = len(learn_y_T.T)
    gradients = {}
    for i in range(layer_count, 0, -1):
        if i == layer_count:
            dA = 1 / m * (matrix_values['A' + str(i)] - learn_y_T)
            dZ = dA
        else:
            dA = np.dot(parameters['W' + str(i + 1)].T, dZ)
            dZ = np.multiply(dA, np.where(matrix_values['A' + str(i)] >= 0, 1, 0))
        if i == 1:
            gradients['W' + str(i)] = 1/ m * np.dot(dA, learn_x_T.T)
            gradients['B' + str(i)] = 1 / m * np.sum(dZ, axis = 1, keepdims=True)
        else:
            gradients['W' + str(i)] = 1 / m * np.dot(dZ, matrix_values['A' + str(i-1)].T)
            gradients['B' + str(i)] = 1 / m * np.sum(dZ, axis = 1, keepdims=True)
    return gradients

def update_parameters(parameters, gradients, learning_rate):
    layer_count = len(parameters) // 2
    parameters_updated = {}
    for i in range(1, layer_count + 1):
        parameters_updated['W' + str(i)] = parameters['W' + str(i)] - learning_rate * gradients['W' + str(i)]
        parameters_updated['B' + str(i)] = parameters['B' + str(i)] - learning_rate * gradients['B' + str(i)]
    return parameters_updated



def binary(x):
    if x > 0.5:
        return 1
    else:
        return 0


def sigmoid(x):
    if x > 700:
        return 1
    elif x < -700:
        return 1 / ( 1 + np.exp(-700) )
    else:
        return 1 / ( 1 + np.exp(-1 * x) )

def export_evaluation(values_test, test_y, layer_count, file='nn_eval.csv'):
    predicted_values = values_test['A' + str(layer_count - 1)][0]
    print(predicted_values)
    real_values = test_y
    with open(file, 'w') as f:
        csv_writer = csv.writer(f, delimiter=',')
        csv_writer.writerow(['Predicted', 'Real'])
        for row in range(len(predicted_values)):
            x = predicted_values[row]
            y = real_values[row]
            csv_writer.writerow([x, y])
    print('Finished Exporting evaluation to', file)
            
            

def model(learn_x, learn_y, layer_sizes, learning_reps, learning_rate, typ):
    parameters = init_parameters(layer_sizes)
    # COMMENT ABOVE LINE AND UNCOMMENT FOLLOWING LINE TO LOAD PARAMETERS INSTEAD OF RESTARTING
    #parameters = load_network('FILE_NAME_HERE.csv')
    
    i = 0
    while i < learning_reps:
        i += 1
        if typ == 'r':
            matrix_values = forward_propogation_returns(learn_x.T, parameters)
        elif typ == 'c':
            matrix_values = forward_propogation_classification(learn_x.T, parameters)
        cost = compute_cost(matrix_values, learn_y.T)
        gradients = backward_propogation(parameters, matrix_values, learn_x.T, learn_y.T)
        parameters = update_parameters(parameters, gradients, learning_rate)
        if i % 1000 == 0:
            print('Cost at iteration ' + str(i + 1) + ' = ' + str(cost) + '\n')
            #export_classification_evaluation(test_x, test_y, parameters, file='evaluate_classification_' + str(i) + '.csv')
        if i == 45000 and cost > 26 and typ == 'c':
            i = 0
            parameters = init_parameters(layer_sizes)
    return parameters


def compute_accuracy_returns(learn_x, learn_y, test_x, test_y, parameters, export=False):
    matrix_values_learn = forward_propogation_returns(learn_x.T, parameters)
    matrix_values_test = forward_propogation_returns(test_x.T, parameters)
    learn_accuracy = np.sqrt(mean_squared_error(learn_y, matrix_values_learn['A' + str(len(layer_sizes)-1)].T))
    test_accuracy = np.sqrt(mean_squared_error(test_y, matrix_values_test['A' + str(len(layer_sizes)-1)].T))
    if export:
        export_evaluation(matrix_values_test, test_y, (len(parameters) // 2) + 1)
    abs_vectorize = np.vectorize(abs)
    error = np.sum(abs_vectorize(matrix_values_test['A' + str(len(layer_sizes)-1)].T - test_y)) / len(test_y)
    
    return learn_accuracy, test_accuracy, error

def export_classification_evaluation(test_x, test_y, parameters, file='evaluate_classification_nn.csv'):
    predicted_y = forward_propogation_classification(test_x.T, parameters)
    
    evaluation = [['result', 'pred_result', 'return_prob', 'fair_catch_prob', 'land_prob']]
    for r in range(len(test_y)):
        if list(test_y[r, :]) == [1, 0, 0]:
            result = 'Return'
        elif list(test_y[r, :]) == [0, 1, 0]:
            result = 'Fair Catch'
        elif list(test_y[r, :]) == [0, 0, 1]:
            result = 'Land'
        return_prob = predicted_y['A3'][0, r]
        fair_catch_prob = predicted_y['A3'][1, r]
        land_prob = predicted_y['A3'][2, r]
        
        p_row = [return_prob, fair_catch_prob, land_prob]
        if return_prob == max(p_row):
            pred_result = 'Return'
        elif fair_catch_prob == max(p_row):
            pred_result = 'Fair Catch'
        elif land_prob == max(p_row):
            pred_result = 'Land'

        new_row = [result, pred_result, return_prob, fair_catch_prob, land_prob]
        #print(new_row)
        evaluation.append(new_row)
    with open(file, 'w') as f:
        csv_writer = csv.writer(f, delimiter=',')
        csv_writer.writerows(evaluation)
    print('Finished Exporting evaluation to', file)
    


# --------------- Functions for specific neural networks ---------------- #

# Takes a proportion of data to save for testing (float between 1 and 0)
# and returns a dictionary containing the learning and test data.
def import_classification_data(file, y_label):
    array_labels = ['nn_hang_time', 'nn_vertical_distance', 'nn_yards_to_sideline',
                    'nn_yards_to_goal_line', 'nn_returner_displacement', 
                    'is_returned', 'is_in_play']
    test_grid = []
    learn_grid = []
    with open(file, 'r') as f:
        csv_reader = csv.reader(f, delimiter = ',')
        for row in csv_reader:
            if y_label in row:
                label_row = row
                proper_length = len(row)
                continue
            
            if len(row) != proper_length:
                continue

            if extract('is_in_play', row, array_labels) == '0':
                continue
            
            if 'NA' not in [row[label_row.index(k)] for k in array_labels]:
                if row[0][:4] == '2021' or (row[0][:4] == '2020' and row[0][4:6] not in ('01', '02')):
                    test_grid.append(smart_enough_trim(row, label_row, array_labels))    
                else:
                    learn_grid.append(smart_enough_trim(row, label_row, array_labels)) 

    y_index = array_labels.index(y_label)
    
    learn_array = np.array(learn_grid, dtype=object)
    learn_y = np.stack(learn_array[:, y_index])
    learn_x = learn_array[:, :y_index]
    
    test_array = np.array(test_grid, dtype=object)
    test_y = np.stack(test_array[:, y_index])
    test_x = test_array[:, :y_index]
    return {'Learn_x': learn_x,
            'Learn_y': learn_y,
            'Test_x': test_x,
            'Test_y': test_y}

def import_return_data(file, y_label, upper_y_limit=110):
    array_labels = ['nn_hang_time', 'nn_vertical_distance', 'nn_yards_to_sideline',
                    'nn_yards_to_goal_line', 'nn_returner_displacement',
                    'kickReturnYardage']
    assert y_label == array_labels[-1]
    test_grid = []
    learn_grid = []
    with open(file, 'r') as f:
        csv_reader = csv.reader(f, delimiter = ',')
        for row in csv_reader:
            if y_label in row:
                label_row = row
                proper_length = len(row)
                continue

            if len(row) != proper_length:
                continue

            
            if 'NA' not in [row[label_row.index(k)] for k in array_labels]:
                if row[0][:4] == '2021' or (row[0][:4] == '2020' and row[0][4:6] not in ('01', '02')):
                    test_grid.append(trim_row(row, label_row, array_labels))    
                else:
                    if float(extract(y_label, row, label_row)) > upper_y_limit:
                        continue
                    learn_grid.append(trim_row(row, label_row, array_labels))
    learn_array = np.array(learn_grid, dtype=object)
    learn_y = learn_array[:, 0]
    learn_x = learn_array[:, 1:]
    test_array = np.array(test_grid, dtype=object)
    test_x = test_array[:, 1:]
    test_y = test_array[:, 0]
    return {'Learn_x': learn_x,
            'Learn_y': learn_y,
            'Test_x': test_x,
            'Test_y': test_y}

# UNCOMMENT BELOW THIS LINE AND RUN TO CREATE NEURAL NETWORKS

### Make Neural Network to predict return/fair catch/let go
##data = import_classification_data('df_for_nn.csv', 'is_returned')
##print('Importing Data from df_for_nn.csv')
##learn_x = data['Learn_x']
##learn_y = data['Learn_y']
##test_x = data['Test_x']
##test_y = data['Test_y']
##layer_sizes = [5, 4, 4, 3]
##learning_reps = 50000
##learning_rate = 12
##network_parameters = model(learn_x, learn_y, layer_sizes, learning_reps, learning_rate, typ='c')
##export_classification_evaluation(test_x, test_y, network_parameters)
##save_network(network_parameters, 'classify_parameters.csv')
##
### Make Neural Network to predict return length
##data = import_return_data('df_for_nn.csv', 'kickReturnYardage', upper_y_limit=25)
##print('Importing Data from df_for_nn.csv')
##learn_x = data['Learn_x']
##learn_y = data['Learn_y']
##test_x = data['Test_x']
##test_y = data['Test_y']
##print(test_x[:5])
##layer_sizes = [5, 4, 4, 1]
##learning_reps = 20000
##learning_rate = 3
##network_parameters = model(learn_x, learn_y, layer_sizes, learning_reps, learning_rate, typ='r')
##for key, item in network_parameters.items():
##    print(key)
##    print(item)
##x_vector = np.array([4.4, 41.2, 24.6, 16.74, 5.9])
##print(forward_propogation_returns(x_vector, network_parameters))
##
##compute_accuracy_returns(learn_x, learn_y, test_x, test_y, network_parameters, export=True)
##save_network(network_parameters, 'return_parameters.csv')
