import numpy as np
import pandas as pd
import key
import csv

#nasdq = pd.read_csv('nasdq.csv')

#nasdq_symbol = []

#nas_sort = nasdq.sort_values("Market Cap",ascending=False)

#count = 0
#for row in nas_sort["Symbol"]:
#    count += 1
#    if count <= 50:
#        try:
#            nasdq_symbol.append(row)
#        except :
#            pass

#for i,symbol in enumerate(nasdq_symbol):
#    print(i%2)

#for i in nasdq_symbol:
#    open((i+".csv"), "x")

#
#thing = pd.read_csv("csv_files/AAPL.csv")
#
#del thing[thing.columns[0]]
#print(thing)
#
#thing.to_csv('csv_files/AAPL.csv',index=False)
#
#remove the index column if needed

deal = pd.read_csv("csv_files/AAPL.csv")


#thing = deal.to_dict()

deal["Weekly Price"] = deal["Weekly Price"].shift(1)

print(deal)

#deal["Weekly Price"] = deal.Weekly_sorted.shift(1)
#print(deal)