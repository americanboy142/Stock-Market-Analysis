from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame
from pandas.core.indexes import period
from six.moves import urllib

import tensorflow as tf
from tensorflow._api.v2 import feature_column
from tensorflow.python.eager.def_function import _evaluate_var_is_initialized
from tensorflow.python.feature_column.feature_column_v2 import NumericColumn
import tensorflow.compat.v2.feature_column as fc


def make_input_func(data_df, lable_df, epochs=10,batch_size=32):
    def input_func():
        ds = tf.data.Dataset.from_tensor_slices((dict(data_df),lable_df))
        ds = ds.batch(batch_size).repeat(epochs)
        return ds
    return input_func


def split_df(df):
    '''
    Takes a data frame and returns a list
    also shifts "Weekly Price" column by 1
    [0] the first 2/3 of original
    [1] the last 1/3 of original
    '''
    dataframes = []

    df["Weekly_Price"] = df["Weekly_Price"].shift(1,fill_value=160)
    df.iloc[::-1]

    index_to_split = len(df) // 4
    start = 0
    end = index_to_split
    for split in range(4):
        temporary_df = df.iloc[start:end, :]
        dataframes.append(temporary_df)
        start += index_to_split
        end += index_to_split

    two_thirds = pd.concat([dataframes[0],dataframes[1],dataframes[2]])
    one_third = dataframes[3]
    split_list = [one_third,two_thirds]

    return split_list 


def GET_SYMBOLS():
    '''
    returns list of the first 50 symbols in nasdq.csv
    '''
    nasdq = pd.read_csv('nasdq.csv')

    nasdq_symbol = []

    nas_sort = nasdq.sort_values("Market Cap",ascending=False)

    count = 0
    for row in nas_sort["Symbol"]:
        count += 1
        if count <= 50:
            try:
                nasdq_symbol.append(row)
            except :
                pass
        else:
            break

    return nasdq_symbol



#deal = pd.read_csv("csv_files/AAPL.csv")

#for col in deal.columns:
#    print(col)