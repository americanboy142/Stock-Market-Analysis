import requests
import key
import pandas as pd

url = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=AAPL&apikey={key.API_KEY}'
r = requests.get(url)
data = r.json()
'''
print(data)
import json

with open('test.json', 'w') as f:
    json.dump(data, f)

import json


with open("test.json", "r") as f:
    data = json.load(f)

'''

income = pd.json_normalize(data["annualReports"])

income.to_csv(f'csv_files/AAPL_IN.csv',index=False)

#print(income)