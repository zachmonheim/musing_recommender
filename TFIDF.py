'''
TF-IDF to determine inverse frequency of keywords of items and users
Created on May 29, 2019

@author: Zach Monheim
'''

import random

from sklearn.feature_extraction.text import TfidfVectorizer

#create list of 1000 keywords
keywords = []
keys = 0
while (keys < 1000):
    keywords.append(keys)
    keys += 1

#create a dataset with 1000 user IDs and assign a list of random keyword IDs based on a list of keywords
userIDs = []

for i in range(1,1001):
    userAmount = random.randint(1, 15)
    x = random.sample(keywords, userAmount)
    userIDs.append(x)


#create a dataset with 1000 item IDs and assign a list of random keyword IDs based on a list of keywords
itemIDs = []

for i in range(1,1001):
    itemAmount = random.randint(1, 15)
    x = random.sample(keywords, itemAmount)
    itemIDs.append(x)
    
print(userIDs)
print(itemIDs)

tfidf = TfidfVectorizer(preprocessor=lambda x: x, tokenizer=lambda x: x)
userResponse = tfidf.fit_transform(userIDs)
itemResponse = tfidf.fit_transform(itemIDs)
print(userResponse)
print(itemResponse)
