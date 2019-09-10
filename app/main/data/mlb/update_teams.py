from sportsreference.mlb.schedule import Schedule
from sportsreference.mlb.boxscore import Boxscore
from sportsreference.mlb.teams import Teams
import pandas as pd
import numpy as np
from datetime import datetime, date

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


today = date.today()
teams = Teams()
for team in teams:
    abr = team.abbreviation
    sched = Schedule(abr)

    #open csv
    #get the last row month and day
    fname = abr + '.csv'
    old_df = pd.read_csv(fname)
    new_rows = []

    last_month = int(old_df.tail(1)['month'])
    last_day = int(old_df.tail(1)['day'])
    last_date = datetime(today.year,last_month,last_day)

    for game in sched:
        if game.datetime > last_date and len(game.boxscore_index) == 16:
            new_rows.append(Boxscore(game.boxscore_index).dataframe)

    if len(new_rows) == 0:
        continue
    elif len(new_rows) == 1:
        new_df = new_rows[0]
    else:
        new_df = pd.concat(new_rows,ignore_index=True)

    del new_df['attendance']
    for col in new_df:
        if col[:4] == 'away':
            new_df[col[5:]] = np.where(new_df['venue']==new_df['venue'].mode()[0],new_df["home"+col[4:]],new_df[col])
            del new_df["home"+col[4:]]
            del new_df[col]

    new_df['home'] = np.where(new_df['venue']==new_df['venue'].mode()[0],1,0)
    del new_df['venue']

    new_df['weekday'] = new_df["date"].str.split(",", n = 1, expand = True)[0]
    new_df = new_df.replace({"weekday":weekday})
    new_df['date'] = new_df["date"].str.split(",", n = 1, expand = True)[1]
    new_df['month'] = new_df['date'].apply(get_month)
    new_df['day'] = new_df['date'].apply(get_day)
    new_df['time_of_day'] = np.where(new_df['time_of_day']=='Day',0,1)
    new_df['duration'] = new_df['duration'].apply(to_duration)
    del new_df['date']
    new_df['opponent'] = np.where(new_df['winning_abbr'] == abr,new_df['losing_abbr'],new_df['winning_abbr'])
    new_df['won'] = np.where(new_df['winning_abbr'] == abr,1,0)
    del new_df['winner'],new_df['winning_name'],new_df['winning_abbr'],new_df['losing_name'],new_df['losing_abbr'],new_df['time']

    fin_df = pd.concat([old_df,new_df],ignore_index=True)
    newcsv = abr + '.csv'
    fin_df.to_csv(newcsv,index=False)
print('EL FIN')
