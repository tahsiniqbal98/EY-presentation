import pandas as pd
import time
import datetime
import glob
import os
import statistics
from collections import Counter

path = 'C:/Users/Tahsin/Desktop/EY Analysis/simulations'
os.chdir(path)

df = pd.read_csv('technical_analysis_full_list_v2.csv')
print('imported')
print(type(df['Date'][0]))
df = df.reset_index(drop=True)

stock_symbols = list(set(df['Symbol']))
stock_symbols = sorted(stock_symbols)

empty_col = ['NA'] * df.shape[0]
print('sorted')

just_dates = [
    datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').date()
    for x in df["Date"]
]
just_dates = pd.Series(just_dates)
just_dates = [
    datetime.datetime.strftime(x, '%Y-%m-%d %H:%M:%S') for x in just_dates
]
date_and_symbol = just_dates + df['Symbol']

df.insert(18, "date_and_symbol", date_and_symbol, True)
print('starting major drops')
a = df.query('TRADE_ENTRY == "YES"').date_and_symbol.unique()
df = df.query('date_and_symbol in @a')
print('all rows dropped')
del df['date_and_symbol']

# df = df.sort_values(by=["Symbol", "Date"])
df = df.reset_index(drop=True)
d = Counter(df['TRADE_ENTRY'])

# df = df.sort_values(by=["Symbol", "Date"])
df = df.reset_index(drop=True)

stock_symbols = list(set(df['Symbol']))
stock_symbols = sorted(stock_symbols)

empty_col = ['NA'] * df.shape[0]
print('sorted')

# -------------------------------------------------------------

df.insert(18, "TRADE_RESULT", empty_col, True)
df.insert(19, "PERCENT_CHANGE", empty_col, True)

i = 0
for x in df['Symbol']:
    if df['TRADE_ENTRY'][i] == "YES":

        for j in range(25):

            if (df['Close'][i] - df['Low'][i + j + 1]) >= 0.25 * df['ATR'][i]:
                df.at[i, 'TRADE_RESULT'] = 'LOSS'
                df.at[i, 'PERCENT_CHANGE'] = (0.25 * df['ATR'][i] /
                                              df['Close'][i]) * 100
                break

            if (df['High'][i + j + 1]) - df['Close'][i] >= 0.5 * df['ATR'][i]:
                df.at[i, 'TRADE_RESULT'] = 'WIN'
                df.at[i, 'PERCENT_CHANGE'] = (0.5 * df['ATR'][i] /
                                              df['Close'][i]) * 100
                break
            if (j == 24):
                df.at[i, 'TRADE_RESULT'] = 'TIE'
                df.at[i, 'PERCENT_CHANGE'] = (
                    (df['Close'][i + j + 1] - df['Close'][i]) /
                    df['Close'][i]) * 100
                break

        print(i)
    i = i + 1

# ------------------------------------------------------

print(df)
print('exporting')
df = df[df['TRADE_ENTRY'] == 'YES']
df.to_csv('sample_only_results_trades_simulation_complete.csv', index=False)
print('done')