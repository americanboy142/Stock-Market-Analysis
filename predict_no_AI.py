import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


data = pd.read_csv('csv_files/AAPL.csv')

week_Price = np.array(data['Weekly_Price'])

Plus_Min = np.zeros(len(week_Price))

predict = np.zeros(len(week_Price))

for i in range(len(week_Price)-1,-1,-1):
    if week_Price[i] < week_Price[i-1]:
        Plus_Min[i] = 1
    else:
        Plus_Min[i] = 0 

# goal is to return percentage change up or down where 0 is down and 1 is up

def calculate_EMA_difference(short, long):
    dif = long - short

    trend = np.diff(dif) / dif[:-1]
    trend = np.insert(trend, 0, 0)

    return np.round(trend,4)


trend = calculate_EMA_difference(np.array(data['EMA_Short']),np.array(data['EMA_Long']))
data['Trend_EMA'] = trend

for i in range(len(trend)-1,-1,-1):
    if trend[i] < trend[i-1]:
        predict[i] = Plus_Min[i-1]
    else:
        if Plus_Min[i-1] == 0:
            predict[i] = 1 
        else:
            predict[i] = 0

count = 0

for i,el in enumerate(predict):
    if el == Plus_Min[i]:
        count +=1

print("percent correct =", count/len(trend))


def calculate_RSI_trend(rsi):

    trend = np.diff(rsi) / rsi[:-1]
    
    return np.round(trend,4)



rsi = data['RSI']

trend = calculate_RSI_trend(rsi)

data['RSI_Trend'] = trend


print("predict:",predict)

""" plt.plot(x, trend)
plt.yscale("log")
plt.show()
plt.plot(x, week_Price)
plt.show() """