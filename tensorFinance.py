def tensor_main(data,Plus_Min):
    " given data and plus_min(up or down column vector) returns tensor flow prediction of whether a given stock will go up or down. "
    import tensorflow as tf
    import numpy as np

    third = len(data) // 3 
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

    print("real:   ",Plus_Min)
    print(data.head())

    x = np.arange(len(data))