import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt

def calculate_EMA_difference(short, long):
    """Calculates the difference between EMA short and long
    returns a vector of the differences
    """
    dif = long - short

    trend = np.diff(dif) / dif[:-1]
    trend = np.insert(trend, 0, 0)

    return np.round(trend,4)

def calculate_RSI_trend(rsi):
    """Calculates trend of the rsi
    MACD
    returns a vector of trends
    """
    trend = np.diff(rsi) / rsi[:-1]
    #trend = np.insert(trend, 0, 0)
    return np.round(trend,4)

def calculate_Puls_min(week_Price):
    """returns a vector of weather the current weeks price is above or below the previous"""
    Plus_Min = np.zeros(len(week_Price))
    
    for i in range(len(week_Price)-1,-1,-1):
        if week_Price[i] < week_Price[i-1]:
            Plus_Min[i] = 1
        else:
            Plus_Min[i] = 0 
    
    return Plus_Min


def predict(data,Plus_Min):
    """takes a data frame of data, returns accuracy,prediction of price increase or decrease given a ticker"""

    predict = np.zeros(len(data['Weekly_Price']))


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

    rsi = data['RSI']

    trend = calculate_RSI_trend(rsi)

    data['RSI_Trend'] = trend
    
    return count/len(trend),predict
