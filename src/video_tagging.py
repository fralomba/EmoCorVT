import cv2
import os
import re
import json
import numpy as np 
import sys
import shutil

from datetime import datetime
from collections import Counter

temp_frames_folder = ""
JSON_file = ""
video_file = ""
data_folder = ""
sender_name = ""

def extractFrames():
    global temp_frames_folder
    global video_file
    try:
        if os.path.isdir(temp_frames_folder):
            return 121 # Directory already exists.
        
        os.mkdir(temp_frames_folder)
        cap = cv2.VideoCapture(video_file)
        count = 0
        while (cap.isOpened()):
            # Capture frame-by-frame
            ret, frame = cap.read()
     
            if ret == True:
                print('Read %d frame: ' % count, ret)
                cv2.imwrite(os.path.join(temp_frames_folder, "frame{:d}.jpg".format(count)), frame, [cv2.IMWRITE_JPEG_QUALITY, 20])  # save frame as JPEG file
                count += 1
            else:
                break
     
        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()
        return 0
    except:
        return 12


def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [atoi(c) for c in re.split('(\d+)', text)]

def orderFrames():
    try:
        global temp_frames_folder
        frames = [filename for filename in temp_frames_folder]
        frames.sort(key=natural_keys)

        dictionary = {key:'neutral' for key in frames}
        return dictionary
    except:
        return 13

def deleteFrames():

	try:
		global temp_frames_folder
		shutil.rmtree(temp_frames_folder)
		return 0
	except:
		return 16

def videoProcessing(JSON, VIDEO, DATA, USERNAME):
    
    global temp_frames_folder
    global JSON_file
    global video_file
    global data_folder
    global sender_name

    JSON_file = JSON
    video_file = VIDEO
    data_folder = DATA
    sender_name = USERNAME
    temp_frames_folder = data_folder + "/videoFrames"


    if not os.path.isfile(JSON_file):
        return 101

    if not os.path.isdir(data_folder):
        return 102

    if not os.path.isfile(video_file):
        return 103

    if data_folder[-1:] == "/":
        return 104

    print("Frame extraction...")

    error = extractFrames()

    if error != 0:
        return error

    print("Frame ordering...")

    frames = orderFrames()

    if frames == 13:
        return frames

    print("Trimming received messages...")

    try:
        with open(JSON_file, encoding='utf-8-sig') as json_file:
            json_data = json.load(json_file)
            # print(json.dumps(json_data["chats"]["list"], indent=4, sort_keys=True))

            chat = json_data["chats"]["list"]
            length = len(chat[0]["messages"])

            message_idx = []
            sender = []

            start = datetime.strptime(chat[0]["messages"][0]["date"], '%Y-%m-%dT%H:%M:%S')

            for i in range(length):       # appends to a list all the timestamps
                if (chat[0]["messages"][i]["from"]).replace(" ", "") == sender_name and len(chat[0]["messages"][i]["text"]) > 6:

                    delta = datetime.strptime(chat[0]["messages"][i]["date"], '%Y-%m-%dT%H:%M:%S')
                    message_idx.append((delta - start).seconds)
                    sender.append(chat[0]["messages"][i]["from"])
    except:
        return 14

    print("Starting labeling...")

    try:  
        # message_idx = [1, 2] # DELETE THIS!!!! IT'S JUST FOR THE TESTS            
        frames_idx = [i * 30 for i in message_idx]

        offset = 30

        tmp = []    # array containing the 30 emotions every 30 frames
        final_emotions = []     # array containing the final emotions from images
        final_frameWindows = np.zeros((2, len(frames_idx)))	# array containing the frame windows (first and last).
        print(final_frameWindows)
        j = 0
        for key in frames_idx:
            tmp.clear()
            for i in range(30):         # number of frames to show

                img = cv2.imread(temp_frames_folder+'/frame'+str(offset + key + i)+'.jpg',0)

                cv2.namedWindow('frame'+str(offset + key + i))        # Create a named window
                cv2.moveWindow('frame'+str(offset + key + i), 40,30)  # Move it to (40,30)
                cv2.imshow('frame'+str(offset + key + i), img)

                k = cv2.waitKey(0)
                if k == 13:         # wait for ENTER key to change image
                    cv2.destroyAllWindows()
                elif k == ord('a'):
                    frames[key] = "angry"
                    tmp.append(frames[key])
                    cv2.destroyAllWindows()
                elif k == ord('s'):
                    frames[key] = "sadness"
                    tmp.append(frames[key])
                    cv2.destroyAllWindows()
                elif k == ord('d'):
                    frames[key] = "disgust"
                    tmp.append(frames[key])
                    cv2.destroyAllWindows()
                elif k == ord('j'):
                    frames[key] = "joy"
                    tmp.append(frames[key])
                    cv2.destroyAllWindows()
                elif k == ord('f'):
                    frames[key] = "fear"
                    tmp.append(frames[key])
                    cv2.destroyAllWindows()

            counter = Counter(tmp)
            print(counter)

            final_frameWindows[j][0] = key
            final_frameWindows[j][1] = key + 30            
            j = j+1

            final_emotions.append(counter.most_common(1)[0][0])
    except Exception as e:
        print(e)
        return 15        

    print("Label saving...")

    if not os.path.isfile(data_folder+"/image_emotions.txt") and not os.path.isfile(data_folder+"/image_frameWindow.txt"):

        final_emotions = np.asarray(final_emotions)
        final_frameWindows = np.asarray(final_frameWindows)
        print("Creating and wrting into:'image_emotions.txt' ...")
        np.savetxt(data_folder + "/image_emotions.txt", final_emotions, fmt="%s")

        print("Creating and wrting into:'image_frameWindow.txt' ...")
        np.savetxt(data_folder + "/image_frameWindow.txt", final_frameWindows, fmt = "%s")
    else:
    	return 151

    print("Frames deleting...")

    deleteFrames()
    return 0

 
if __name__=="__main__":

    if len(sys.argv) < 4:
        exit(10)

    JSON_file = str(sys.argv[1])
    video_file = str(sys.argv[2])
    data_folder = str(sys.argv[3])
    sender_name = str(sys.argv[4])
    temp_frames_folder = data_folder + "/videoFrames"

    error = videoProcessing(JSON_file, video_file, data_folder, sender_name)
    exit(error)