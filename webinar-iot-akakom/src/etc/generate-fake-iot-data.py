from datetime import datetime, timedelta
import numpy as np
import pandas as pd

print("1")

#create the data frame and the initial timestamp
iotdf = pd.DataFrame(columns = ['timestamp', 'event', 'simid'])
iotdf.at[0, 'timestamp'] = datetime.now()


print("2")
#create sequential timestamps with random lags

#option 1: set limit by number of rows
number_of_rows  =  90000
n = 0

print("22")
while iotdf.shape[0] < number_of_rows:
    x = n
    n = n + 1
    iotdf.at[n, 'timestamp'] = iotdf.at[ x,'timestamp'] + timedelta(seconds=np.random.randint(10,60,1)[0].item())

print("3")
#option 2: set limit by number of hours
number_of_hours  =  48
n = 0
while (iotdf.iloc[-1, 0] - iotdf.iloc[0, 0]).days * 24 < number_of_hours:
    x = n
    n = n + 1
    iotdf.at[n, 'timestamp'] = iotdf.at[ x,'timestamp'] + timedelta(seconds=np.random.randint(10,60,1)[0].item())

print("4")
#option 3: set limit by the custom date
final_date = '2022-09-16 17:35:32.908580'
date_time_obj = datetime.strptime(final_date, '%Y-%m-%d %H:%M:%S.%f')
n = 0
while iotdf.iloc[-1, 0] < date_time_obj:
    x = n
    n = n + 1
    iotdf.at[n, 'timestamp'] = iotdf.at[ x,'timestamp'] + timedelta(seconds=np.random.randint(10,60,1)[0].item())

print("5")
# create the random numbers column 
iotdf['randNumCol'] = np.random.randint(1, iotdf.shape[0], iotdf.shape[0])

print("6")
#allocate data usage events randomly
def random_event(x):
    if (x >= 1) & (x < 60000):
        result = 'data'
    else:
        result =  'alert'
    return result
iotdf['event'] = iotdf['randNumCol'].apply(random_event)

print("7")
#allocate device / SIM IDs randomly (based on the number of rows limit = 90,000)
def random_simid(x):
    if (x >= 1) & (x < 25000):
        result = '0001'
    elif (x >= 25000) & (x < 50000):
        result =  '0002'
    elif (x >= 50000) & (x < 75000):
        result = '0003'
    else:
        result = '0004'
    return result
iotdf['simid'] = iotdf['randNumCol'].apply(random_simid)

print("8")
#allocate semi-random PDP context events
n = iotdf.shape[0]
for i in range(0,iotdf.shape[0]):
    if iotdf.at[i, 'event'] == 'data':
        n = n + 1
        iotdf.at[n, 'event'] = 'Create PDP context'
        iotdf.at[n, 'timestamp'] = iotdf.at[i, 'timestamp'] - timedelta(seconds = 1)
        iotdf.at[n, 'simid'] = iotdf.at[i, 'simid']
        n = n + 1
        iotdf.at[n, 'event'] = 'Delete PDP context'
        iotdf.at[n, 'timestamp'] = iotdf.at[i, 'timestamp'] + timedelta(seconds = 1)
        iotdf.at[n, 'simid'] = iotdf.at[i, 'simid']

print("9")
#final prettifying
iotdf = iotdf.sort_values(by='timestamp')
iotdf = iotdf.drop(columns = ['randNumCol'])
iotdf.head(n = 10)

iotdf.to_csv()

for row in iotdf.itertuples():
  print(row)
