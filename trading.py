import numpy as np
import pandas
import pymongo
from pymongo import MongoClient
import streamlit as st
import pickle
import pandas as pd
import numpy as np
import os
import time
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model

@st.cache(hash_funcs={MongoClient: id})
def get_client():
    return MongoClient("mongodb://127.0.0.1/admin")

client = get_client()
db = client.local
collection = db.startup_log

#st.write(collection.find()[0])

db = client.finance

society_choice = st.sidebar.radio('chose a society',('Microsoft', 'Apple', 'Google'))

if society_choice == 'Microsoft':
	collection = db.MSFT
	model = keras.models.load_model("models/MSFT_model.h5",compile = False)




if society_choice == 'Google':
	collection = db.GOOGL
	model = keras.models.load_model("models/GOOGL_model.h5", compile = False)



if society_choice == 'Apple':
	collection = db.AAPL
	model = keras.models.load_model("models/AAPL_model.h5", compile = False)


#data = pd.DataFrame(list(collection.find()))
data = list(collection.find())




def buy_or_sell():

	#converting data to np array 
	x_test = np.array(data)

	#reshaping the data #we need a 3 dimensional shape
	x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1]))

	x_test.shape

	#get the model predicted price values
	predictions = model.predict(x_test)
	predictions = scaler.inverse_transform(predictions) #unscaling the values


	new_df = collection.filter(['Close'])
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
	diif = last_day - pred_price

	#return diif, last_day, pred_price
	return pred_price


	#??????????????
	# if diif < 0: #baisse
	#     advise ="i advise you to buy"
	#     #print(advise)
	#     return advise
	# elif diif > 0: #hausse
	#     advise="i advise you to sell"
	#     #print(advise)
	#     return advise



buy_or_sell()


bar = st.progress(0)

if st.button("predict tomorrow's stock price"):
	for i in range(11):
		bar.progress(i * 10)
		# wait
		time.sleep(0.07)

	if diif < 0: # decrease
		st.write("i advise you to sell")
	st.write("soon, stock exchang's predictions, xoxo")




