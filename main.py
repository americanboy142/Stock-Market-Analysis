import numpy as np
import pandas as pd
import news
import time
import json
import portfol_funcs as port

with open('json_files/news_main.json', 'r') as f:
    curr_news_scores = json.load(f)
 
symbols = ['AAPL']
for sym in symbols:
    news_data = news.call(sym)
    curr_news_scores = news.score(news_data,curr_news_scores)
    time.sleep(5)



with open('json_files/news_main.json', 'w') as f:
    json.dump(curr_news_scores, f)




tops = news.tops(curr_news_scores,5)

print(tops)

with open('json_files/port.json', 'r') as f:
    portfol = json.load(f)

port.news_check(curr_news_scores,portfol)





