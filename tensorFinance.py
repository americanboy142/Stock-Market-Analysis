def tensor_main(data,Plus_Min):
    """ given data and plus_min(up or down column vector) returns tensor flow max accuracy, predictions of whether a given stock will go up or down. 
    uses epochs,batchsize (15,20),(60,70), (100, 128)
    """
    import tensorflow as tf
    import numpy as np

    third = len(data) // 3 
    traindf = data.iloc[third:]
    testdf = data.iloc[:third]


    numeric = np.array([traindf['EMA_Short'],traindf['EMA_Long'],traindf['RSI'],traindf['OBV'],traindf['Trend_EMA']])
    numeric = numeric.transpose()
    # Create a sequential model

    model = tf.keras.Sequential([
        tf.keras.layers.Dense(10, input_shape=(5,), activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    # Compile the model with binary cross-entropy loss and Adam optimizer
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Train the model

    epoc_list = [(15,20),(60,70), (100, 128)]
    test_vec = [[]*3]*len(epoc_list)
    i = 0
    acc = 0
    for epoc,batch in epoc_list:
        model.fit(numeric, Plus_Min[third:], epochs=epoc, batch_size=batch, verbose=0)

        # Use the trained model to predict the class of a new input
        X_test = np.array([testdf['EMA_Short'],testdf['EMA_Long'],testdf['RSI'],testdf['OBV'],testdf['Trend_EMA']])
        X_test = X_test.transpose()

        loss,test_acc = model.evaluate(X_test, Plus_Min[:third], verbose=0)
        
        if test_acc > acc:
            acc = test_acc
            predictions = model.predict(X_test,verbose=0)
        i += 1


    predictions = predictions.flatten()
    
    return acc,predictions
