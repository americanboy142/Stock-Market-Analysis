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
    with open('json_files/news_main.json', 'r') as f:
        curr_news_scores = json.load(f)

    for sym in symbs:
        news_data = news.call(sym)
        if news_data != None:
            curr_news_scores = news.score(news_data,curr_news_scores)
        else:
            print('something when wrong with Call, make sure symbols are correct')
            return
        time.sleep(5)

    tops,curr_news_scores = news.tops(curr_news_scores,5)

    with open('json_files/news_main.json', 'w') as f:
        json.dump(curr_news_scores, f)


    print(tops)

    with open('json_files/port.json', 'r') as f:
        portfol = json.load(f)
    

    port.news_check(curr_news_scores,portfol)

    check = input('update portfolio (Y/N)? ')
    if check == 'Y':
        port.update_port(curr_news_scores)
    



symbols = ['APPF','AMD']

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



