'''
Matrix creator but with the common dataset, using tuples

needs more even ratio of seen to unseen given that collaborative
filtering works better with more ratings

Created on Jun 14, 2019

@author: Zach Monheim
'''


import numpy as np
from builtins import int

#links MatrixFactorization module to use MF class
from Recommenders.MatrixFactorization import MF

import pickle

#this runs MatDictSave again (therefore does not preserve current matrices)
from Recommenders.MatDictSave import numUsers, numVideos

#loading object from file
def load_obj(name ):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

#loads userIDs matrix
ratings = load_obj("ratings")

userIDs = [x[0] for x in ratings]
videoIDs = [x[1] for x in ratings]
scoreTuple = [x[2] for x in ratings]

size = len(ratings)

#creates an array of zeros to hold [score, user_id, item_id]
scores = np.zeros(shape=(size, 3))

#size of empty score matrix should be numUsers by numVideos
#n and m are used to find the dimensions of the matrix
n=numUsers
m=numVideos
print(n)
print(m)

for i in range(0, size):
    #finds values at i for in dataset
    currUser = userIDs[i]
    currVideo = videoIDs[i]
    currWatchTime = scoreTuple[i][0]
    currShared = scoreTuple[i][1]
    currLiked = scoreTuple[i][2]
    
    
    ##use the numUsers and numVideos instead?
    #if the video id or user id is larger than previous ids, replace n and/or m
    if(currVideo > m):
        m = currVideo
    if(currUser > n):
        n = currUser
    
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
    score_matrix[int(scores[i][1]) - 1, int(scores[i][2]) - 1] = int(scores[i][0])


print(score_matrix)


#uses matrix factorization to train and print matrix with a collaborative filter
mf = MF(score_matrix, K=9, alpha=0.1, beta=0.01, iterations=20)
mf.train()
print(mf.sgd())
print(mf.get_rating(4, 3))
np.set_printoptions(precision=3)
print(mf.full_matrix())
