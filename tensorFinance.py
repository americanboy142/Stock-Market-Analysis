# this is to create a weekly prediction for the companies selected
# training and prediction

# will save the prediction in a column along with symbol
# will be used to compare with daily price

from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from six.moves import urllib

import tensorflow as tf
from tensorflow._api.v2 import feature_column
from tensorflow.python.eager.def_function import _evaluate_var_is_initialized
from tensorflow.python.feature_column.feature_column_v2 import NumericColumn
import tensorflow.compat.v2.feature_column as fc

from admin_func import split_df

df = pd.read_csv('csv_files/AAPL.csv')

#df["Weekly_Price"] = df["Weekly_Price"].shift(1,fill_value=160)
df = df.iloc[::-1]
df["Weekly_Price"] = df["Weekly_Price"].astype(float)

dftrain =  df.sample(frac=.8,random_state=0) # training data
dfeval = df.drop(dftrain.index) # testing data

y_train = dftrain.pop('Weekly_Price') # move weekly col to y_train//y_eval
y_eval = dfeval.pop('Weekly_Price')
print(y_train)
print(y_eval)

NUMERIC_COLUMNS = ["EMA_Short","EMA_Long","RSI","OBV","MACD"]

columns = []

for column in NUMERIC_COLUMNS:
    columns.append(tf.feature_column.numeric_column(column, dtype=tf.float32))

def make_input_func(data_df, lable_df, epochs=10,batch_size=32):
    def input_func():
        ds = tf.data.Dataset.from_tensor_slices((dict(data_df),lable_df))
        ds = ds.batch(batch_size).repeat(epochs)
        return ds
    return input_func

train_input_func = make_input_func(dftrain, y_train)
eval_input_func = make_input_func(dfeval, y_eval, epochs = 1)

print(len(y_train))
print(y_train.iloc[0])
numClasses = len(dftrain)

linear_fn = tf.estimator.LinearEstimator(head=tf.estimator.MultiLabelHead(n_classes=1),feature_columns=columns)


linear_fn.train(train_input_func)
eval_fn = linear_fn.evaluate(eval_input_func)


#print(eval_fn['accuracy'])


predict = list(linear_fn.predict(eval_input_func))

predictions_vs_actual = np.zeros((len(predict),3))


for predictions in range(len(predict)):
    predictions_vs_actual[predictions,1] = predict[predictions]["probabilities"][1]
    predictions_vs_actual[predictions,0] = y_eval[predictions]
    diff = predictions_vs_actual[predictions,1]-predictions_vs_actual[predictions,0]
    if diff < 0:
        predictions_vs_actual[predictions,2] = 1.0
    else:
        predictions_vs_actual[predictions,2] = 0.0

way_off = 0

for i in range(len(predictions_vs_actual)):
    way_off = way_off + predictions_vs_actual[i,2]

print(way_off, len(predictions_vs_actual))
