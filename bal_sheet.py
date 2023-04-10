import requests
import key

""" url = f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=AAPL&apikey={key.API_KEY}'
r = requests.get(url)
data = r.json() """

import json


""" with open('test.json', 'w') as f:
    json.dump(data, f) """

with open("test.json", "r") as f:
    data = json.load(f)


import pandas as pd

balence = pd.json_normalize(data["annualReports"])

balence.to_csv(f'csv_files/AAPL_BAL.csv',index=False)

#print(data)