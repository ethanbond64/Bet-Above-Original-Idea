import csv
import pandas as pd
import numpy as np

def softMax(arr):
    exps = np.exp(arr)
    return exps / np.sum(exps)

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def feature_rank(filename,selected_features):

    df = pd.read_csv(filename)
    if type(selected_features) == str:
        selected_features = [selected_features]
    selected_features = ['Team','Strength']+selected_features
    df = pd.DataFrame(df[selected_features])

    df['Total'] = 0

    for col in df:
        if col != 'Team' and col != 'Strength':
            df[col] = df[col]/df[col].median()
            df['Total'] += df[col]

    df['Total'] = (df['Total']/df['Total'].median())
    df['Total'] += df['Strength']/df['Strength'].size

    df = df.sort_values(by=['Total'],ascending=False)
    df = df.reset_index(drop=True)
    df.index += 1

    return df[['Team','Total']]
