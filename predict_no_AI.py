import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


data = pd.read_csv('csv_files/AAPL.csv')

week_Price = np.array(data['Weekly_Price'])

Plus_Min = np.zeros(len(week_Price))

predict = np.zeros(len(week_Price))

for i in range(len(week_Price)-1,-1,-1):
    if week_Price[i] < week_Price[i-1]:
        Plus_Min[i] = 1
    else:
        Plus_Min[i] = 0 

# goal is to return percentage change up or down where 0 is down and 1 is up

def calculate_EMA_difference(short, long):
    dif = long - short

    trend = np.diff(dif) / dif[:-1]
    trend = np.insert(trend, 0, 0)

    return np.round(trend,4)


trend = calculate_EMA_difference(np.array(data['EMA_Short']),np.array(data['EMA_Long']))
data['Trend_EMA'] = trend

for i in range(len(trend)-1,-1,-1):
    if trend[i] < trend[i-1]:
        predict[i] = Plus_Min[i-1]
    else:
        if Plus_Min[i-1] == 0:
            predict[i] = 1 
        else:
            predict[i] = 0

count = 0

for i,el in enumerate(predict):
    if el == Plus_Min[i]:
        count +=1

print("percent correct =", count/len(trend))


def calculate_RSI_trend(rsi):

    trend = np.diff(rsi) / rsi[:-1]
    
    return np.round(trend,4)



rsi = data['RSI']

trend = calculate_RSI_trend(rsi)

data['RSI_Trend'] = trend


import tensorflow as tf

third = len(trend) // 3 
traindf = data.iloc[third:]
testdf = data.iloc[:third]


numeric = np.array([traindf['EMA_Short'],traindf['EMA_Long'],traindf['RSI'],traindf['OBV'],traindf['Trend_EMA']])
numeric = numeric.transpose()
print(numeric.shape)
print(Plus_Min[third:].shape)
print(Plus_Min[:third].shape)
# Create a sequential model

model = tf.keras.Sequential([
    tf.keras.layers.Dense(10, input_shape=(5,), activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

# Compile the model with binary cross-entropy loss and Adam optimizer
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model

epoc_list = [(10, 32), (15,20),(30,50),(60,70), (50, 64), (100, 128), (200, 256)]
test_vec = [[]*3]*len(epoc_list)
i = 0
for epoc,batch in epoc_list:
    history = model.fit(numeric, Plus_Min[third:], epochs=epoc, batch_size=batch, verbose=0)

    # Use the trained model to predict the class of a new input
    X_test = np.array([testdf['EMA_Short'],testdf['EMA_Long'],testdf['RSI'],testdf['OBV'],testdf['Trend_EMA']])
    X_test = X_test.transpose()
    #y_pred = model.predict(X_new, verbose=0)

    test_loss, test_acc = model.evaluate(X_test, Plus_Min[:third], verbose=0)

    test_vec[i] = [epoc,batch,test_acc]
    i += 1


print(test_vec)

print("predict:",predict)
print("real:   ",Plus_Min)
print(data.head())

x = np.arange(len(trend))

""" plt.plot(x, trend)
plt.yscale("log")
plt.show()
plt.plot(x, week_Price)
plt.show() """