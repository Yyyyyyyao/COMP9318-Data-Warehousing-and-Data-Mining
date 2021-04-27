import numpy as np
import pandas as pd
from sklearn.svm import SVR
from sklearn.metrics import mean_absolute_error
import math

## Project-Part1
def predict_COVID_part1(svm_model, train_df, train_labels_df, past_cases_interval, past_weather_interval, test_feature):
    
    # get training labels 
    # size 162x2
    feature_matrix_y_for_max_interval = train_labels_df[30:]
    
    # only start from day 30 for max interval 
    # so it can get the past days
    draft_df = train_df.copy()

    # except the day 
    # all the remaining needs to have past values
    to_expand_list = draft_df.columns[1:]
    expanding_list = []
    for word in to_expand_list:
        for i in range(1,31):
            to_add = str(word+"-{}".format(i)) # into format like max_temp-1
            expanding_list.append(to_add)

    # create the data with 30days past records
    i = 30
    add_rows = []
    while i < train_df.shape[0]:
        row = []
        for word in expanding_list:
            feature,day_number = word.split('-')
            row.append(train_df.iloc[i-int(day_number)][feature]) # this is max_temp-1 is 1 day before the target day
        add_rows.append(row)
        i += 1

    # create the dataframe which has the max_interval records
    # size: 162x510
    feature_matrix_X_for_max_interval = pd.DataFrame(data=add_rows, columns=expanding_list)

    # For part-1, we only need the ['max_temp', 'max_dew', 'max_humid', 'dailly_cases']
    # And with a preset past_cases_interval and past_weather_interval
    selected_keywords = ['max_temp', 'max_dew', 'max_humid', 'dailly_cases']
    selected_columns = []
    for word in selected_keywords:
        i = 1
        if (word == 'dailly_cases'):
            while (i <= past_cases_interval):
                selected_columns.append(word+"-{}".format(i))
                i +=1
            
        else:
            while (i <= past_weather_interval):
                selected_columns.append(word+"-{}".format(i))
                i +=1

    # get the part1 training data
    part_1_feature_X = feature_matrix_X_for_max_interval[selected_columns]

    # get the part1 testing data
    part_1_test_features_X = test_feature[selected_columns].values.reshape(1, -1)

    # fit data to the SVM model
    # do predicting
    svm_model.fit(part_1_feature_X, feature_matrix_y_for_max_interval["dailly_cases"])
    a = svm_model.predict(part_1_test_features_X)

    # we only take the floor integer of the predicted value
    return math.floor(a)

## Project-Part2
def predict_COVID_part2(train_df, train_labels_df, test_feature):

    # get training labels 
    # size 162x2
    feature_matrix_y_for_max_interval = train_labels_df[30:]

    # only start from day 30 for max interval 
    # so it can get the past days
    draft_df = train_df.copy()

    # except the day 
    # all the remaining needs to have past values
    to_expand_list = draft_df.columns[1:]
    expanding_list = []
    for word in to_expand_list:
        for i in range(1,31):
            to_add = str(word+"-{}".format(i)) # into format like max_temp-1
            expanding_list.append(to_add)

    # create the data with 30days past records
    i = 30
    add_rows = []
    while i < train_df.shape[0]:
        row = []
        for word in expanding_list:
            feature,day_number = word.split('-')
            row.append(train_df.iloc[i-int(day_number)][feature]) # this is max_temp-1 is 1 day before the target day
        add_rows.append(row)
        i += 1

    # create the dataframe which has the max_interval records
    # size: 162x510
    feature_matrix_X_for_max_interval = pd.DataFrame(data=add_rows, columns=expanding_list)

    past_cases_interval = 15
    past_weather_interval_temp = 10
    past_weather_interval_dew = 15
    past_weather_interval_humid = 30

    kernel = 'poly'
    C = 17000
    ## Set hyper-parameters for the SVM Model
    svm_model = SVR()
    svm_model.set_params(**{'kernel': kernel, 'degree': 1, 'C': C,
                            'gamma': 'scale', 'coef0': 7.5, 'tol': 2.5, 'epsilon': 0.04})

    selected_keywords = ['max_temp', 'avg_temp', 'min_temp', 'max_dew', 'avg_dew', 'min_dew', 'max_humid', 'avg_humid', 'min_humid', 'dailly_cases']
    selected_columns = []
    for word in selected_keywords:
        i = 1
        if (word == 'dailly_cases'):
            while (i <= past_cases_interval):
                selected_columns.append(word+"-{}".format(i))
                i +=1
        elif 'temp' in word:
            while (i <= past_weather_interval_temp):
                selected_columns.append(word+"-{}".format(i))
                i +=1
        elif 'dew' in word:
            while (i <= past_weather_interval_dew):
                selected_columns.append(word+"-{}".format(i))
                i +=1
        elif 'humid' in word:
            while (i <= past_weather_interval_humid):
                selected_columns.append(word+"-{}".format(i))
                i +=1
                        
    # get the part1 training data
    part_2_feature_X = feature_matrix_X_for_max_interval[selected_columns]


    # get the part1 testing data 
    part_2_test_features_X = test_feature[selected_columns].values.reshape(1, -1)

    # Model:
    svm_model.fit(part_2_feature_X, feature_matrix_y_for_max_interval["dailly_cases"])
    preds = svm_model.predict(part_2_test_features_X)

    return math.floor(preds)



