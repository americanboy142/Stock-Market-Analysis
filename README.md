Simple finance tool. Grabs all avalable data on top 50 of the top 500 companies.

Using Alpha Advantage with private api key in key.py

[TEST.csv](csv_files/TEST.csv) is an example of output.

Data grabbed for each company:
  - EMA_Short
    - set to 15 days
  - EMA_Long
    - set to 50 days
  - RSI
  - OBV
  - MACD
  - Weekly_Price

set to iterate 5 times every minute for api restriction. 

[Predict](predict_numeric.py) is a non AI prediction combines different data to produce a prediction of stock price change.
Returns a array of predictions and accuracy of that prediction

[Tensor finance](tensorFinance.py) uses tensorflow's keras sequential model to predict the same thing as above.
Returns a array of predictions and accuracy of that prediction.

[News](news.py) Formats the news call from alpha and returns the top n, most likely to be bullish based on the news score.


