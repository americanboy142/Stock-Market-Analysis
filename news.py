
def news_to_table(data):
    """
        Given a news api response as is and current news.json
        will return updated dictionary, with most current news.
        Problem : essentially delets and rebuilds news.json
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


def score(data,news_scores={}):
    '''
        return the bear/bull scores of given data
        -1 => bear , 0 => nothing , 1 => bull
        only returns scores if number of articles is > 2
        sample call => news.score(data,curr_scores), data: News api call
        curr_scores: dictinary of scores calulated from other calls
        returns average score of ones that have been calulated
    '''
    import pandas as pd
    import numpy as np 

    News = news_to_table(data)
    for symb in News:

        News_df = pd.DataFrame()
        if len(News[symb]) > 2:
            for i in News[symb]:
                temp = pd.DataFrame(News[symb][i])
                dates = np.full(len(temp),i)
                temp.insert(0,'dates',dates)
                News_df = pd.concat([News_df,temp])

            #ticker_lable = np.array(News_df['ticker_sentiment_label'])
            ticker_score = np.array(News_df['ticker_sentiment_score']).astype(float)


            score_avg = sum(ticker_score)/len(News_df['ticker_sentiment_score'])
            if symb not in news_scores:
                news_scores[symb] = score_avg
            else:
                news_scores[symb] = (news_scores[symb] + score_avg) / 2
            
            news_scores[symb] = news_scores[symb].round(5)

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