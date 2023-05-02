import key
import json
import requests
import numpy as np
# json=2.0.9

symbol = 'AAPL'


def daily_call(symbol):
    
    r = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&outputsize=full&apikey={key.API_KEY}')
    return r.json()


'''with open('json_files/test_call.json', 'w') as f:
    json.dump(data, f)
'''
with open('json_files/test_call.json', 'r') as f:
    data = json.load(f)

def calc_daly_gain_loss(data:dict):
    '''
        takes in full call returns numpy array of daily gain/loss
        daily gain would return > 0
    '''
    open = np.array([float(val["1. open"]) for val in data["Time Series (Daily)"].values()])
    close = np.array([float(val["4. close"]) for val in data["Time Series (Daily)"].values()])

    return close - open

#dif = calc_daly_gain_loss(data)

#print(dif[4:10])
# RSI = 100 – 100 / ( 1 + RS)
# RS = avgU / avgD
# avgU = SUM of all gains over the time period / timeperiod === 0 if no gain
# avgD = SUM of all losses over the time period / timeperiod ==== 100 if no loss
def RSI_calc(daily_gain_loss):
    '''
        using 14 days as time period
    '''
    interval = 14
    def RS(sub_array) -> float:
        avgU = np.mean(np.where(sub_array >= 0,sub_array,0))
        avgD = np.mean(np.where(sub_array < 0,-sub_array, 0))

        if avgD == 0:
            return 1000000000000

        return avgU/avgD
    
    RS_arr = np.zeros(len(daily_gain_loss))

    for i in range(len(daily_gain_loss)):
        RS_arr[i] = RS(daily_gain_loss[i:i+interval])

    return  100 - 100 / ( 1 + RS_arr) 

'''
    NEEDS TO BE REVERED
'''

#RSI = RSI_calc(dif)

#print(RSI[-3:])


#EMA = 2/(timeperiods+1)(current_price - prev_ema) + prev_ema
# timeperiods would be number of days between calculation
# so long might be 50days and short could be 15 days

def EMA_calc(data:dict):
    daily_price = np.array([float(val["5. adjusted close"]) for val in data["Time Series (Daily)"].values()])
    curr_price = daily_price[-1]

    interval_short = 15
    interval_long = 60
    k_short = 2/(interval_short + 1)
    k_long = 2/(interval_long + 1)

    
    '''
        gets first EMA using SMA so rest of EMAs can be calculated
    '''
    curr_EMA_short = k_short * (curr_price - sum(daily_price[:interval_short])) + sum(daily_price[:interval_short])
    curr_EMA_long = k_long * (curr_price - sum(daily_price[:interval_long])) + sum(daily_price[:interval_long])

    EMA_short_vec = np.zeros(len(daily_price))
    EMA_long_vec = np.zeros(len(daily_price))

    ''' 
        loop through rest of daily prices starting at 1 since [0] is caluclated
        and calculates EMA, short/long, for each
    '''
    for i in range(1,len(daily_price)):
        EMA_short_vec[i] = curr_EMA_short
        EMA_long_vec[i] = curr_EMA_long
        curr_EMA_short = k_short * (curr_price - curr_EMA_short) + curr_EMA_short
        curr_EMA_long = k_long * (curr_price - curr_EMA_long) + curr_EMA_long


    return EMA_long_vec,EMA_short_vec


EMA_long,EMA_short = EMA_calc(data)

print(EMA_long[-3:])

#data["Time Series (Daily)"]

#Weekly_price = np.array([vals["OBV"] for vals in data_Week["Weekly Adjusted Time Series"].values()])


#print(OBV.shape)
#print(len(OBV))
