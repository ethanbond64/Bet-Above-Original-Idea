import pickle
import pandas as pd
import numpy as np

def compare_teams(team1,team2,home,day,month,time_of_day,weekday):
    team1_file = team1 + '.csv'
    team2_file = team2 + '.csv'

    team1_df = pd.read_csv(team1_file)
    team2_df = pd.read_csv(team2_file)

    team1_df = team1_df.mean().to_frame().T
    team2_df = team2_df.mean().to_frame().T

    team1_df = team1_df.rename(columns={'won':'record'})
    team2_df = team2_df.rename(columns={'won':'record'})

    del team1_df['unknown_bat_type'], team2_df['unknown_bat_type']

    fin_df = team1_df / team2_df
    # print(fin_df)
    fin_df['home'] = home
    fin_df['day'] = day
    fin_df['month'] = month
    fin_df['time_of_day'] = time_of_day
    fin_df['weekday'] = weekday
    fin_df = fin_df.fillna(0)
    # fin_df = fin_df.replace(np.inf, 0, inplace=True)
    print(fin_df)
    with open('training\\mlb_model.pkl','rb') as f:
        clf = pickle.load(f)

    probabilities = clf.predict_proba(fin_df)

    # Returns probability that team1 wins
    return probabilities[0][1]
    # return clf.predict(fin_df)
