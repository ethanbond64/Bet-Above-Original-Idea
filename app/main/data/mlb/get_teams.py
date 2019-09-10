from sportsreference.mlb.schedule import Schedule
from sportsreference.mlb.boxscore import Boxscore
from sportsreference.mlb.teams import Teams
import pandas as pd
import numpy as np
from datetime import datetime

weekday = {
    'Sunday':1,
    'Monday':2,
    'Tuesday':3,
    'Wednesday':4,
    'Thursday':5,
    'Friday':6,
    'Saturday':7
}


def get_month(str):
    return datetime.strptime(str," %B %d, %Y").month

def get_day(str):
    return datetime.strptime(str," %B %d, %Y").day

def to_duration(str):
    t1 = datetime.strptime(str, '%H:%M')
    t2 = datetime(1900,1,1)

    return (t1-t2).total_seconds() / 60.0

## FINDING ALL THE BOXSCORES FOR THE TEAM

teams = Teams()
for team in teams:
    abr = team.abbreviation
    sched = Schedule(abr)

    dfs = []
    for game in sched:
        if len(game.boxscore_index) == 16:
            dfs.append(Boxscore(game.boxscore_index).dataframe)

    mega_df = pd.concat(dfs,ignore_index=True)
    df = mega_df
    del df['attendance']
    for col in df:
        if col[:4] == 'away':
            df[col[5:]] = np.where(df['venue']==df['venue'].mode()[0],df["home"+col[4:]],df[col])
            del df["home"+col[4:]]
            del df[col]


    df['home'] = np.where(df['venue']==df['venue'].mode()[0],1,0)
    del df['venue']

    df['weekday'] = df["date"].str.split(",", n = 1, expand = True)[0]
    df = df.replace({"weekday":weekday})
    df['date'] = df["date"].str.split(",", n = 1, expand = True)[1]
    df['month'] = df['date'].apply(get_month)
    df['day'] = df['date'].apply(get_day)
    df['time_of_day'] = np.where(df['time_of_day']=='Day',0,1)
    df['duration'] = df['duration'].apply(to_duration)
    del df['date']
    df['opponent'] = np.where(df['winning_abbr'] == abr,df['losing_abbr'],df['winning_abbr'])
    df['won'] = np.where(df['winning_abbr'] == abr,1,0)
    del df['winner'],df['winning_name'],df['winning_abbr'],df['losing_name'],df['losing_abbr'],df['time']
    print(abr)
    print(df)
    newcsv = abr + '.csv'
    df.to_csv(newcsv,index=False)
print('EL FIN')
