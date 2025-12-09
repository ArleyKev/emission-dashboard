import pandas as pd

def aggregate_time_series(df: pd.DataFrame, start_year=None, end_year=None, sector=None, region=None):
    d = df.copy()
    if start_year:
        d = d[d['year'] >= int(start_year)]
    if end_year:
        d = d[d['year'] <= int(end_year)]
    if sector:
        d = d[d['sector'] == sector]
    if region:
        d = d[d['region'] == region]
    ts = d.groupby(['year','sector'], as_index=False)['emissions_tCO2e'].sum()
    pivot = ts.pivot(index='year', columns='sector', values='emissions_tCO2e').fillna(0).reset_index()
    return pivot.to_dict(orient='records')

def breakdown_by_industry(df: pd.DataFrame, year, sector):
    d = df[(df['year'] == int(year)) & (df['sector'] == sector)]
    out = d.groupby('industry', as_index=False)['emissions_tCO2e'].sum().to_dict(orient='records')
    return out
