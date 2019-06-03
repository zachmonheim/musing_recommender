'''
Finds relevance between videos based on the keywords present in a set of videos

Created on May 31, 2019

@author: zmonh
'''
import random
import math

#create list of 1000 keywords
keywords = []
keys = 0
while (keys < 1000):
    keywords.append(keys)
    keys += 1

#create a dataset with 1000 user IDs and assign a list of random keyword IDs based on a list of keywords
#represents the user profiles
userIDs = []

for i in range(1,1001):
    userAmount = random.randint(1, 15)
    x = random.sample(keywords, userAmount)
    userIDs.append(x)


#create a dataset with 1000 item IDs and assign a list of random keyword IDs based on a list of keywords
#represents the tags on a video
itemIDs = []

for i in range(1,1001):
    itemAmount = random.randint(1, 15)
    x = random.sample(keywords, itemAmount)
    itemIDs.append(x)

print(itemIDs[0])
print(itemIDs[2])
print(itemIDs[3])
print(itemIDs[4])
print(itemIDs[5])
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

print(findVids(302, itemIDs))

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
print(numVids(302, itemIDs))

'''
the distance of two vids based on their keywords in common?

input:
id1 = keyword list of v
id2 = keyword list of v*
V = list of videos (each video has it's own list of keywords

output:
list of distances between vids

example call:
distance = distancesOfVids(keywords)
'''
def distancesOfVids(V):
    dist = []
    N = len(V)
    
    for i in V:
        for word, val in i.items():
            if val > 0:
                dist.append(1)
    
    for word, val in dist.items():
        dist[word] = math.log10(N/float(val))
        
    return dist

def distanceOfVids(id1, id2, V):
    N = len(V)
        
    dist = dict.fromkeys(V[0].keys(), 0)
    for i in dist:
        for word, val in i.items():
            if val > 0:
                dist[word] += 1
    
    for word in dist.items():
        dist[word] = math.log10(N/numVids(word, V))
    
    return dist

'''
dist of vid finds distance of a vid at a specified index

input:
index = index of specific video's distance to determine
V = list of videos (each video has it's own list of keywords

output:
distance of specified vid

example call:
distance = distOfVid(445, itemIDs)
'''
def distOfVid(index, V):
    N = len(V)
    dist = []
    for j in V[index]:
        dist.append(math.log10(N/numVids(j, V)))
    
    sumOfVid = 0
    for i in dist:
        sumOfVid += i
    return sumOfVid
print(distOfVid(0, itemIDs))
print(distOfVid(2, itemIDs))
print(distOfVid(3, itemIDs))
print(distOfVid(4, itemIDs))
print(distOfVid(5, itemIDs))



'''
based on the distance between videos
find relevance

input:
V = list of videos (each video has it's own list of keywords

output:
relevance in a numerical value (the greater the number the greater relevance it holds)

example call:
relevance = relevance(itemIDs)
'''
def relevance(V):
    rel = []
    index = 0
    for i in V:
        rel.append(1/distOfVid(index, V))
        index += 1
    return rel
#print(relevance(itemIDs))

'''
sort videos in terms of relevance
descending order
for ascending order take out reverse parameter
'''
def sortRel(V):
    return sorted(range(len(relevance(V))), key=relevance(V).__getitem__, reverse=True)
#print(sortRel(itemIDs))
'''
find which videos user has not seen?
'''


def top3(V, U):
    sortedRel = sortRel(V)
    index = 0
    
    recommend = []
    for word in U[index]:
        vids = findVids(word, V)
    for i in sortedRel:
        for k in V[i]:
            for relK in vids:
                if relK is k:
                    recommend.append(i)
    print(recommend)
    print("Top three relevant videos for user 1 are: " + str(sortedRel[0]) + ", " + str(sortedRel[1]) + ", and " + str(sortedRel[2]))

top3(itemIDs, userIDs)

