import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools
import os
import sys


def correlation(x, y):
	emotions = pd.DataFrame({'text':x, 'images':y})
	print(emotions)

	emotions['text'] = emotions['text'].astype('category').cat.codes
	emotions['images'] = emotions['images'].astype('category').cat.codes

	correlation = emotions.corr()
	print(correlation)

# --------------------------------------------- start data handling -----------------------------------------------

def doStatistics(DATASET):

	try:
		data = pd.read_csv(DATASET)

		# if not os.path.exists(data):
		# 	return 101

		text_emotions = data['text_emotions']
		image_emotions = data['frames_emotions']

		correlation(text_emotions,image_emotions)		# computes and prints the correlation between labels


		negative = data['neg']
		neutral = data['neutral']
		positive = data['pos']

		thresholds = [0.33, 0.66]
		sentiment = []

		for neg, neu, pos in zip(negative, neutral, positive):
			if neu == 1.0:
				if neu < thresholds[0]:
					sentiment.append(('neutral', 'weak', neu))
				elif thresholds[0] < neu < thresholds[1]:
					sentiment.append(('neutral', 'normal', neu))
				else:
					sentiment.append(('neutral', 'strong', neu))

			elif neg > pos:
				if neg < thresholds[0]:
					sentiment.append(('neg', 'weak', neg))
				elif thresholds[0] < neg < thresholds[1]:
					sentiment.append(('neg', 'normal', neg))
				else:
					sentiment.append(('neg', 'strong', neg))

			else:
				if pos < thresholds[0]:
					sentiment.append(('pos', 'weak', pos))
				elif thresholds[0] < pos < thresholds[1]:
					sentiment.append(('pos', 'normal', pos))
				else:
					sentiment.append(('pos', 'strong', pos))


		sentiment_type = [sentiment[i][0] for i in range(len(sentiment))]
		sentiment_strength = [sentiment[i][1] for i in range(len(sentiment))]
		sentiment_strength_values = [sentiment[i][2] for i in range(len(sentiment))]


		overall_neg_anger, overall_neg_sadness, overall_neg_joy, overall_neg_disgust, overall_neg_fear = ([] for i in range(5))
		overall_neu_anger, overall_neu_sadness, overall_neu_joy, overall_neu_disgust, overall_neu_fear = ([] for i in range(5))
		overall_pos_anger, overall_pos_sadness, overall_pos_joy, overall_pos_disgust, overall_pos_fear = ([] for i in range(5))

		for emo, neg, neu, pos in zip(text_emotions, negative, neutral, positive):
			if emo == 'anger':
				overall_neg_anger.append(neg)
				overall_neu_anger.append(neu)
				overall_pos_anger.append(pos)

			if emo == 'sadness':
				overall_neg_sadness.append(neg)
				overall_neu_sadness.append(neu)
				overall_pos_sadness.append(pos)

			if emo == 'joy':
				overall_neg_joy.append(neg)
				overall_neu_joy.append(neu)
				overall_pos_joy.append(pos)

			if emo == 'disgust':
				overall_neg_disgust.append(neg)
				overall_neu_disgust.append(neu)
				overall_pos_disgust.append(pos)

			if emo == 'fear':
				overall_neg_fear.append(neg)
				overall_neu_fear.append(neu)
				overall_pos_fear.append(pos)


		box_neg = [overall_neg_anger, overall_neg_sadness, overall_neg_joy, overall_neg_disgust, overall_neg_fear]
		box_neu = [overall_neu_anger, overall_neu_sadness, overall_neu_joy, overall_neu_disgust, overall_neu_fear]
		box_pos = [overall_pos_anger, overall_pos_sadness, overall_pos_joy, overall_pos_disgust, overall_pos_fear]

		emotions = ['anger', 'sadness', 'joy', 'disgust', 'fear']


		# --------------------------------------------- start plots -----------------------------------------------


		plt.scatter(text_emotions,image_emotions, alpha=0.2)		# figure 1
		plt.xlabel('text emotions')
		plt.ylabel('image emotions')
		plt.show()

		fig = plt.figure()		# figure 2
		ax1 = fig.add_subplot(111)
		ax1.scatter(range(38),text_emotions, s = 15, alpha=0.5, color = 'red')
		ax1.scatter(range(38),image_emotions, s = 15, alpha=0.5, color = 'blue')
		plt.legend(loc = 'upper center', bbox_to_anchor=(0.5, 1.1), ncol = 2);
		plt.xlabel('message id')
		plt.ylabel('emotions')
		plt.show()

		plt.scatter(sentiment_type,sentiment_strength, alpha=0.2) 		# type vs strength
		plt.xlabel('sentiment type')
		plt.ylabel('sentiment strength')
		plt.show()

		plt.scatter(sentiment_type,sentiment_strength_values, alpha=0.2)	# type vs strength values
		plt.xlabel('sentiment type')
		plt.ylabel('sentiment strength values')
		plt.show()

		fig = plt.figure()
		fig.suptitle('sentences overall negativity', fontsize=14, fontweight='bold')
		ax1 = fig.add_subplot(111)
		ax1.boxplot(box_neg)
		ax1.set_xticklabels([em for em in emotions])
		ax1.set_xlabel('emotions')
		plt.show()

		fig = plt.figure()
		fig.suptitle('sentences overall neutrality', fontsize=14, fontweight='bold')
		ax1 = fig.add_subplot(111)
		ax1.boxplot(box_neu)
		ax1.set_xticklabels([em for em in emotions])
		ax1.set_xlabel('emotions')
		plt.show()

		fig = plt.figure()
		fig.suptitle('sentences overall positivity', fontsize=14, fontweight='bold')
		ax1 = fig.add_subplot(111)
		ax1.boxplot(box_pos)
		ax1.set_xticklabels([em for em in emotions])
		ax1.set_xlabel('emotions')
		plt.show()
		return 0
	except Exception as e:
		print(str(e))
		return 41

if __name__=="__main__":
	
	if len(sys.argv) < 2:
		exit(40)

	dataset = str(sys.argv[1])
	error = createDataset(dataset)
	print(error)
	exit(error)

