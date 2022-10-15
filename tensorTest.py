#from __future__ import absolute_import, division, print_function, unicode_literals

#import numpy as np
#import pandas as pd
#import matplotlib.pyplot as plt
#from six.moves import urllib

#import tensorflow as tf
#from tensorflow._api.v2 import feature_column
#from tensorflow.python.eager.def_function import _evaluate_var_is_initialized
#from tensorflow.python.feature_column.feature_column_v2 import NumericColumn
#import tensorflow.compat.v2.feature_column as fc

#dftrain = pd.read_csv('https://storage.googleapis.com/tf-datasets/titanic/train.csv') # training data
#dfeval = pd.read_csv('https://storage.googleapis.com/tf-datasets/titanic/eval.csv') # testing data

#y_train = dftrain.pop('survived') # move suvived col to y_train//y_eval
#y_eval = dfeval.pop('survived')

#print(len(y_train)/32)

#CATEGORICAL_COLUMNS = ['sex', 'n_siblings_spouses', 'parch', 'class', 'deck',
#                       'embark_town', 'alone']
#NUMERIC_COLUMNS = ['age', 'fare']

#columns = []

#for column in CATEGORICAL_COLUMNS:
#    grouped = dftrain[column].unique()
#    columns.append(tf.feature_column.categorical_column_with_vocabulary_list(column,grouped))


#for column in NUMERIC_COLUMNS:
#    columns.append(tf.feature_column.numeric_column(column, dtype=tf.float32))



#def make_input_func(data_df, lable_df, epochs=10,shuffle=True,batch_size=32):
#    def input_func():
#        ds = tf.data.Dataset.from_tensor_slices((dict(data_df),lable_df))
#        if shuffle:
#            ds = ds.shuffle(1000)
#        ds = ds.batch(batch_size).repeat(epochs)
#        return ds
#    return input_func

#train_input_func = make_input_func(dftrain, y_train)
#eval_input_func = make_input_func(dfeval, y_eval, epochs = 1, shuffle= False)

#linear_fn = tf.estimator.LinearClassifier(feature_columns=columns)

#linear_fn.train(train_input_func)
#eval_fn = linear_fn.evaluate(eval_input_func)


##print(eval_fn['accuracy'])


#predict = list(linear_fn.predict(eval_input_func))

#predictions_vs_actual = np.zeros((len(predict),3))


##for predictions in range(len(predict)):
##    predictions_vs_actual[predictions,1] = predict[predictions]["probabilities"][1]
##    predictions_vs_actual[predictions,0] = y_eval[predictions]
##    diff = predictions_vs_actual[predictions,1]-predictions_vs_actual[predictions,0]
##    if abs(diff) > .5:
##        predictions_vs_actual[predictions,2] = 1.0
##    else:
##        predictions_vs_actual[predictions,2] = 0.0

##way_off = 0

##for i in range(len(predictions_vs_actual)):
##    way_off = way_off + predictions_vs_actual[i,2]

##print(way_off, len(predictions_vs_actual))
##print(predictions_vs_actual)