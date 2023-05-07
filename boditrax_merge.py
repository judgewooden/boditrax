"""
    Merge boditrax2 with boditrax1 bmi, bonemass, fatmass, metabolicage, musclemass & bodyweight data
"""
import os
import pandas as pd

if __name__ == "__main__":
    df1 = pd.read_csv("boditrax2.csv")
    df1['date'] = pd.to_datetime(df1['date']).dt.tz_localize('Europe/Amsterdam').dt.strftime('%Y-%m-%d %H:%M:%S')
    df1['date'] = pd.to_datetime(df1['date'])
    df1['date'] = df1['date'] + pd.Timedelta(hours=1)
    df1.set_index('date', inplace=True)
    df1 = df1.rename(columns={
        'date': 'date',
        'BMI': 'bmi',
        'Bone': 'bonemass',
        'Fat': 'fatmass',
        'MetabolicAge': 'metabolicage',
        'Muscle': 'musclemass',
        'Weight': 'bodyweight'
    })

    df2 = pd.read_csv("boditrax.csv")
    df2['date'] = pd.to_datetime(df2['date'])
    df2.set_index('date', inplace=True)

    MERGED_FILE = "boditrax_merge.csv"
    df3 = pd.DataFrame()
    if os.path.exists(MERGED_FILE):
        df3 = pd.read_csv(MERGED_FILE)
        df3['date'] = pd.to_datetime(df3['date'])
        df3.set_index('date', inplace=True)

    df4 = pd.concat([df1, df2, df3])
    df4 = df4[~df4.index.duplicated(keep='first')]
    df4.sort_index(inplace=True)
    df4 = df4.loc[:, ['bmi', 'bonemass', 'fatmass', 'metabolicage', 'musclemass', 'bodyweight']]
    df4.to_csv(MERGED_FILE)
