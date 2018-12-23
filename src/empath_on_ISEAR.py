import pandas as pd
import nltk
import operator
import os
import sys
import numpy as np

from empath import Empath


def executeEmpathOnISEAR(ISEAR, DATADIR):

	try:
		corpus = pd.read_csv(ISEAR, sep=',',header=None)

		if not os.path.isfile(DATADIR + "/labels_empath_on_ISEAR.txt"):

			lexicon = Empath()		#instance of empath analyser
			emotions_list = ['fear', 'joy', 'anger', 'sadness', 'disgust']
			model = "reddit"

			res = {}

			best_em = []		# will contain empath analysis results
			emotions_results = []

			for i in range(len(emotions_list)):			# creates a category for each emotion
				lexicon.create_category(emotions_list[i],[emotions_list[i]], model=model)

			for sentence in corpus[1]:
				for k in range(len(emotions_list)):			# tokenizes and analyzes the sentences
					tokens = nltk.word_tokenize(sentence)
					emotions_results = lexicon.analyze(tokens, normalize=True, categories=[emotions_list[k]])
					res = {**res, **emotions_results}		# merge all results in one dictionary

					emotion_results = []

				max_likely_emotions_empath = max(res.items(), key=operator.itemgetter(1))[0]

				if res[max_likely_emotions_empath] != 0.0:
					best_em.append(max_likely_emotions_empath)
				else:
					best_em.append('no_idea')

			best_em = np.asarray(best_em)
			np.savetxt(DATADIR + "/labels_empath_on_ISEAR.txt", best_em, fmt="%s")      #saves empath detection

		# ---------------------------------- if labels already exist: --------------------------------

		ISEAR_labels = corpus[0]

		empath_labels = pd.read_csv(DATADIR + '/labels_empath_on_ISEAR.txt', sep=',',header=None)

		detected_labels = [ISEAR_labels[i] for i in range(len(ISEAR_labels)) if empath_labels[0][i] != 'no_idea']
		matches = [ISEAR_labels[i] for i in range(len(ISEAR_labels)) if empath_labels[0][i] == ISEAR_labels[i]]

		detected_percentage = len(detected_labels)/len(ISEAR_labels)
		overall_accuracy = len(matches)/len(ISEAR_labels)
		detected_accuracy = len(matches)/len(detected_labels)

		print('detected_percentage:', detected_percentage)
		print('detected_accuracy:', detected_accuracy)
		print('overall_accuracy:', overall_accuracy)
		return 0
		
	except Exception as e:
		print(str(e))
		return 51

if __name__=="__main__":
	
	if len(sys.argv) < 3:
		exit(50)

	isear_csv = str(sys.argv[1])
	data_folder = str(sys.argv[2])
	error = createDataset(isear_csv, data_folder)
	print(error)
	exit(error)

