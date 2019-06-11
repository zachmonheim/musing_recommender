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
import collections

#create list of 1000 keywords
keywords = []
keys = 0
while (keys < 1000):
    keywords.append(keys)
    keys += 1

#create a dataset with 1000 user IDs and assign a list of random keyword IDs based on a list of keywords
#represents the user profiles
userIDs = []

for i in xrange(0,1000):
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

for i in xrange(0,1000):
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
    default = diction.setdefault
    for i in range(0, len(D)):
        if unseen[user][i] == 0:
            default(i, D[i])
    
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
    default = diction.setdefault
    for i in range(0, len(D)):
        if seen[user][i] == 1:
            default(i, D[i])
    
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
    append = listV.append
    for i in V:
        for j in i:
            if (j == word):
                append(index) #adds index of video
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
            #checks if keyword is in video based on index
            if (j == w):
                count += 1
                #adds to j to escape loop once keyword found
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
    logg = math.log10
    append = dist.append
    lst1 = D.get(id1)
    lst2 = D.get(id2)
    
    #checks types to ensure no integers are being passed
    #to the intersection function so no intersections are repeated
    if type(lst1) is type(dist) and type(lst2) is type(dist):
        intersect = intersection(lst1, lst2)
        
        #over set of intersection, add calculated difference
        for i in intersect:
            append(logg(N/numVids(i, V)))
    
    
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
user = user id in question

output:
list of distances between all videos and indexed video

example call:
dist = distances(451, item_d, itemIDs, user)
'''
def sumDistances(index, D, V, user):
    N = len(D)
    distSum = 0
    #gets unseen dictionary
    unseen = findUnseen(user, seenUnseen, D)
    for v in xrange(0, N):
        #if v is the current video or it has been seen
        #do not count towards sum if either are true
        if (v is index or v in unseen):
            distSum += 0
        else:
            check = distanceOfVids(index, v, D, V)
            distSum += check
    
    return distSum

'''
based on the distance between videos
find relevance

input:
V = list of videos (each video has it's own list of keywords
D = dictionary of videos
user = user id in question

output:
relevance in a numerical value (the greater the number the greater relevance it holds)

example call:
relevance = relevance(item_d, itemIDs, 0)
'''
def relevance(D, V, user):
    rel = D
    index = 0
    
    update = rel.update
    for i in V:
        #finds the sum of distances for each video
        dist = sumDistances(index, D, V, user)
        #if the sum is 0, no relation to any other vids
        #then update with 0 otherwise update with inverse sum
        if (dist != 0):
            update({index:1/dist})
        else:
            update({index:0})
        index += 1
    #sorts relevance scores in descending order
    sortedrel = sorted(rel.items(), key=lambda kv: kv[1], reverse=True)
    #puts relevance scores in ordered dictionary
    sortrel = collections.OrderedDict(sortedrel)
    
    return sortrel


'''
finds top 3 recommended videos for specific user
only includes unseen videos

input:
userID = the id number of the user to find relevance for
D = dictionary of videos
V = list of videos (each video has it's own list of keywords
U = list of users (each user has it's own list of keywords

output:
prints out top 3 videos based on relevance to user

example call:
top3(0, item_d, itemIDs, userIDs)
'''
def top3(userID, D, V, U):
    sortedRel = relevance(D, V, userID)
    recommend = []
    vids = []
    
    vidAppend = vids.append
    #creates the U of R(U, v)
    #loops through user's tags to find vids according to those tags
    for word in U[userID]:
        vidAppend(findVids(word, V))
    
    #find unseen dictionary
    unseen = findUnseen(userID, seenUnseen, D)
    
    recAppend = recommend.append
    #iterates sorted relevance, i is index in sortedRel
    for i in sortedRel:
        #iterates through vids that share a keyword
        for v in vids:
            #k is a keyword in V[i] which is being iterated through
            #relK finds keyword in shared keyword videos
            for k, relK in product(V[i], v):
                #no duplicates in recommend
                duplicate = set(recommend)
                #checks if relevant k is k (indices)
                #also checks if k is unseen
                if relK is k and k in unseen and i not in duplicate:
                    recAppend(i)
    
    print(recommend)
    rec1 = "N/A"
    rec2 = "N/A"
    rec3 = "N/A"
    
    if (len(recommend) >= 3):
        rec3 = str(recommend[2])
    if (len(recommend) >= 2):
        rec2 = str(recommend[1])
    if (len(recommend) >= 1):
        rec1 = str(recommend[0])
        
    print("Top three relevant videos for user " + str(userID) + " are: " + rec1 + ", " + rec2 + ", and " + rec3)

#used to determine execution time of program
import time
start_time = time.time()
#run program with user ID of 0
top3(0, item_d, itemIDs, userIDs)
print("--- %s seconds ---" % (time.time() - start_time))

#used to determine execution time of functions
import profile
profile.run('top3(456, item_d, itemIDs, userIDs)')
