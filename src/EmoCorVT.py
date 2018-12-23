import video_tagging
import text_emotion_detection
import dataset_creation
import statistics
import empath_on_ISEAR
import os


def errorTreatment(error):


	# video_tagging.py

	if error == 10:
		print("Too few arguments. ")

	elif error == 101:
		print("JSON file does not exist. ")

	elif error == 102:
		print("data-directory does not exist. ")

	elif error == 103:
		print("Video file does not exist. ")	

	elif error == 104:
		print("Do not add '/' to the end of the data-directory PATH. ")

	elif error == 12: 
		print("Some error occurred extracting the frames from the video. ")

	elif error == 121:
		print("A directory named 'videoFrames' already exists at the data-directory PATH. ")

	elif error == 13:
		print("Some error occurred ordering the frames of the video.")

	elif error == 14:
		print("Some error occurred opening JSON file. ")

	elif error == 15:
		print("Some error occurred opening or during the labeling of the frames. ")

	elif error == 151:
		print("A file named 'image_emotions.txt' or 'image_frameWindow.txt' already exists at the data-directory PATH. ")

	elif error == 16:
		print("Some erro occurred deleting the frames folder. ")

	# text_emotion_detection.py

	elif error == 20:
		print("Too few arguments. ")

	elif error == 201:
		print("JSON file does not exist. ")

	elif error == 202:
		print("data-directory does not exist. ")	

	elif error == 204:
		print("Do not add '/' to the end of the data-directory PATH. ")

	elif error == 23:
		print("Error reading JSON file. Is it a JSON file?")

	elif error == 24:
		print("Error treating the file. ")

	elif error == 25:
		print("Error detecting the emotion. ")

	elif error == 26:
		print("Error during the sentiment analysis. ")

	elif error == 27:
		print("Error during the TextBlob analysis. ")

	elif error == 280:
		print("File 'sentences.txt' already exists at the data-directory PATH. ")

	elif error == 281:
		print("File 'text_emotions.txt' already exists at the data-directory PATH. ")

	elif error == 282:
		print("File 'sentiment_types.txt' already exists at the data-directory PATH. ")

	# dataset_creation.py

	elif error == 30:
		print("Too few arguments. ")

	elif error == 301:
		print("data-directory does not exist. ")

	elif error == 302:
		print("Do not add '/' to the end of the data-directory PATH. ")

	elif error == 32:
		print("File 'sentences.txt' at the data-directory PATH can't be read. ")

	elif error == 33:
		print("File 'text_emotions.txt' at the data-directory PATH can't be read. ")

	elif error == 34:
		print("File 'image_emotions.txt' at the data-directory PATH can't be read. ")

	elif error == 35:
		print("File 'image_frameWindow.txt' at the data-directory PATH can't be read. ")

	elif error == 36:
		print("File 'sentiment_types.txt' at the data-directory PATH can't be read. ")

	elif error == 37:
		print("Error creating the dataset. ")

	elif error == 38:
		print("Error writing the dataset into the .csv file. ")

	elif error == 39:
		print("Error deleting some file used in the creation of dataset.csv. ")

	# statistics.py

	elif error == 40:
		print("Too few arguments. ")

	elif error == 401:
		print("Introduced dataset file does not exist. ")

	elif error == 41:
		print("Some error occurred while statistics were being done. ")

	# empath_on_ISEAR.py

	elif error == 50:
		print("Too few arguments. ")

	elif error == 51:
		print("Some error occurred while executing Empath with ISEAR.csv courpus. ")


if __name__ == "__main__":

	os.system('cls' if os.name == 'nt' else 'clear')

	print("##############   Welcome to EmoCorVT!   ############## ")

	try:
		while True:
			print("")
			print("")
			print("")
			print("Please, insert a job and press enter:")
			print("")
			print("1: Label the video.")
			print("2: Process the text with the IBM Watson machine (Key needed). ")
			print("3: Create a dataset with all the data. ")
			print("4: Run some statistics over the data. ")
			print("5: ISEAR corpus thingie. ")
			print("0: To stop the program. ")

			job = input()

			if int(job) == 1:

				print("A kind reminder before the video labelling:")
				print("Remember that it will take a fair amount of time to label the video frames if the mentioned is longer than 5 minutes and message amount is high (more than 10).")
				print("Do you still want to continue? y/n")
				answer = input()
				if answer == "y" or answer == "Y":
					
					print("Please, write the PATH to the Telegram-generated JSON file, where the conversation is.")
					JSON_file = input()
					
					print("Please, write the PATH to the video.")
					video_file = input()

					print("Please, write the PATH to the directory where the data will be stored. DO NOT WRITE THE LAST '/' ")
					data_folder = input()

					print("Please, write the NAME of the user whose messages have be analysed. All together, with no blank SPACES.")
					username = input()

					error = video_tagging.videoProcessing(JSON_file, video_file, data_folder, username)
					errorTreatment(int(error))

			elif int(job) == 2:
				
				print("A kind reminder before the text emotion detection:")
				print("Remeber that you need a valid IBM watson key in order to execute this. Also, it can take a fair amount of time depending on message amount that is to be evaluated. ")
				print("Do you still want to continue? y/n")
				answer = input()
				if answer == "y" or answer == "Y":
					
					print("Please, write a valid and legal API-Key of IBM Watson machine. ")
					Api_Key = input()

					print("Please, write the PATH to the Telegram-generated JSON file, where the conversation is.")
					JSON_file = input()

					print("Please, write the PATH to the directory where the data will be stored. DO NOT WRITE THE LAST '/' ")
					data_folder = input()

					print("Please, write the NAME of the user whose messages have be analysed. All together, with no blank SPACES.")
					username = input()

					error = text_emotion_detection.textProcessing(JSON_file, data_folder, username, Api_Key)
					errorTreatment(int(error))


			elif int(job) == 3:

				print("A kind reminder before the dataset creation:")
				print("Remeber that to create the full dataset, first video and text emotion detection has to be performed. ")
				print("Do you still want to continue? y/n")
				answer = input()
				if answer == "y" or answer == "Y":

					print("Please, write the PATH to the directory where the data will be stored. DO NOT WRITE THE LAST '/' ")
					data_folder = input()

					error = dataset_creation.createDataset(data_folder)
					errorTreatment(int(error))				
			elif int(job) == 4:
				
				print("A kind reminder before doing the statistics:")
				print("Remeber that a dataset must be available in order to perform the statistics. ")
				print("Do you still want to continue? y/n")
				answer = input()
				if answer == "y" or answer == "Y":

					print("Please, write the PATH to the dataset")
					dataset = input()

					error = statistics.doStatistics(dataset)
					errorTreatment(int(error))

			elif int(job) == 5:
				
				print("A kind reminder before doing the statistics:")
				print("ISEAR.csv file corpus is needed. It can be downloaded from the internet. ")
				print("Do you still want to continue? y/n")
				answer = input()
				if answer == "y" or answer == "Y":

					print("Please, write the PATH to the directory where the data will be stored. DO NOT WRITE THE LAST '/' ")
					data_folder = input()

					print("Please, write the PATH to the ISEAR.csv corpus file.")
					isear_corpus = input()

					error = empath_on_ISEAR.executeEmpathOnISEAR(isear_corpus, data_folder)
					errorTreatment(int(error))

			elif int(job) == 0:
				break
			else:
				print("Please, introduce only the number that corresponds to the job and press enter.") 

	except Exception as e:
		print("Some error has occurred: " + str(e))
		exit(1)

	exit(0)




