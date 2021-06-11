import pandas as pd
import time
import datetime
import glob
import os
import statistics

# change path and import data
# resort data to make sure it uses stock symbol as primary sort
# then uses chronogical order as secondary sort
path = 'C:/Users/Tahsin/Desktop/EY Analysis/indicators'
os.chdir(path)
df = pd.read_csv('sample_combined_15_min_files.csv')
print('imported')
df['Date'] = pd.to_datetime(df.Date, format='%d-%b-%Y %H:%M')
df = df.sort_values(by=["Symbol", "Date"])
print('sorting done')
df = df.reset_index(drop=True)

stock_symbols = list(set(df['Symbol']))
stock_symbols = sorted(stock_symbols)

# -----------------------------------------------------------------
#create SSL columns
print('part 1/6')

empty_col = ['NA'] * df.shape[0]
df.insert(8, "SMA_HIGH", empty_col, True)
df.insert(9, "SMA_LOW", empty_col, True)
df.insert(10, "SSL_COLOUR", empty_col, True)
df.insert(11, "SSL_SWITCH", empty_col, True)

df['SMA_HIGH'] = df.High.rolling(window=20, min_periods=0).mean()
df['SMA_LOW'] = df.Low.rolling(window=20, min_periods=0).mean()

df.loc[df.Close >= df.SMA_HIGH, "SSL_COLOUR"] = "GREEN"
df.loc[df.Close <= df.SMA_LOW, "SSL_COLOUR"] = "RED"

shift_col = df['SSL_COLOUR'].shift(periods=1)
df.insert(12, "shift_col", shift_col, True)

for x in range(500):
    df.loc[(df.Close > df.SMA_LOW) & (df.Close < df.SMA_HIGH),
           "SSL_COLOUR"] = df.shift_col
    df['shift_col'] = df['SSL_COLOUR'].shift(periods=1)
    print(x)

df.loc[df.SSL_COLOUR == df.shift_col, "SSL_SWITCH"] = "NO"
df.loc[df.SSL_COLOUR != df.shift_col, "SSL_SWITCH"] = "YES"

del df['shift_col']

# -----------------------------------------------------------------
#create ATR values (NOTE: later need to delete first 390 rows from every ticker)
print('part 2/6')

df.insert(12, "ATR", empty_col, True)

curr_close_1 = df['Close'].shift(periods=1)
prev_close_1 = df['Close'].shift(periods=27)
curr_close_2 = df['Close'].shift(periods=27)
prev_close_2 = df['Close'].shift(periods=53)
curr_close_3 = df['Close'].shift(periods=53)
prev_close_3 = df['Close'].shift(periods=79)
curr_close_4 = df['Close'].shift(periods=79)
prev_close_4 = df['Close'].shift(periods=105)
curr_close_5 = df['Close'].shift(periods=105)
prev_close_5 = df['Close'].shift(periods=131)
curr_close_6 = df['Close'].shift(periods=131)
prev_close_6 = df['Close'].shift(periods=157)
curr_close_7 = df['Close'].shift(periods=157)
prev_close_7 = df['Close'].shift(periods=183)
curr_close_8 = df['Close'].shift(periods=183)
prev_close_8 = df['Close'].shift(periods=209)
curr_close_9 = df['Close'].shift(periods=209)
prev_close_9 = df['Close'].shift(periods=235)
curr_close_10 = df['Close'].shift(periods=235)
prev_close_10 = df['Close'].shift(periods=261)
curr_close_11 = df['Close'].shift(periods=261)
prev_close_11 = df['Close'].shift(periods=287)
curr_close_12 = df['Close'].shift(periods=287)
prev_close_12 = df['Close'].shift(periods=313)
curr_close_13 = df['Close'].shift(periods=313)
prev_close_13 = df['Close'].shift(periods=339)
curr_close_14 = df['Close'].shift(periods=339)
prev_close_14 = df['Close'].shift(periods=365)

df.insert(13, "curr_close_1", curr_close_1, True)
df.insert(14, "prev_close_1", prev_close_1, True)
df.insert(15, "curr_close_2", curr_close_2, True)
df.insert(16, "prev_close_2", prev_close_2, True)
df.insert(17, "curr_close_3", curr_close_3, True)
df.insert(18, "prev_close_3", prev_close_3, True)
df.insert(19, "curr_close_4", curr_close_4, True)
df.insert(20, "prev_close_4", prev_close_4, True)
df.insert(21, "curr_close_5", curr_close_5, True)
df.insert(22, "prev_close_5", prev_close_5, True)
df.insert(23, "curr_close_6", curr_close_6, True)
df.insert(24, "prev_close_6", prev_close_6, True)
df.insert(25, "curr_close_7", curr_close_7, True)
df.insert(26, "prev_close_7", prev_close_7, True)
df.insert(27, "curr_close_8", curr_close_8, True)
df.insert(28, "prev_close_8", prev_close_8, True)
df.insert(29, "curr_close_9", curr_close_9, True)
df.insert(30, "prev_close_9", prev_close_9, True)
df.insert(31, "curr_close_10", curr_close_10, True)
df.insert(32, "prev_close_10", prev_close_10, True)
df.insert(33, "curr_close_11", curr_close_11, True)
df.insert(34, "prev_close_11", prev_close_11, True)
df.insert(35, "curr_close_12", curr_close_12, True)
df.insert(36, "prev_close_12", prev_close_12, True)
df.insert(37, "curr_close_13", curr_close_13, True)
df.insert(38, "prev_close_13", prev_close_13, True)
df.insert(39, "curr_close_14", curr_close_14, True)
df.insert(40, "prev_close_14", prev_close_14, True)

df['ATR'] = (abs(df.curr_close_1 - df.prev_close_1) +
             abs(df.curr_close_2 - df.prev_close_2) +
             abs(df.curr_close_3 - df.prev_close_3) +
             abs(df.curr_close_4 - df.prev_close_4) +
             abs(df.curr_close_5 - df.prev_close_5) +
             abs(df.curr_close_6 - df.prev_close_6) +
             abs(df.curr_close_7 - df.prev_close_7) +
             abs(df.curr_close_8 - df.prev_close_8) +
             abs(df.curr_close_9 - df.prev_close_9) +
             abs(df.curr_close_10 - df.prev_close_10) +
             abs(df.curr_close_11 - df.prev_close_11) +
             abs(df.curr_close_12 - df.prev_close_12) +
             abs(df.curr_close_13 - df.prev_close_13) +
             abs(df.curr_close_14 - df.prev_close_14)) / 14

del df['curr_close_1']
del df['prev_close_1']
del df['curr_close_2']
del df['prev_close_2']
del df['curr_close_3']
del df['prev_close_3']
del df['curr_close_4']
del df['prev_close_4']
del df['curr_close_5']
del df['prev_close_5']
del df['curr_close_6']
del df['prev_close_6']
del df['curr_close_7']
del df['prev_close_7']
del df['curr_close_8']
del df['prev_close_8']
del df['curr_close_9']
del df['prev_close_9']
del df['curr_close_10']
del df['prev_close_10']
del df['curr_close_11']
del df['prev_close_11']
del df['curr_close_12']
del df['prev_close_12']
del df['curr_close_13']
del df['prev_close_13']
del df['curr_close_14']
del df['prev_close_14']

# ------------------------------------------------
#RED CANDLE, VOLUME REQ AND PRICE REQ
print('part 3/6')

df.insert(13, "RED_CANDLE", empty_col, True)
df.insert(14, "VOLUME_REQ", empty_col, True)
df.insert(15, "PRICE_REQ", empty_col, True)

prev_volume = df['Volume'].shift(periods=1)
df.insert(16, "prev_volume", prev_volume, True)

prev_close = df['Close'].shift(periods=1)
df.insert(17, "prev_close", prev_close, True)

df.loc[df.Volume >= df.prev_volume, "VOLUME_REQ"] = "YES"
df.loc[df.Volume < df.prev_volume, "VOLUME_REQ"] = "NO"

df.loc[df.Close >= df.Open, "RED_CANDLE"] = "NO"
df.loc[df.Close < df.Open, "RED_CANDLE"] = "YES"

df.loc[df.Open >= df.prev_close, "PRICE_REQ"] = "YES"
df.loc[df.Open < df.prev_close, "PRICE_REQ"] = "NO"

del df['prev_volume']
del df['prev_close']

# ------------------------------------------------
# BASELINE REQUIREMENT
print('part 4/6')

df.insert(16, "BASELINE_REQ", empty_col, True)

prev_close = df['Close'].shift(periods=1)
df.insert(17, "prev_close", prev_close, True)

df.loc[((df.Open - df.prev_close) < 0.5 * df.ATR) &
       ((df.Close - df.prev_close) < df.ATR), "BASELINE_REQ"] = "YES"

del df['prev_close']

# ------------------------------------------------
# TRADE ENTRY
print('part 5/6')

df.insert(17, "TRADE_ENTRY", empty_col, True)
df.loc[(df.time == df['time'][0]) & (df.SSL_COLOUR == 'GREEN') &
       (df.SSL_SWITCH == 'NO') & (df.RED_CANDLE == 'NO') &
       (df.VOLUME_REQ == 'YES') & (df.PRICE_REQ == 'YES') &
       (df.BASELINE_REQ == 'YES'), "TRADE_ENTRY"] = "YES"

# ------------------------------------------------
print(df)
print('part 6/6')

df.to_csv('technical_analysis_full_list_v2.csv', index=False)
# df.to_csv('troubleshooting.csv', index = False)