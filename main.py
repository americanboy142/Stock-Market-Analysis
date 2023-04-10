import numpy as np
import pandas as pd
import news
import time



symbols = ['IBM','AAPL']
curr_news_scores = {}
for sym in symbols:
    news_data = news.call(sym)
    curr_news_scores = news.score(news_data,curr_news_scores)
    time.sleep(5)



import json

with open('json_files/news_main.json', 'w') as f:
    json.dump(curr_news_scores, f)

print(curr_news_scores)





