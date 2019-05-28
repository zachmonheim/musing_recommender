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

#read in csv file
data = pd.read_csv('C:\\Users\\zmonh\\datasets\\smallMock.csv')

data_germany = data.drop('user_id', 1)


print(data.columns)

#three columns to keep track of 
print(data.get(['watch_time']))
print(data.get(['watch_time']).to_numpy()[5])


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
    
    print(currWatchTime)
    print(currItem)
    print(currUser)
    print(currShared)
    print(currLiked)
    
    #if the item id or user id is larger than previous ids, replace n and/or m
    if(currItem > m):
        m = currItem[0]
    if(currUser > n):
        n = currUser[0]
    
    #determine weights
    A = 1
    B = 1
    C = 1
    
    #regularizes watch time to not overpower score
    if (currWatchTime > 1200):
        currWatchTime = 3
    elif (currWatchTime > 800):
        currWatchTime = 2
    elif (currWatchTime > 400):
        currWatchTime = 1
    else:
        currWatchTime = 0
    
    #calculates score based on weights
    currScore = A*currWatchTime + B*currLiked + C*currShared
    
    print(currScore)
    
    #adds calculated score to scores array of tuples
    scores[i] = [currScore, currUser, currItem]
    print(scores)


score_matrix = np.empty([n + 1, m + 1])
for i in range(scoreSize):
    score_matrix[int(scores[i][1]), int(scores[i][2])] = scores[i][0]


'''
to round matrix if decimals present

np.around(score_matrix, decimals=0)
'''
print(score_matrix)







