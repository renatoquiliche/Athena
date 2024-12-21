
# %%
import numpy as np
import pandas as pd
import math
import operator
import heapq
import statistics

df_close = pd.read_csv('./ASSETS/GOLD/1 HOUR/GOLD(60min).csv', usecols=[5], header= None)
df_date = pd.read_csv('./ASSETS/GOLD/1 HOUR/GOLD(60min).csv', usecols=[0], header= None).values
df_time = pd.read_csv('./ASSETS/GOLD/1 HOUR/GOLD(60min).csv', usecols=[1], header= None).values
Data_close = df_close.values
Rate1_step = int(len(df_close)/4)
Rate1_arr = []
for i in range(Rate1_step):
    Rate1 = Data_close[i*4+3][0]*100/Data_close[i*4][0]-100
    #Rate1 = math.floor(Rate1*1000)/1000
    Rate1_arr.append(Rate1)
#print(Rate1_arr)
Rate2_arr = []

for j in range(len(Rate1_arr)-1):
    Rate2 = Rate1_arr[j+1]*100/Rate1_arr[j]-100
    #if Rate2 >=120:
        #var_arr = [Data_close[j*4][0], Data_close[j*4+1][0], Data_close[j*4+2][0], Data_close[j*4+3][0]]
        #ex = [1,2,3,4]
        #max_point = max(var_arr)
    #else:
        #max_point = 0
    #Rate2 = math.floor(Rate2*1000)/1000
    Rate2_arr.append(Rate2)
    #max_arr.append(max_point)
#print(Rate2_arr)
No_arr = []
index_arr = []
for k in range(len(Rate2_arr)):
    if Rate2_arr[k] >= 120:
        var_max_arr = [Data_close[(k+1)*4][0], Data_close[(k+1)*4+1][0], Data_close[(k+1)*4+2][0], Data_close[(k+1)*4+3][0]]
        max_index, max_value = max(enumerate(var_max_arr), key=operator.itemgetter(1))        
        #max_point = 0
        #for m in range(0, 4):
            #if Data_close[(k+1)*4+m][0] > max_point:
                #max_point = Data_close[(k+1)*4+m][0]
        No_arr.append(max_value)
        index_arr.append((k+1)*4 + max_index)
    elif Rate2_arr[k] <= 56:
        var_min_arr = [Data_close[(k+1)*4][0], Data_close[(k+1)*4+1][0], Data_close[(k+1)*4+2][0], Data_close[(k+1)*4+3][0]]
        min_index, min_value = min(enumerate(var_min_arr), key=operator.itemgetter(1))
        No_arr.append(min_value)
        index_arr.append((k+1)*4 + min_index)
        
#print(index_arr)
#print(No_arr)
Axis_X_arr = []
Axis_Y_arr = []

for m in range(len(index_arr)-1):
    Axis_X = index_arr[m+1]-index_arr[m]
    Axis_Y = abs(No_arr[m+1]-No_arr[m])
    Axis_X_arr.append(Axis_X)
    Axis_Y_arr.append(math.floor(Axis_Y*100)/100)
#print(Axis_X_arr)
#print(Axis_Y_arr)


Baseline_AX_arr = [Axis_X_arr[len(Axis_X_arr)-4], Axis_X_arr[len(Axis_X_arr)-3], Axis_X_arr[len(Axis_X_arr)-2], Axis_X_arr[len(Axis_X_arr)-1]]
#print(Baseline_AX_arr)

correlation_number_X_arr=[]
for n in range(len(Axis_X_arr)-3):
    Gen_AX_arr= [Axis_X_arr[n], Axis_X_arr[n+1], Axis_X_arr[n+2], Axis_X_arr[n+3]]
    correlation_number = np.corrcoef(Baseline_AX_arr, Gen_AX_arr)[0][1]*100
    correlation_number_X_arr.append(correlation_number)
#print(correlation_number_X_arr)

X = heapq.nlargest(5, correlation_number_X_arr)
X_indexes = heapq.nlargest(5, range(len(correlation_number_X_arr)), key=correlation_number_X_arr.__getitem__)
#print(X)
#print(X_indexes)

Baseline_AY_arr = [Axis_Y_arr[len(Axis_Y_arr)-4], Axis_Y_arr[len(Axis_Y_arr)-3], Axis_Y_arr[len(Axis_Y_arr)-2], Axis_Y_arr[len(Axis_Y_arr)-1]]
#print(Baseline_AY_arr)

correlation_number_Y_arr=[]
for n in range(len(Axis_Y_arr)-3):
    Gen_AY_arr= [Axis_Y_arr[n], Axis_Y_arr[n+1], Axis_Y_arr[n+2], Axis_Y_arr[n+3]]
    correlation_number = np.corrcoef(Baseline_AY_arr, Gen_AY_arr)[0][1]*100
    correlation_number_Y_arr.append(correlation_number)
#print(correlation_number_Y_arr)

Y = heapq.nlargest(5, correlation_number_Y_arr)
Y_indexes = heapq.nlargest(5, range(len(correlation_number_Y_arr)), key=correlation_number_Y_arr.__getitem__)
#print(Y)
#print(Y_indexes)

correlation_XY_arr = []
for l in range(len(correlation_number_Y_arr)):
    XY_val = statistics.mean([correlation_number_Y_arr[l], correlation_number_X_arr[l]])
    correlation_XY_arr.append(XY_val)

XY = heapq.nlargest(5, correlation_XY_arr)
XY_indexes = heapq.nlargest(5, range(len(correlation_XY_arr)), key=correlation_XY_arr.__getitem__)
#print(XY)
#print(XY_indexes)

X_corresponding_date_times = []

for h in range(0, 4):
    X_corresponding_date = df_date[index_arr[X_indexes[h] + 2]:index_arr[X_indexes[h] + 3]]
    X_corresponding_time = df_time[index_arr[X_indexes[h] + 2]:index_arr[X_indexes[h] + 3]]
    X_corresponding_date_time_arr = []
    for p in range(len(X_corresponding_date)):
        X_corresponding_date_time = X_corresponding_date[p] + '-' + X_corresponding_time[p]
        X_corresponding_date_time_arr.append(X_corresponding_date_time)
    X_corresponding_date_times.append([X[h], X_corresponding_date_time_arr])
print('-----------X values and Times --------------')

print(X_corresponding_date_times)

Y_corresponding_date_times = []

for h in range(0, 4):
    Y_corresponding_date = df_date[index_arr[Y_indexes[h] + 2]:index_arr[Y_indexes[h] + 3]]
    Y_corresponding_time = df_time[index_arr[Y_indexes[h] + 2]:index_arr[Y_indexes[h] + 3]]
    Y_corresponding_date_time_arr = []
    for p in range(len(Y_corresponding_date)):
        Y_corresponding_date_time = Y_corresponding_date[p] + '-' + Y_corresponding_time[p]
        Y_corresponding_date_time_arr.append(Y_corresponding_date_time)
    Y_corresponding_date_times.append([Y[h], Y_corresponding_date_time_arr])
    
print('-----------Y values and Times --------------')
print(Y_corresponding_date_times)

XY_corresponding_date_times = []

for h in range(0, 4):
    XY_corresponding_date = df_date[index_arr[XY_indexes[h] + 2]:index_arr[XY_indexes[h] + 3]]
    XY_corresponding_time = df_time[index_arr[XY_indexes[h] + 2]:index_arr[XY_indexes[h] + 3]]
    XY_corresponding_date_time_arr = []
    for p in range(len(XY_corresponding_date)):
        XY_corresponding_date_time = XY_corresponding_date[p] + '-' + XY_corresponding_time[p]
        XY_corresponding_date_time_arr.append(XY_corresponding_date_time)
    XY_corresponding_date_times.append([XY[h], XY_corresponding_date_time_arr])
    
print('-----------XY values and Times --------------')
print(XY_corresponding_date_times)

"""
Graphic interface
"""    
    
# %%
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import date2num

asset_graph = pd.read_csv('./ASSETS/GOLD/1 HOUR/GOLD(60min).csv'
                          , header=None
                          , names=['date', 'time', 'a1', 'a2', 'a3', 'a4', 'vol'])

format = '%Y-%m-%d %H:%M:%S'
asset_graph['Datetime'] = pd.to_datetime(asset_graph['date'] + ' ' + asset_graph['time'], format=format)
asset_graph = asset_graph.set_index(pd.DatetimeIndex(asset_graph['Datetime']))
asset_graph = asset_graph.drop(['date', 'time', 'Datetime'], axis=1)

# %%
plt.style.use('ggplot')
plt.figure(figsize=(15,7))



#Indexes the second best
second_best = 1
#Indexes the time stamp
time_stamp = 1
#Indexes the first date
first_date = 0

timestamp1 = XY_corresponding_date_times[second_best][time_stamp][first_date][0]
timestamp2 = XY_corresponding_date_times[second_best][time_stamp][-1][0]

#markers_on = [timestamp1, timestamp2]

month = timestamp1[0:10]

# Hace un zoom en el mes en que se hallo la correlacion
plt.plot(asset_graph["a1"].loc[month], label='Value')
#plt.plot(asset_graph["a1"].loc[month], '-rD', markevery=markers_on)

plt.axvspan(date2num(datetime.strptime(timestamp1, '%Y.%m.%d-%H:%M')),
            date2num(datetime.strptime(timestamp2, '%Y.%m.%d-%H:%M')),
            facecolor='b', alpha=0.5, label="Optimal")
plt.legend()

print("Periodos temporales incluidos en la solución :",
      pd.DataFrame(XY_corresponding_date_times[second_best][time_stamp]))

print("\U0001F618")

plt.show()
