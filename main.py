import numpy as np
import pandas as pd
import news
import time
import json
import portfol_funcs as port
import admin_func as admin

# ======================== NUMERIC ==============================
def numeric_predict(symbs):
    import tensorFinance as tf
    import predict_numeric as pn

    data = admin.CSV_to_DATA('AAPL')

    week_Price = np.array(data['Weekly_Price'])

    Plus_Min = pn.calculate_Puls_min(week_Price)
    non_tens_acc , non_tensor_predict = pn.predict(data,Plus_Min)

    tens_acc , tensor_predict = tf.tensor_main(data,Plus_Min)

    print(non_tens_acc,non_tensor_predict[0])
    print(tens_acc ,tensor_predict[0])

# ======================== NEWS =================================
def news_main(symbs):
    '''main news does not return anything'''

    # gets previusly ran news scores
    curr_news_scores = news.GET_HISTORIC_NEWS_SCORES()

    # loop through the given symbols and calls each symbole and retievs scores
    for sym in symbs:
        news_data = news.call(sym)
        if news_data != None:
            curr_news_scores = news.score(news_data,curr_news_scores)
            print(f'RUNNING: {sym}')
            print("Score:",curr_news_scores[sym])
        else:
            print('something when wrong with Call, make sure symbols are correct')
            return
        time.sleep(5)

    # sorts and graps top n scores
    tops,curr_news_scores = news.tops(curr_news_scores,5)

    # wirtes the calculated and sorted scores to news_scores.json
    news.WRITE_NEWS(curr_news_scores)

    print("Top Scores:", tops)

    curr_portfolio = port.EDIT_PORTFOLIO('r')

    port.news_check(curr_news_scores,curr_portfolio)

    check = input('update portfolio (Y/N)? ')
    if check == 'Y':
        print("Current Portfolio:",curr_portfolio)
        user = input("Add changes in the form\n=== <ticker>:B/S; === \n")
        updated_port = port.update_port(curr_news_scores,curr_portfolio,user)
        port.EDIT_PORTFOLIO('w',updated_port)
    else:
        return
    



symbols = ['APPF','AMD',"VZ","SPLK"]

user = input('News (N), Numeric (P), Search scores (S), Reset News (R) : ')

if user == 'N':
    news_main(symbols)
elif user == 'P':
    numeric_predict(symbols)
elif user == 'S':
    admin.search_news_scores(input('Ticker: '))
elif user == 'R':
    news.reset_news_scores()
else:
    print("end")

"""
SET UP TEST DATA    

df = pd.DataFrame({'EMA_DIFF': pn.calculate_EMA_difference(np.array(data["EMA_Short"]),np.array(data["EMA_Long"])),
                   'Plus_Min': pn.calculate_Puls_min(np.array(data['Weekly_Price']))
                   })
df.to_csv('csv_files\TEST_FUNCS.csv',index=False)
"""

"""
df = pd.DataFrame(np.array(pn.calculate_RSI_trend(np.array(data["RSI"]))))
df.to_csv('csv_files\TEST_RSI.csv',index=False)

"""

"""
with open('json_files/TEST_NEWS.json', 'r') as f:
    newss = json.load(f)


with open('json_files/TEST_NEWS.json', 'w') as f:
    json.dump(newss, f) 

news_dict = news.news_to_dict(newss)

with open('json_files/TEST_NEWS_TO_DICT.json', 'w') as f:
    json.dump(news_dict, f)

scores = news.score(newss)

with open('json_files/TEST_NEWS_SCORES.json', 'w') as f:
    json.dump(scores, f)



tops = news.tops(scores,5)

with open('json_files/TEST_NEWS_TOPS.json', 'w') as f:
    json.dump(tops, f)
 """



