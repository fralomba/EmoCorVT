import json
import operator
import pprint
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import nltk
nltk.download('punkt')
import os
import sys
import shutil

from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EmotionOptions
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from empath import Empath

JSON_file = ""
data_folder = ""
sender_name = ""
def detect_emotion(sentence, APIKEY):		#IBM emotion detector
    try:
    	natural_language_understanding = NaturalLanguageUnderstandingV1(
    	    version='2018-03-16',
    	    iam_apikey=APIKEY,
    	    url='https://gateway-syd.watsonplatform.net/natural-language-understanding/api'
    	)

    	response = natural_language_understanding.analyze(text=sentence, features=Features(emotion=EmotionOptions())).get_result()

    	emotions_response = response["emotion"]["document"]["emotion"]

    	max_likely_emotion = max(emotions_response.items(), key=operator.itemgetter(1))[0]
    	print('max_likely_emotion:', max_likely_emotion)
    	return max_likely_emotion
    except Exception as e:
        return 25

def sentiment_analyzer_scores(sentence, analyser):	# Vader sentiment analysis
    
    try:
        score = analyser.polarity_scores(sentence)
        print("Vader Sentiment Analysis: {}".format(str(score)))
        return score
    except Exception as e:
        return 26

def textBlobSentimentAnalyze(sentence):		# textBlob sentiment analysis
	
    try:
        utterance = TextBlob(sentence)
        print(utterance.sentiment)
        return 0
    except Exception as e:
        return 27

def textProcessing(JSON, DATA, USERNAME, APIKEY):

    global JSON_file
    global data_folder
    global sender_name

    JSON_file = JSON
    data_folder = DATA
    sender_name = USERNAME
    
    if not os.path.isfile(JSON_file):
        return 201
    
    if not os.path.isdir(data_folder):
        return 202
    
    if data_folder[-1:] == "/":
        return 203

    analyser = SentimentIntensityAnalyzer()			# istance of vader sentiment analyzer

    lexicon = Empath()		#instance of empath analyser
    emotions_list = ['fear', 'joy', 'anger', 'sadness', 'disgust']
    model = "reddit"


    with open(JSON_file, encoding='utf-8-sig') as json_file:
        try:

            try:
                json_data = json.load(json_file)
            except Exception as e:
                return 23

            chat = json_data["chats"]["list"]
            sentences = []

            text_emotions = []

            for i in range(len(chat[0]["messages"])):		# appends to a list all the messages
                if (chat[0]["messages"][i]["from"]).replace(" ", "") == sender_name and len(chat[0]["messages"][i]["text"]) > 6:
                    sentences.append(chat[0]["messages"][i]["text"])

            for i in range(len(emotions_list)):			# creates a category for each emotion
            	lexicon.create_category(emotions_list[i],[emotions_list[i]], model=model)

            best_em = []		# will contain empath analysis results
            emotions_results = []

            res = {}
            neg = []
            neutral = []
            pos = []

            for j in range(len(sentences)):
                if sentences[j] != '':
                    print('')
                    print(sentences[j])
                    output = detect_emotion(sentences[j], APIKEY)
                    if output == 25:
                        return output
                    text_emotions.append(output)

                    output = sentiment_analyzer_scores(sentences[j], analyser)
                    if output == 26:
                        return output

                    neg.append(output["neg"])
                    neutral.append(output["neu"])
                    pos.append(output["pos"])

                    if j != len(sentences) - 1:
                        neg.append(',')
                        neutral.append(',')
                        pos.append(',')

                    error = textBlobSentimentAnalyze(sentences[j])
                    if error != 0:
                        return error

                    for k in range(len(emotions_list)):			# tokenizes and analyzes the sentences
                        tokens = nltk.word_tokenize(sentences[j])
                        emotions_results = lexicon.analyze(tokens, normalize=True, categories=[emotions_list[k]])
                        res = {**res, **emotions_results}           # merge all results in one dictionary

                    print(res)

                    emotions_results = []


                    max_likely_emotions_empath = max(res.items(), key=operator.itemgetter(1))[0]

                    if max(res.items(), key=operator.itemgetter(1))[1] != 0.0:
                        print('max empath:',max_likely_emotions_empath)

                    print('')

            if not os.path.isfile(data_folder + "/sentences.txt"):
                print("Creating and wrting into:'sentences.txt' ...")
                sentences = np.asarray(sentences)
                np.savetxt(data_folder + "/sentences.txt", sentences, fmt="%s")      #saves sentences

            else:
                return 280

            if not os.path.isfile(data_folder + "/text_emotions.txt"):
                print("Creating and wrting into:'text_emotions.txt' ...")
                text_emotions = np.asarray(text_emotions)
                np.savetxt(data_folder + "/text_emotions.txt", text_emotions, fmt="%s")      #saves emotions

            else:
                return 281

            if not os.path.isfile(data_folder + "/sentiment_types.txt"):
                print("Creating and wrting into:'sentiment_types.txt' ...")
                sentiment_types = []
                sentiment_types.append(neg)
                sentiment_types.append(neutral)
                sentiment_types.append(pos)
                sentiment_types = np.asarray(sentiment_types)
                np.savetxt(data_folder + "/sentiment_types.txt", sentiment_types, fmt="%s")      #saves sentiment types
            else:
                return 282

            return 0
        except Exception as e:
            print(e)
            return 24


if __name__=="__main__":

    if len(sys.argv) < 4:
        exit(10)

    JSON_file = str(sys.argv[1])
    data_folder = str(sys.argv[3])
    sender_name = str(sys.argv[4])
    APIKEY = str(sys.argv[5])
    temp_frames_folder = data_folder + "/videoFrames"


    error = textProcessing()
    print(error)
    exit(error)



    
