import pandas as pd
from sportsreference.mlb.teams import Teams

teams = Teams()
for team in teams:
    abr = team.abbreviation
    oldfile = abr + '.csv'
    df = pd.read_csv(oldfile)
    df['record'] = df['won']
    for col in df:
        if col not in ['time_of_day','home','weekday','won','opponent','month','day',]:
            df[col] = df[col].cumsum().shift().fillna(0).div(df.index.to_series(),axis=0)

    df = df.iloc[1:]
    newfile = 'training\\' + abr + '_train.csv'
    df.to_csv(newfile,index=False)
print('EL FIN')
