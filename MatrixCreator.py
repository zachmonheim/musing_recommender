'''
Load csv file into and find constants to use to
generate scores to fill matrix for factorization

this assumes a filled csv dataset (every user has numbers for every item)

Created on May 28, 2019

@author: Zach Monheim
'''

import pandas as pd
import numpy as np
from builtins import int

#links MatrixFactorization module to use MF class
from Recommenders.MatrixFactorization import MF

#read in csv file
data = pd.read_csv('dataset.csv')


#creates an array of zeros to hold [score, user_id, item_id]
scoreSize = data.get(['user_id']).__len__()
scores = np.zeros(shape=(scoreSize, 3))

#n and m are used to find the dimensions of the matrix
n=1
m=1

for i in range(0, scoreSize):
    #finds values at i for each column in dataset
    currWatchTime = data.get(['watch_time']).to_numpy()[i]
    currShared = data.get(['shared']).to_numpy()[i]
    currLiked = data.get(['liked']).to_numpy()[i]
    currUser = data.get(['user_id']).to_numpy()[i]
    currItem = data.get(['item_id']).to_numpy()[i]
    
    #if the item id or user id is larger than previous ids, replace n and/or m
    if(currItem > m):
        m = currItem[0]
    if(currUser > n):
        n = currUser[0]
    
    #determine weights
    A = 1/600
    B = 1
    C = 1
    
    #calculates score based on weights
    currScore = int(round(A*currWatchTime[0])) + B*currLiked + C*currShared
    
    #adds calculated score to scores array of tuples
    scores[i] = [currScore, currUser, currItem]


score_matrix = np.empty([n + 1, m + 1])
for i in range(scoreSize):
    score_matrix[int(scores[i][1]), int(scores[i][2])] = scores[i][0]


print(score_matrix)

#uses matrix factorization to train and print matrix with a collaborative filter
mf = MF(score_matrix, K=9, alpha=0.1, beta=0.01, iterations=20)
mf.train()
print(mf.sgd())
print(mf.get_rating(4, 3))
np.set_printoptions(precision=3)
print(mf.full_matrix())
