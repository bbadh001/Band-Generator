import numpy as np
import random
import io
import sys
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM, SimpleRNN
from keras.optimizers import RMSprop
from keras.layers.wrappers import TimeDistributed

def getData():
	""" Load data
	"""
	datafile = 'bandnames.txt'
	with io.open(datafile, encoding='utf-8') as f:
		text = f.read().lower()
		chars = sorted(list(set(text)))
		VOCAB_SIZE = len(chars)
		return text, chars, VOCAB_SIZE

def createModel(HIDDEN_UNITS,VOCAB_SIZE,SEQ_LENGTH):
	model = Sequential()
	model.add(LSTM(HIDDEN_UNITS, input_shape=(SEQ_LENGTH,VOCAB_SIZE)))
	model.add(Dense(VOCAB_SIZE))
	model.add(Activation('softmax'))
	optimizer = RMSprop(lr=0.005)
	model.compile(loss='categorical_crossentropy', optimizer=optimizer)
	return model

def shuffle_data(x, y):
	""" Shuffles training data in parallel after every epoch
	"""
    assert len(x) == len(y)
    p = np.random.permutation(len(x))
    return x[p], y[p]

def main():
	""" data: list of chars (each bandname seperated by a newline character)
	    chars: list of all unique characters in the dataset (can be thought of as a feature vector)
	    VOCAB_SIZE: number of unique characters 
	"""
	data,chars,VOCAB_SIZE  = getData() 
	print("Number of characters in data set: " + str(len(data)))
	print("Number of unique characters: " + str(VOCAB_SIZE))

	# mappings from index to chars (and vice versa):
	index_to_char = {index:char for index, char in enumerate(chars)}
	char_to_index = {char:index for index, char in enumerate(chars)}

	# creating training sequences and target characters 
	# skips N characters 
	SEQ_LENGTH = 30
	skip = 3
	sequences = []
	next_chars = []

	for i in range(0,len(data)-SEQ_LENGTH,skip):
		sequences.append(data[i:i+SEQ_LENGTH])
		next_chars.append(data[i+SEQ_LENGTH])

	X = np.zeros((len(sequences),SEQ_LENGTH,VOCAB_SIZE))
	y = np.zeros((len(sequences),VOCAB_SIZE))

	for i, sequence in enumerate(sequences):
		for j, char in enumerate(sequence):
			X[i,j,char_to_index[char]] = 1
			y[i,char_to_index[next_chars[i]]] = 1

	# creating LSTM
	HIDDEN_UNITS = 256
	model = createModel(HIDDEN_UNITS,VOCAB_SIZE,SEQ_LENGTH)

	# train loop
	epoch = 0
	while True:
	    model.fit(X, y, batch_size=128, verbose=1, epochs=1)
	    model.save('band_gen_LSTM_epoch_{}.h5'.format(epoch))
	    X, y = shuffle_data(X,y)
	    epoch += 1

if __name__ == "__main__":
    main()