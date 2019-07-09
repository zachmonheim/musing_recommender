'''
A matrix and dictionary creator module to randomly generate
a matrix of videos, users, and keywords, and transition those
values into a dictionary, save that dictionary for repeated testing

Created on Jun 13, 2019

@author: Zach Monheim
'''
import random
import numpy
from pip._vendor.msgpack.fallback import xrange
import pickle

#determines number of user ids
numUsers = 1000
#determines number of video ids
numVideos = 1000

#create list of 1000 keywords - change number to adjust amount of keywords
keywords = []
keys = 0
while (keys < 1000):
    keywords.append(keys)
    keys += 1

#create a dataset with 1000 user IDs and assign a list of random keyword IDs based on a list of keywords
#represents the user profiles
userIDs = []

#creates numUsers amount of users
for i in xrange(0, numUsers):
    #change second number to adjust max number of keywords any user may have
    userAmount = random.randint(1, 5)
    x = random.sample(keywords, userAmount)
    userIDs.append(x)

#creates a dictionary out of the userIDs matrix to keep track of IDs throughout
user_d = dict()
key = 0
for i in userIDs:
    user_d.setdefault(key, i)
    key += 1


#create a dataset with 1000 item IDs and assign a list of random keyword IDs based on a list of keywords
#represents the tags on a video
videoIDs = []

#creates numVideos number of videos
for i in xrange(0, numVideos):
    #change second number to adjust max number of keywords any video may have
    itemAmount = random.randint(1, 5)
    x = random.sample(keywords, itemAmount)
    videoIDs.append(x)

#creates a dictionary out of the videoIDs matrix
video_d = dict()
key = 0
for i in videoIDs:
    video_d.setdefault(key, i)
    key += 1


#generate matrix of seen and not seen
#rows are user id's and columns are video id's
rows = len(userIDs)
cols = len(videoIDs)
#weight 1:9 the unseen to seen
seenUnseen = numpy.random.choice([x for x in xrange(0, 2, 1)], rows*cols, p=[0.9, 0.1])

seenUnseen.resize(rows,cols)

'''
creates list of tuples, to represent values for factorization
tuple
(userID, videoID, [secs watched, shared, watched])
or
nested tuples
(userID, videoID, (secs watched, shared, watched))
'''
ratings = []

for userid in xrange(0, numUsers):
    for videoid in xrange(0, numVideos):
        tup = [userid, videoid]
        score = []
        scAppend = score.append
        #if unseen, no tuple will be added
        if (seenUnseen[userid][videoid] == 1):
            #randomize a secs watched, shared, liked
            secWatched = random.randint(20, 1800)
            shared = random.randint(0, 1)
            liked = random.randint(0, 1)
            scAppend(secWatched)
            scAppend(shared)
            scAppend(liked)
            tup.append(score)
            #add tuple to overall list
            ratings.append(tuple(tup))


import numpy as np
from builtins import int

'''
creates matrix of 0s and nonzero values
0s represent unseen n video of m user
and nonzero values represent rating of n video by m user
'''
userids = [x[0] for x in ratings]
videoids = [x[1] for x in ratings]
scoreTuple = [x[2] for x in ratings]

size = len(ratings)

#creates an array of zeros to hold [score, user_id, item_id]
scores = np.zeros(shape=(size, 3))

#size of empty score matrix should be numUsers by numVideos
#n and m are used to find the dimensions of the matrix
n=numUsers
m=numVideos


for i in range(0, size):
    #finds values at i for in dataset
    currUser = userids[i]
    currVideo = videoids[i]
    currWatchTime = scoreTuple[i][0]
    currShared = scoreTuple[i][1]
    currLiked = scoreTuple[i][2]
    
    #determine weights
    A = 1/600
    B = 1
    C = 1
    
    
    #calculates score based on weights
    currScore = int(round(A*currWatchTime)) + B*currLiked + C*currShared
    
    
    #adds calculated score to scores array of tuples
    scores[i] = [currScore, currUser, currVideo]



#populates a score matrix with calculated scores
score_matrix = np.zeros([n, m])
for i in range(size):
    score_matrix[int(scores[i][1]), int(scores[i][2])] = int(scores[i][0])



#saves object into file
def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


#saves userID matrix into file
save_obj(userIDs, "user_IDs")

#saves dictionary into file
save_obj(user_d, "user_dict")

#saves itemID matrix into file
save_obj(videoIDs, "video_IDs")

#saves dictionary into file
save_obj(video_d, "video_dict")

#saves ratings list into file
save_obj(ratings, "ratings")

#saves score matrix into file
save_obj(score_matrix, "score_matrix")




'''
creating csv files
changing matrices into a zipped file of csv files

archive.zip
    dataScore.csv
    dataUser.csv
    dataVideo.csv
    
    
    
dataScore
user_id, video_id, score
1, 1, 3
1, 2, 4
2, 1, 1
etc.

dataUser
user_id, keywords
1, [13, 23, 26]
2, [5]
3, [1, 14]
etc.
'''

#create matrix that corresponds with desired csv layout
csvScoreMatrix = []
csvAppend = csvScoreMatrix.append
for u in xrange(numUsers):
    for v in xrange(numVideos):
        if (score_matrix[u][v] != 0):
            csvAppend([u, v, score_matrix[u][v]])

#creates matrix that has all keywords as one feature
csvUsers = []
userApp = csvUsers.append
u = 0
for k in userIDs:
    userApp([u, k])
    u += 1
    
#creates matrix that has all keywords as one feature
csvVideos = []
vidApp = csvVideos.append
u = 0
for k in userIDs:
    vidApp([u, k])
    u += 1

import pandas as pd

#puts into dataframes
dfUser = pd.DataFrame(userIDs, columns=['user_id', 'keywords'])
dfVideo = pd.DataFrame(videoIDs, columns=['video_id', 'keywords'])
dfScore = pd.DataFrame(csvScoreMatrix, columns=['user_id', 'video_id', 'score'])

#puts dataframes into csv files
dfUser.to_csv("dataUser.csv", encoding='utf-8', index=False)
dfVideo.to_csv("dataVideo.csv", encoding='utf-8', index=False)
dfScore.to_csv("dataScore.csv", encoding='utf-8', index=False)


import os
import zipfile

#compresses csv files into a zipped file
#replace path with wherever this file is save
new_zip = zipfile.ZipFile('*file path ending in archive.zip*', 'w')

for folder, subfolders, files in os.walk('*file path*'):
    
    for file in files:
        if file.startswith('dataScore') or file.startswith('dataUser') or file.startswith('dataVideo'):
            new_zip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), '*file path*'), compress_type = zipfile.ZIP_DEFLATED)
 
new_zip.close()
