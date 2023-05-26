import key
import json
import requests
import numpy as np
import matplotlib.pyplot as plt
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

dif = calc_daly_gain_loss(data)

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
    RS_arr = RS_arr[::-1]
    return  100-100/( 1 + RS_arr) 



RSI = RSI_calc(dif)



#RSI = RSI
#print(RSI[-3:])


#EMA = 2/(timeperiods+1)(current_price - prev_ema) + prev_ema
# timeperiods would be number of days between calculation
# so long might be 50days and short could be 15 days

def EMA_calc(data:dict):
    daily_price = np.array([float(val["5. adjusted close"]) for val in data["Time Series (Daily)"].values()])

    interval_short = 15
    interval_long = 60
    k_short = 2/(interval_short + 1)
    k_long = 2/(interval_long + 1)

    daily_price = daily_price[::-1]
    
    '''
        gets first EMA using SMA so rest of EMAs can be calculated using normal formula
    '''
    curr_EMA_short = np.mean(daily_price[:interval_short])
    curr_EMA_long = np.mean(daily_price[:interval_long])


    '''
        initialize arrays win None set to float so it can be filled properly 
    '''
    EMA_short_vec = np.full(len(daily_price), None, dtype= float)
    EMA_long_vec = np.full(len(daily_price), None, dtype= float)

    #EMA_short_vec[interval_short] = curr_EMA_short
    
    ''' 
        main loop to calculate respecitve emas
        starts at long interval
    '''
    for i in range(interval_long, len(daily_price)):
        EMA_short_vec[i] = curr_EMA_short
        EMA_long_vec[i] = curr_EMA_long
        curr_EMA_short = k_short * (daily_price[i] - curr_EMA_short) + curr_EMA_short
        curr_EMA_long = k_long * (daily_price[i] - curr_EMA_long) + curr_EMA_long

    # removes all None values from arrays then returns
    return EMA_short_vec[~np.isnan(EMA_short_vec)] , EMA_long_vec[~np.isnan(EMA_long_vec)], daily_price

def OBV_calc(data):
    daily_price,daily_volume = np.array([(float(val["5. adjusted close"]),float(val["6. volume"])) for val in data["Time Series (Daily)"].values()])[::-1].T
    #daily_volume = np.array([float(val["6. volume"]) for val in data["Time Series (Daily)"].values()])

    daily_compar = np.where(daily_price[:-1]<daily_price[1:], -1, np.where(daily_price[:-1]>daily_price[1:],1,0))

    adjsted_volumes = daily_volume[:-1] * daily_compar

    return np.cumsum(adjsted_volumes[::-1])[::-1]




OBV = OBV_calc(data)
#print(OBV)

EMA_short,EMA_long, price = EMA_calc(data)

#print(EMA_long[1:10])
n = len(EMA_long)

EMA_long = EMA_long[1:n]
#print(EMA_long[0])

#x = range(len(EMA_long))
x = range(200)

#print(len(EMA_short[:len(EMA_long)]))

'''plt.plot(x,EMA_long)
plt.plot(x,EMA_short[:len(EMA_long)])
plt.plot(x,price[:len(EMA_long)])
plt.legend(['EMA long','EMA short','price'])
plt.show()'''

plt.plot(x,EMA_long[-200:])
plt.plot(x,EMA_short[-200:])
plt.plot(x,price[-200:])
plt.plot(x,RSI[-200:])
plt.legend(['EMA long','EMA short','price', 'RSI', 'OBV'])
plt.show()

#data["Time Series (Daily)"]

#Weekly_price = np.array([vals["OBV"] for vals in data_Week["Weekly Adjusted Time Series"].values()])


#print(OBV.shape)
#print(len(OBV))

