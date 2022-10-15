# finance_api
Simple finance tool. Grabs all avalable data on top 50 of the top 500 companies. [Main code](finance_api.py)

[AAPL.csv](AAPL.csv) is an example of output.

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
