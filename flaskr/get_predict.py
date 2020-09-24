import math
import pandas_datareader as web 
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight') 
import datetime

def buy_or_sell():
	
	end = datetime.date.today()

	df = web.DataReader('AAPL', data_source='yahoo', start='2015-01-01', end=end)


	#new df with df[close]
	close_data = df.filter(['Close'])

	#convert to np array
	close_dataset=close_data.values

	#number of rows to train model on
	training_data_len = math.ceil(len(close_dataset) * .8) #pour entrainer sur 80% de notre data

	training_data_len

	#data scaling
	scaler = MinMaxScaler(feature_range=(0,1))
	scaled_close_data = scaler.fit_transform(close_dataset)

	scaled_close_data

	# create scaled training dataset
	train_close_data = scaled_close_data[0:training_data_len, :]

	#split the data into x_train and y_train sets
	x_train = []
	y_train = []

	for i in range(60, len(train_close_data)):
	    x_train.append(train_close_data[i-60:i, 0])
	    y_train.append(train_close_data[i,0]) #60 values from index 0 to 59

	#utiliser un réseau de neurones récurrent pour prdéire le cours de la bourse #supervised DL

	#converting x_train and y_train into np arrays
	x_train, y_train = np.array(x_train), np.array(y_train)

	x_train.shape
	#x_train.shape[0] for 1st value

	#reshaping the data
	x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1)) #x_train.shape == 60
	x_train.shape
	#y_train = np.reshape(y_train, ())

	#build the LSTM model

	model = Sequential()
	#50 nerons
	model.add(LSTM(50, return_sequences=True, input_shape= (x_train.shape[1], 1)))
	model.add(LSTM(50, return_sequences=False))
	#25neurons
	model.add(Dense(25))
	model.add(Dense(1))

	#compile the model
	model.compile(optimizer='adam', loss='mean_squared_error')

	#training
	model.fit(x_train, y_train, batch_size=1, epochs=1)

	#testing dataset creation
	#scaled values array from index 1084 to 1144 creation
	test_data = scaled_close_data[training_data_len - 60: , :]

	#x_test and y_test data sets creation
	x_test= []
	y_test= close_dataset[training_data_len:, :]

	for i in range (60, len(test_data)):
	    x_test.append(test_data[i-60:i, 0])
	    #y_test.append()

	#converting data to np array 
	x_test = np.array(x_test)

	#reshaping the data #we need a 3 dimensional shape
	x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

	x_test.shape

	#get the model predicted price values
	predictions = model.predict(x_test)
	predictions = scaler.inverse_transform(predictions) #unscaling the values




	#get the quote
	apple_quote = web.DataReader('AAPL', data_source='yahoo', start='2015-01-01', end=end)
	# new dataframe creation
	new_df = apple_quote.filter(['Close'])
	#getting the last 60 days closing price values & conversion df to np array
	last_60_days = new_df[-60:].values

	#data scaling between 0 and 1
	last_60_days_scaled = scaler.transform(last_60_days)

	#empty list creation
	X_test = []
	#append the 60 past days
	X_test.append(last_60_days_scaled)
	#convert to np array
	X_test = np.array(X_test)
	#reshaping
	X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

	#get predicted scaled price
	pred_price = model.predict(X_test)
	#unscaling
	pred_price = scaler.inverse_transform(pred_price)


	#apple_quote2 = web.DataReader('AAPL', data_source='yahoo', start='2019-09-03', end=end)

	last_day = new_df[-1:].values
	last_day

	diif = last_day - pred_price

	if diif < 0: #baisse
	    advise ="i advise you to buy"
	    #print(advise)
	    return advise
	elif diif > 0: #hausse
	    advise="i advise you to sell"
	    #print(advise)
	    return advise
