from collections import Counter
import pandas as pd
import time
import datetime
import glob
import os

#change directory and read csv file
path = 'C:/Users/Tahsin/Desktop/EY Analysis/cleanup/*.csv'

#create empty list for times
combined_data_list = []
i = 1

# Define timestamps to filter out
time1 = datetime.datetime.strptime('09:00:00', '%H:%M:%S').time()
time2 = datetime.datetime.strptime('09:15:00', '%H:%M:%S').time()
time3 = datetime.datetime.strptime('16:00:00', '%H:%M:%S').time()
time4 = datetime.datetime.strptime('16:15:00', '%H:%M:%S').time()
time5 = datetime.datetime.strptime('16:30:00', '%H:%M:%S').time()
time6 = datetime.datetime.strptime('16:45:00', '%H:%M:%S').time()

# loop to iterate through each csv file and:
# - filter dates
# - Remove 'days' with missing timestamps
for fname in glob.glob(path):
    df = pd.read_csv(fname)
    # create column for time only (dataset only comes with datetime)
    just_times = [
        datetime.datetime.strptime(x, '%d-%b-%Y %H:%M').time()
        for x in df["Date"]
    ]
    df.insert(1, "time", just_times, True)
    #filter out times
    df = df[(df["time"] != time1)]
    df = df[(df["time"] != time2)]
    df = df[(df["time"] != time3)]
    df = df[(df["time"] != time4)]
    df = df[(df["time"] != time5)]
    df = df[(df["time"] != time6)]
    # group data by stock ticker and remove all groups which have incomplete data
    df = df.sort_values(by=["Symbol"])
    grouped = df.groupby('Symbol')
    df = (grouped.filter(lambda x: len(x) > 25))
    combined_data_list.append(df)
    print(i)
    i = i + 1

combined_data_list = pd.concat(combined_data_list)
path = 'C:/Users/Tahsin/Desktop/EY Analysis/cleanup'
os.chdir(path)

# Print out a list of stocks and how many data points they have
d = Counter(combined_data_list['Symbol'])
stock_counts = pd.DataFrame.from_dict(d, orient='index').reset_index()
print(stock_counts)
stock_counts.to_csv('stock_counts.csv')

# Filter out stocks which have less than 85% of maximum data
combined_data_list = combined_data_list.sort_values(by=["Symbol"])
grouped = combined_data_list.groupby('Symbol')
combined_data_list = (grouped.filter(lambda x: len(x) > 110))
print(combined_data_list)

combined_data_list.to_csv('sample_combined_15_min_files.csv', index=False)
