from time import sleep
import requests
import pandas as pd
from admin_func import GET_SYMBOLS
import key
import numpy as np

# move to calulations want to only call daily price

#EMA = 2/(timeperiods+1)(current_price - prev_ema) + prev_ema
# timeperiods would be number of days between calculation
# so long might be 50days and short could be 15 days


# RSI = 100 – 100 / ( 1 + RS)
# RS = avgU / avgD
# avgU = SUM of all gains over the time period / timeperiod === 0 if no gain
# avgD = SUM of all losses over the time period / timeperiod ==== 100 if no loss




#nasdq_symbol = GET_SYMBOLS

def numeric_build(symbol:str):
    # call for short moving average
    r = requests.get(f'https://www.alphavantage.co/query?function=EMA&symbol={symbol}&interval=weekly&time_period=15&series_type=open&apikey={key.API_KEY}')
    data_EMA_Short = r.json()
    EMA_Short = np.array([vals["EMA"] for vals in data_EMA_Short["Technical Analysis: EMA"].values()])

    # call for long moving average
    r = requests.get(f'https://www.alphavantage.co/query?function=EMA&symbol={symbol}&interval=weekly&time_period=50&series_type=open&apikey={key.API_KEY}')
    data_EMA_Long = r.json()
    EMA_long = np.array([vals["EMA"] for vals in data_EMA_Long["Technical Analysis: EMA"].values()])

    #call for RSI
    r = requests.get(f'https://www.alphavantage.co/query?function=RSI&symbol={symbol}&interval=weekly&time_period=10&series_type=open&apikey={key.API_KEY}')
    data_RSI = r.json()
    RSI = np.array([vals["RSI"] for vals in data_RSI["Technical Analysis: RSI"].values()])

    #call for OBV
    r = requests.get(f'https://www.alphavantage.co/query?function=OBV&symbol={symbol}&interval=weekly&apikey={key.API_KEY}')
    data_OBV = r.json()
    OBV = np.array([vals["OBV"] for vals in data_OBV["Technical Analysis: OBV"].values()])

    #call for Weekly adjusted
    r = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol={symbol}&apikey={key.API_KEY}')
    data_Week = r.json()
    Weekly_price = np.array([vals["5. adjusted close"] for vals in data_Week["Weekly Adjusted Time Series"].values()])

    if not Weekly_price:
        raise Exception('Call Failed')
 
    shortest_data = min(len(EMA_Short),
                        len(EMA_long),
                        len(RSI),
                        len(OBV),
                        len(Weekly_price))

    Main_Array = np.array([EMA_Short],
                        [EMA_long],
                        [RSI],
                        [OBV],
                        [Weekly_price])
    
    for i in Main_Array:
        i = i[:shortest_data]

    # fill the matrix with values
    #{
    # (0) EMA Short
    # (1) EMA Long
    # (2) RSI
    # (3) OBV
    # (4) Adjusted Close
    #}

    # creats a dictionary for the current symbols data
    # will be changed every itereation
    Historical_Current_dct = {"EMA Short" : EMA_Short,
                              "EMA Long": EMA_long, 
                              "RSI": RSI,
                              "OBV": OBV,
                              "Weekly Price": Weekly_price}

    Historica_current_df = pd.DataFrame(Historical_Current_dct)

    # df was 1 row with crazy columns
    Historica_current_df.to_csv(f'csv_files/{symbol}.csv',index=False)
    print(f"{symbol} has been filled")
    print("===========================================")

numeric_build('AAPL')

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
