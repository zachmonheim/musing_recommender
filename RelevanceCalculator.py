'''
Finds relevance between videos based on the keywords present in a set of videos
Finds top 3 recommendations for user

Created on May 31, 2019

@author: Zach Monheim
'''
import random
import math
import numpy
from pip._vendor.msgpack.fallback import xrange

#create list of 1000 keywords
keywords = []
keys = 0
while (keys < 1000):
    keywords.append(keys)
    keys += 1

#create a dataset with 1000 user IDs and assign a list of random keyword IDs based on a list of keywords
#represents the user profiles
userIDs = []

for i in range(0,1000):
    userAmount = random.randint(1, 15)
    x = random.sample(keywords, userAmount)
    userIDs.append(x)

print(userIDs)

#creates a dictionary out of the userIDs matrix
user_d = dict()
key = 0
for i in userIDs:
    user_d.setdefault(key, i)
    key += 1


#create a dataset with 1000 item IDs and assign a list of random keyword IDs based on a list of keywords
#represents the tags on a video
itemIDs = []

for i in range(0,1000):
    itemAmount = random.randint(1, 15)
    x = random.sample(keywords, itemAmount)
    itemIDs.append(x)

print(itemIDs)
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
seenUnseen = numpy.random.choice([x for x in xrange(0, 2, 1)], rows*cols)
seenUnseen.resize(rows,cols)


'''
creates new dictionary with only videos unseen by a
specified user

input:
user = user specified to adjust dictionary to
unseen = matrix of seen and unseen
D = existing dictionary of items

output:
dictionary of unseen videos

example call:
unseenDict = findUnseen(392, seenUnseen, item_d)
'''
def findUnseen(user, unseen, D):
    diction = {}
    for i in range(0, len(D)):
        if unseen[user][i] == 0:
            diction.setdefault(i, D[i])
    
    return diction

'''
creates new dictionary with only videos seen by a
specified user

input:
user = user specified to adjust dictionary to
unseen = matrix of seen and unseen
D = existing dictionary of items

output:
dictionary of seen videos

example call:
seenDict = findSeen(392, seenUnseen, item_d)
'''
def findSeen(user, seen, D):
    diction = {}
    for i in range(0, len(D)):
        if seen[user][i] == 1:
            diction.setdefault(i, D[i])
    
    return diction

'''
find vids function finds vids with a certain keyword

input:
word = keyword to be found
V = list of videos (each video has it's own list of keywords

output:
list of video ids

example call:
listOfIDs = findVids(423, itemIDs)
'''
def findVids(word, V):
    listV = []
    index = 0
    for i in V:
        for j in i:
            if (j == word):
                listV.append(index) #adds index of video
                #listV.append(V[index])
        index += 1
    return listV


'''
counts how many videos include the keyword

input:
w = keyword to search for
V = list of videos (each video has it's own list of keywords

output:
returns count of how many videos have the given keyword

example call:
f(w) = numVids(321, keywords)
'''
def numVids(w, V):
    count = 0
    index = 0
    for i in V:
        for j in V[index]:
            if (j == w):
                count += 1
                j += len(V[index])
        index += 1
    return count

'''
finds the intersecting set between two lists

input:
lst1 = first list
lst2 = second list

output:
intersection set

example call:
intersectSet = intersection(dict[32], dict[532])
'''
#finds intersecting set between two sets (videos)
def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3

'''
distance of Vids finds distance between two videos given each id

input:
id1 = first video id
id2 = second video id
D = dictionary in question
V = dataset in question

output:
distance between the two videos

example call:
dist = distanceOfVids(32, 397, item_d, itemIDs)
'''
def distanceOfVids(id1, id2, D, V):
    N = len(D)
    dist = []
    
    intersect = intersection(D.get(id1), D.get(id2))
    for i in intersect:
        dist.append(math.log10(N/numVids(i, V)))
    
    sumOfVid = 0
    for i in dist:
        #sums the distances
        sumOfVid += i
    
    return sumOfVid

'''
finds distance between one video to all others

input:
index = index of video to be compared
D = dictionary in question
V = dataset in question

output:
list of distances between all videos and indexed video

example call:
dist[] = distances(451, item_d, itemIDs)
'''
def distances(index, D, V):
    N = len(D)
    dist = []
    for v in range(0, N):
        if (v == index):
            dist.append(-1)
        else:
            check = distanceOfVids(index, v, D, V)
            if check is 0:
                dist.append(50)
            else:
                dist.append(check)
    
    return dist

'''
based on the distance between videos
find relevance

input:
V = list of videos (each video has it's own list of keywords
D = dictionary of videos

output:
relevance in a numerical value (the greater the number the greater relevance it holds)

example call:
relevance = relevance(item_d, itemIDs)
'''
def relevance(D, V):
    rel = []
    index = 0
    for i in V:
        rel.append(1/distances(index, D, V)[index])
        index += 1
    return rel

'''
sort videos in terms of relevance
descending order
for ascending order take out reverse parameter

input:
V = list of videos (each video has it's own list of keywords
D = dictionary of videos

output:
list of relevances in sorted descending order

example call:
sortedRel = sortRel(item_d, itemIDs)
'''
def sortRel(D, V):
    return sorted(range(len(relevance(D, V))), key=relevance(D, V).__getitem__, reverse=True)


'''
finds top 3 recommended videos for specific user
only includes unseen videos

input:
D = dictionary of videos
V = list of videos (each video has it's own list of keywords
U = list of users (each user has it's own list of keywords

output:
prints out top 3 videos based on relevance to user

example call:
top3(0, item_d, itemIDs, userIDs)
'''
def top3(user, D, V, U):
    sortedRel = sortRel(D, V)
    
    recommend = []
    vids = []
    for word in U[user]:
        vids.append(findVids(word, V))
    
    unseen = findUnseen(user, seenUnseen, D)
    for i in sortedRel:
        for k in V[i]:
            for v in vids:
                for relK in v:
                    #checks if relevant k is k (indices)
                    #also checks if k is unseen
                    if relK is k and k in unseen:
                        recommend.append(i)
    
    print(recommend)
    print("Top three relevant videos for user 1 are: " + str(sortedRel[0]) + ", " + str(sortedRel[1]) + ", and " + str(sortedRel[2]))
    rec1 = "N/A"
    rec2 = "N/A"
    rec3 = "N/A"
    if (len(recommend) >= 3):
        rec3 = str(recommend[2])
    if (len(recommend) >= 2):
        rec2 = str(recommend[1])
    if (len(recommend) >= 1):
        rec1 = str(recommend[0])
        
    print("Top three relevant videos for user 1 are: " + rec1 + ", " + rec2 + ", and " + rec3)


