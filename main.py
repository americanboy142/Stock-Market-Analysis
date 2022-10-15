import os
import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler


d_train = pd.read_csv("csv_files/AAPL.csv")
d_eval = d_train.iloc[:,5] # weekly_price

scaler = MinMaxScaler(feature_range = (0,1))
scaled_set = scaler.fit_trasform(d_eval)

x_train = []
y_train = []

for i in range(1/4*len(d_train),d_train):
    x_train.append(scaled_set[i-1/4*len(d_train):i,0])
    y_train.append(scaled_set[i,0])

x_train = np.array(x_train)
y_train = np.array(y_train)





