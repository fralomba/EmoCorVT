import pandas as pd
import numpy as np
import sys
import os

def eraseFiles(sent, textEm, imEm, imFr, sentTyp):
	try:
		print("Deleting restant files ...")
		os.remove(sent)
		os.remove(textEm)
		os.remove(imEm)
		os.remove(imFr)
		os.remove(sentTyp)
		return 0

	except Exception as e:
		print(str(e))
		return 39


def createDataset(DATA):
	

	data_folder = DATA

	if not os.path.isdir(data_folder):
		return 301

	if data_folder[-1:] == "/":
		return 302

	sentences_txt = data_folder + '/sentences.txt'
	text_emotions_txt = data_folder + '/text_emotions.txt'
	image_emotions_txt = data_folder + '/image_emotions.txt'
	image_frameWindow_txt = data_folder + '/image_frameWindow.txt'
	sentiment_types_txt = data_folder + '/sentiment_types.txt'

	try:
		sentences = pd.read_csv(sentences_txt, delimiter = '\t', header=None)
		dataset_rows = len(sentences)
	except Exception as e:
		print(str(e))
		return 32

	try:
		text_emotions = pd.read_csv(text_emotions_txt, sep=" ", header=None)
	except Exception as e:
		print(str(e))
		return 33

	try:
		frames_emotions = pd.read_csv(image_emotions_txt, header=None)
	except Exception as e:
		print(str(e))
		return 34

	try:
		frames_data = pd.read_csv(image_frameWindow_txt, sep=" ", header=None)
	except Exception as e:
		print(str(e))
		return 35

	try:
		sentiment_types = np.array(pd.read_csv(sentiment_types_txt, sep = ',', header=None))
	except Exception as e:
		return 36

	neg = np.array([i for i in sentiment_types[0]]).reshape((dataset_rows,1))
	neutral = np.array([i for i in sentiment_types[1]]).reshape((dataset_rows,1))
	pos = np.array([i for i in sentiment_types[2]]).reshape((dataset_rows,1))

	try:
		dataset = pd.DataFrame(np.column_stack([sentences, text_emotions, frames_data[0], frames_data[1], frames_emotions, neg, neutral, pos]), 
	                               	columns=['sentences', 'text_emotions', 'starting_frame', 'ending_frame', 'frames_emotions', 'neg', 'neutral', 'pos'])
	except Exception as e:
		print(str(e))
		return 37
	
	try:
		dataset.to_csv(data_folder + '/dataset.csv', encoding='utf-8', index=False)
	except Exception as e:
		print(str(e))
		return 38

	error = eraseFiles(sentences_txt, text_emotions_txt, image_emotions_txt, image_frameWindow_txt, sentiment_types_txt)
	if error != 0:
		return error

	return 0


if __name__=="__main__":
	
	if len(sys.argv) < 2:
		exit(30)

	data_folder = str(sys.argv[1])
	error = createDataset(data_folder)
	print(error)
	exit(error)		