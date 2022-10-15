from operator import index
from time import sleep
from typing import DefaultDict
import requests
import numpy as np
import pandas as pd
from admin_func import GET_SYMBOLS
import key
import csv
import time

nasdq_symbol = GET_SYMBOLS

print("Main Loop Started")

count = 0
for i,symbol in enumerate(nasdq_symbol):
    # call for short moving average
    url_EMA_Short = f'https://www.alphavantage.co/query?function=EMA&symbol={symbol}&interval=daily&time_period=15&series_type=open&apikey={key.API_KEY}'
    r = requests.get(url_EMA_Short)
    data_EMA_Short = r.json()

    # call for long moving average
    url_EMA_Long = f'https://www.alphavantage.co/query?function=EMA&symbol={symbol}&interval=daily&time_period=50&series_type=open&apikey={key.API_KEY}'
    r = requests.get(url_EMA_Long)
    data_EMA_Long = r.json()

    #call for RSI
    url_RSI = f'https://www.alphavantage.co/query?function=RSI&symbol={symbol}&interval=daily&time_period=10&series_type=open&apikey={key.API_KEY}'
    r = requests.get(url_RSI)
    data_RSI = r.json()

    #call for OBV
    url_OBV = f'https://www.alphavantage.co/query?function=OBV&symbol={symbol}&interval=daily&apikey={key.API_KEY}'
    r = requests.get(url_OBV)
    data_OBV = r.json()

    #call for Weekly adjusted
    url_Week = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol={symbol}&apikey={key.API_KEY}'
    r = requests.get(url_Week)
    data_Week = r.json()

    # Will stop loop if api call fails
    try:
        unsorted_data = [data_EMA_Short["Technical Analysis: EMA"], 
                     data_EMA_Long["Technical Analysis: EMA"], 
                     data_RSI["Technical Analysis: RSI"],
                     data_OBV["Technical Analysis: OBV"], 
                     data_Week["Weekly Adjusted Time Series"]
                     ]
    except :
        break
    
    Data_sub = [ "EMA", "EMA",
                 "RSI", "OBV",
                 "5. adjusted close"
                 ]
    shortest_data = min(len(data_EMA_Short["Technical Analysis: EMA"]),
                        len(data_EMA_Long["Technical Analysis: EMA"]),
                        len(data_RSI["Technical Analysis: RSI"]),
                        len(data_OBV["Technical Analysis: OBV"]),
                        len(data_Week["Weekly Adjusted Time Series"])
                            )
    Longest_data = max(len(data_EMA_Short["Technical Analysis: EMA"]),
                        len(data_EMA_Long["Technical Analysis: EMA"]),
                        len(data_RSI["Technical Analysis: RSI"]),
                        len(data_OBV["Technical Analysis: OBV"]),
                        len(data_Week["Weekly Adjusted Time Series"])
                            )


    # fill the matrix with values
    #{
    # (0) EMA Short
    # (1) EMA Long
    # (2) RSI
    # (3) OBV
    # (4) Adjusted Close
    #}

    EMA_short_sorted = []
    EMA_long_sorted = []
    RSI_sorted = []
    OBV_sorted =[]
    MACD_sorted =[]
    Weekly_sorted =[] 
    
    sorted_data = [EMA_short_sorted, EMA_long_sorted, RSI_sorted, OBV_sorted, Weekly_sorted, MACD_sorted] # list of list of values


    # this loop fills all the sorted lists with api values for each of the sybols
    for i in range(5): # loops length of list of unsored data, IE for i in 5
        for points in unsorted_data[i]: # loops though each point in unsorted data
            sorted_data[i].append(unsorted_data[i][points][Data_sub[i]]) # values are put into each of the sorted lists
    
    # trouble shoots incase a api list is shorter then another   
    # makes all lists equal size by removing values from lists that are longer then the shortest one                   
    for datas in sorted_data:
        for i in range(len(datas)-shortest_data):
            datas.pop()

    for i in range(len(sorted_data[0])):
        #short-long
        #short = EMA_short_sorted
        #long = EMA_long_sorted
        MACD_sorted.append(float(EMA_short_sorted[i]) - float(EMA_long_sorted[i]))
    
    # creats a dictionary for the current symbols data
    # will be changed every itereation
    Historical_Current_dct = {"EMA Short" : EMA_short_sorted,
                              "EMA Long": EMA_long_sorted, 
                              "RSI": RSI_sorted,
                              "OBV": OBV_sorted,
                              "MACD": MACD_sorted,
                              "Weekly Price": Weekly_sorted}

    Historica_current_df = pd.DataFrame(Historical_Current_dct)

    # df was 1 row with crazy columns
    Historica_current_df.to_csv(f'csv_files/{symbol}.csv',index=False)
    print(f"{symbol} has been filled")
    count+=1
    print(f"{50-count} remaining")
    print("===========================================")
    print("===========================================")
    break
    sleep(61)

# all historical csvs created and filled 

# now needs to be read back for training and eval will do in tensorFinance.py file so no more api calls need to happen, 
# needs to be ran once a week to keep with new data values



#technical = data_ma['Technical Analysis: SMA']
#minData = data['Time Series (5min)']



#{
#   1)  try converting historical data to saveable csv file
#       a) using only 5 calls per min I.E. one complete table per minute,per company
#       b) using 2/3 as training and 1/3 as practice eval
#
#   2)  from csv build up ai predictive functions for each company
#       a) either reset, or different variables for each
#
#   3)  test function on the later historical data
#       a) function will predict next weeks closing price
#
#   4)  for new data can only do one company per minute
#       a) we will only need to call once a day or every other day
#
#   5)  test out on fake trading website for a month
#
#
#}
