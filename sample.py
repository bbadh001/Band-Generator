import numpy as np
import random
import io
import sys
from keras.models import load_model

def getData():
	datafile = 'bandnames.txt'
	with io.open(datafile, encoding='utf-8') as f:
		text = f.read().lower()
		chars = sorted(list(set(text)))
		VOCAB_SIZE = len(chars)
		return text, chars, VOCAB_SIZE

def sample(preds, temperature=1.0):
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

def nameToUpper(n):
	name = list(n)
	if name[0].isalpha():
		name[0] = name[0].upper()
	for i in range(1,len(name)):
		if name[i].isalpha() and name[i-1] == ' ':
			name[i] = name[i].upper()
	return "".join(name)

def generateName(model,SEQ_LENGTH,VOCAB_SIZE,index_to_char,char_to_index,text):
    start_index = random.randint(0, len(text) - SEQ_LENGTH - 1)
    generated = ''
    sentence = text[start_index: start_index + SEQ_LENGTH]
    generated += sentence

    for i in range(200):
        x_pred = np.zeros((1, SEQ_LENGTH, VOCAB_SIZE))
        for t, char in enumerate(sentence):
            x_pred[0, t, char_to_index[char]] = 1.0
        preds = model.predict(x_pred, verbose=0)[0]
        next_index = sample(preds,1.0)
        next_char = index_to_char[next_index]
        generated += next_char
        sentence = sentence[1:] + next_char

    names = generated.split('\n')
    names = names[5:-1]
    for i,name in enumerate(names):
    	names[i] = nameToUpper(name)
    return names

def main():
	VOCAB_SIZE = 38
	SEQ_LENGTH = 30
	data,chars,VOCAB_SIZE  = getData() 
	index_to_char = {index:char for index, char in enumerate(chars)}
	char_to_index = {char:index for index, char in enumerate(chars)}

	model = load_model('models/band_gen_LSTM_epoch_25.h5')
	continueSampling = input("Enter 's' to sample a new set of names (enter anything else to quit): ")
	while continueSampling == "s":
		names = generateName(model,SEQ_LENGTH,VOCAB_SIZE,index_to_char,char_to_index,data)
		for i,name in enumerate(names):
			print("(" + str(i+1) + ") " + str(name))
		print("")
		continueSampling = input("Enter 's' to sample a new set of names (enter anything else to quit): ")

if __name__ == "__main__":
    main()