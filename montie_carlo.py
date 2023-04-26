# e = number drawn from normal distribution, mean at 0, std =1
# u = expected annual rate of return
# s_t = price at t
# y = time interval which equals a week = 7
# o expected annual volatility
# s0 - current price
# u = r_f+b(r_m-r_f)
# r_f = risk free ratw of return
# b = beta of stock against market
# = coveriance (return on stock, return of market)/ varience (return on market)
# r_m = expected rate of return of market portfolio

def book_value(bal_sheet) -> float:
    return (bal_sheet['totalAssets'][0]-bal_sheet['totalLiabilities'][0])/bal_sheet['commonStockSharesOutstanding'][0]

def P_B_ratio(data,bal_sheet) -> float:
    """calculated the price book ratio of a given stock"""  
    print(data['Weekly_Price'][0]/book_value(bal_sheet))
    return 0.0

import pandas as pd
data = pd.read_csv('csv_files/AAPL.csv')
bal_sheet = pd.read_csv('csv_files/AAPL_BAL.csv')
#P_B_ratio(data,bal_sheet)

def risk_free_ROR():
    '''
    current 30 day tresury bill rate of return
    '''
    return 3.36

def market_beta(stock_data,market_data=None):
    import numpy as np
    stock_price = np.array(stock_data['Weekly_Price'])
    #market_price = np.array(market_data['Weekly_Price'])
    #stock_return = (stock_price[0] - stock_price[6])/stock_price[6]
    #market_return = (market_price[0] - market_price[6])/market_price[6]
    stock_split = np.split(stock_price[:364], 52)
    #market_split = np.split(market_price[:364], 52)
    stock_returns = [0.0]*52
    #market_returns = [0.0]*52
    for i in range(len(stock_split)):
        stock_returns[i] = (stock_split[i][0] - stock_split[i][6])/stock_split[i][6]
        #market_returns = (market_split[i][0] - market_split[i][6])/market_split[i][6]
    #print(deal)
    #print(np.cov(stock_returns))
    print(stock_price.shape)
    #return np.cov([[stock_returns],[market_returns]])/np.variance(market_returns)

market_beta(data)