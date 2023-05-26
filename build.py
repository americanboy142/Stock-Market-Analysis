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

class Build_Admin():
    '''
        all functions needed to build csv/dataframe for numerical analysis
    '''
    def __init__(self,ticker) -> None:
        # get daily data for given ticker
        self.Daily_Data = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={ticker}&outputsize=full&apikey={key.API_KEY}').json()
        
        # gets daily prices from data, and reverse order so index 0 is current
        self.Daily_Price, self.Daily_Volume =  np.array([(float(val["5. adjusted close"]),float(val["6. volume"])) for val in self.Daily_Data["Time Series (Daily)"].values()])[::-1].T

    '''
        difference bettween daily prices
    '''
    def calc_daily_gain_loss(self,data:dict):
        '''
            takes in full call returns numpy array of daily gain/loss
            daily gain would return > 0
        '''
        open = np.array([float(val["1. open"]) for val in data["Time Series (Daily)"].values()])
        close = np.array([float(val["4. close"]) for val in data["Time Series (Daily)"].values()])

        return close - open

    '''
        RSI 14 day interval
    '''
    def RSI_calc(self,daily_gain_loss):
        '''
            using 14 days as time period
        '''
        interval = 14
        # RS = avgU / avgD
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

    '''
        EMA SHORT AND LONG
        returns (short,long,price)
    '''
    def EMA_calc(self,daily_price):
        interval_short = 15
        interval_long = 60
        k_short = 2/(interval_short + 1)
        k_long = 2/(interval_long + 1)
        
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
    

    def OBV_calc(self,daily_price,daily_volume):
        daily_compar = np.where(daily_price[:-1]<daily_price[1:], -1, np.where(daily_price[:-1]>daily_price[1:],1,0))

        adjsted_volumes = daily_volume[:-1] * daily_compar

        return np.cumsum(adjsted_volumes[::-1])[::-1]


    '''
        call functions and combine into a dictionary
    '''
    def Build(self) -> dict:
        '''
            Names and order: "EMA Short","EMA Long","RSI","OBV","Daily Price"
        '''
        RSI = self.RSI_calc(self.calc_daily_gain_loss(self.Daily_Data))
        EMA_short , EMA_long , daily_price = self.EMA_calc(self.Daily_Price)
        OBV = self.OBV_calc(self.Daily_Price,self.Daily_Volume)

        return {"EMA Short" : EMA_short,
                    "EMA Long": EMA_long, 
                    "RSI": RSI,
                    "OBV": OBV,
                    "Daily Price": daily_price}



main = Build_Admin('VOO').Build()
print(main)
    








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
