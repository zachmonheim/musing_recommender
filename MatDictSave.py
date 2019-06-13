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

#create list of 1000 keywords - change number to adjust amount of keywords
keywords = []
keys = 0
while (keys < 1000):
    keywords.append(keys)
    keys += 1

#create a dataset with 1000 user IDs and assign a list of random keyword IDs based on a list of keywords
#represents the user profiles
userIDs = []

#change second number to change number of users
for i in xrange(0, 1000):
    #change second number to adjust max number of keywords any user may have
    userAmount = random.randint(1, 15)
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
itemIDs = []

#change second number to change number of videos
for i in xrange(0, 1000):
    #change second number to adjust max number of keywords any video may have
    itemAmount = random.randint(1, 15)
    x = random.sample(keywords, itemAmount)
    itemIDs.append(x)

#creates a dictionary out of the itemIDs matrix
item_d = dict()
key = 0
for i in itemIDs:
    item_d.setdefault(key, i)
    key += 1


#generate matrix of seen and not seen
#rows are user id's and columns are video id's
rows = len(userIDs)
cols = len(itemIDs)
#weight 1:9 the unseen to seen
seenUnseen = numpy.random.choice([x for x in xrange(0, 2, 1)], rows*cols, p=[0.9, 0.1])

seenUnseen.resize(rows,cols)


#saves object into file
def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


#saves userID matrix into file
save_obj(userIDs, "user_IDs")

#saves dictionary into file
save_obj(user_d, "user_dict")

#saves itemID matrix into file
save_obj(itemIDs, "item_IDs")

#saves dictionary into file
save_obj(item_d, "item_dict")

#saves matrix into file
save_obj(seenUnseen, "seenUnseen_matrix")

