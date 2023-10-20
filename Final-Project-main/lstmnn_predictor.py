# -*- coding: utf-8 -*-
"""LSTMNN_predictor.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pqLkfaJwoMCvqxD4SBJfxXWfna5w9cm0
"""

#REFERENCE FOR THE CODE
#https://www.youtube.com/watch?v=hpfQE0bTeA4
#https://www.youtube.com/watch?v=lhrCz6t7rmQ

pip install pandas_ta

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
import pandas_ta as ta
#pandas technical analysis module as we need technical indicators

#Load the data from Yahoo Finance module
#In this case Tesla stock price
data = yf.download(tickers='VOO', start = '2012-01-01', end = '2023-03-25')
data.head(10)

#Adding technical indicators
data['RSI'] = ta.rsi(data.Close, length=15)
#Fast moving average
data['EMAF'] = ta.ema(data.Close, length=20)
#Medium moving average
data['EMAM'] = ta.ema(data.Close, length=100)
#Slow moving average
data['EMAS'] = ta.ema(data.Close, length=150)

#Adding target column
#Calculating the difference between the close price and open price
data['Target'] = data['Adj Close'] - data.Open
data['Target'] = data['Target'].shift(-1)

#Closing price of the next day
#Obtained by shifting the day 1 back
#That's the column with the predictions that I'll be making
data['PredictNextClose'] = data['Adj Close'].shift(-1)

#Removing missing values and unnecessary columns
data.dropna(inplace=True)
data.reset_index(inplace=True)
data.drop(['Volume', 'Close', 'Date'], axis=1, inplace=True)

data_set = data.iloc[:, 0:11]
pd.set_option('display.max_columns', None)

data_set.head(5)

#Applying the MinMaxScaler so I can have data ranging betwen 0 and 1
from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range=(0, 1))
data_set_scaled = sc.fit_transform(data_set)
print(data_set_scaled)

#Multiple feature from data provided to the model
X = []

#This is the number of days you want to look back
backcandles = 30
print(data_set_scaled.shape[0])
#This is the part where the columns are getting processed 
for j in range(8):
  X.append([])
  for i in range(backcandles, data_set_scaled.shape[0]):
    X[j].append(data_set_scaled[i-backcandles:i, j])

#Move axis from 0 to possition 2
X = np.moveaxis(X, [0], [2])

#Erase first elements of y because of backcandles to match X length
#del(yi[0:backcandles])
#X, yi = np.array(X), np.array(yi)
#Choose -1 for last column, classification with -2...
X, yi = np.array(X), np.array(data_set_scaled[backcandles:, -1])
y = np.reshape(yi, (len(yi), 1))
#y=sc.fit_transform(yi)
#X_train = np.reshape(X_train, (Xtrain.shape[0], X_train.shape[1], 1))

print(X.shape)
#print(X)
print(y.shape)
#print(y)

#Another comperhansions for X
#X = np.array([data_set_scaled[i-backcandles:i, :4].copy() for i in range(backcandles, len(data_set_scaled))])
#print(X)
#print(X.shape)

#Splitting the data
splitlimit = int(len(X)*0.8)
print(splitlimit)
X_train, X_test = X[:splitlimit], X[splitlimit:]
y_train, y_test = y[:splitlimit], y[splitlimit:]

print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)
print(y_train)

from prompt_toolkit.shortcuts.dialogs import input_dialog
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dropout
from keras.layers import Dense
from keras.layers import TimeDistributed

import tensorflow as tf
import keras
from keras import optimizers
from keras.callbacks import History
from keras.models import Model
from keras.layers import Input, Activation, concatenate

#The model is fed two dimentional matix (days back to predict + the columns )
lstm_input = Input(shape=(backcandles, 8), name='lstm_input')
inputs = LSTM(100, name='first_layer')(lstm_input)
inputs = Dense(1, name='dense_layer')(inputs)
output = Activation('tanh', name='output')(inputs)
model = Model(inputs=lstm_input, outputs=output)
adam = optimizers.Nadam()
model.compile(optimizer=adam, loss='mse')
model.fit(x=X_train, y=y_train, batch_size=15, epochs=30, shuffle=True, validation_split = 0.1)

y_pred = model.predict(X_test)
for i in range(10):
  print(y_pred[i], y_test[i])

plt.figure(figsize=(16,8))
plt.plot(y_test, color = 'blue', label = 'Test')
plt.plot(y_pred, color = 'red', label = 'pred')
plt.legend()
plt.show()

#REFERENCE FOR THE CODE
#https://www.youtube.com/watch?v=hpfQE0bTeA4
#https://www.youtube.com/watch?v=lhrCz6t7rmQ