
def news_to_dict(data):
    """
        Given a news api response as is will return updated dictionary, with most current news.
    """
    
    dict = {}
    for j in range(len(data["feed"])):

        date = data['feed'][j]['time_published'][:8]

        for i in range(len(data['feed'][j]['ticker_sentiment'])):
            
            curr_tick = data['feed'][j]['ticker_sentiment'][i]["ticker"]
            # in form {'BABA':{ time: [{'relevance_score': '0.038811', 'ticker_sentiment_score': '-0.012711', 'ticker_sentiment_label': 'Neutral'}], ... }}

            if curr_tick not in dict:
                dict[curr_tick] = {}
            
            if date not in dict[curr_tick]:
                dict[curr_tick][date] = [{key: data['feed'][j]['ticker_sentiment'][i][key] for key in data['feed'][j]['ticker_sentiment'][i] if key != 'ticker'}]
            else:
                dict[curr_tick][date].append({key: data['feed'][j]['ticker_sentiment'][i][key] for key in data['feed'][j]['ticker_sentiment'][i] if key != 'ticker'})
    return dict

    
def GET_HISTORIC_NEWS_SCORES():
    from json import load
    with open('json_files/news_scores.json', 'r') as f:
        return load(f)

def WRITE_NEWS(scores):
    from json import dump
    with open('json_files/news_scores.json', 'w') as f:
        dump(scores, f)

def score(data,news_scores={}):
    '''
        return the bear/bull scores of given raw news data
        -1 => bear , 0 => nothing , 1 => bull
        only returns scores if number of articles is > 2
        sample call => news.score(data,curr_scores), data: News api call
        curr_scores: dictinary of scores calulated from other calls
        returns average score of ones that have been calulated
    '''
    import pandas as pd
    import numpy as np 

    News = news_to_dict(data)
    for symb in News:
        
        News_df = pd.DataFrame()

        length = sum(len(News[symb][date]) for date in News[symb])

        if length > 2:
            for i in News[symb]:
                temp = pd.DataFrame(News[symb][i])
                dates = np.full(len(temp),i)
                temp.insert(0,'dates',dates)
                News_df = pd.concat([News_df,temp])

            ticker_score = np.array(News_df['ticker_sentiment_score']).astype(float)

            score_avg = sum(ticker_score)/len(News_df['ticker_sentiment_score'])
            if symb not in news_scores:
                news_scores[symb] = score_avg.round(5)
            else:
                news_scores[symb] = ((news_scores[symb] + score_avg) / 2).round(5)
            

    return(news_scores)


def call(symb):
    import key
    '''
        call for news.
        returns news api call, as json object
    '''
    import requests

    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={symb}&apikey={key.API_KEY}'
    r = requests.get(url)
    return r.json()


def tops(data,n):
    '''
        using the dictinary from scores call
        returns the top n scores and sorted scores, i.e. highest bull prediction
    '''
    import itertools as it

    sorted_data_dict = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))
    if n > len(sorted_data_dict)-1:
        n = len(sorted_data_dict)-1
    best_n = dict(it.islice(sorted_data_dict.items(),n))

    return best_n, sorted_data_dict

def reset_news_scores():
    import json
    with open('json_files/news_main.json','w') as f:
        json.dump({},f)