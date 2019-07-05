'''
Using lightFM as a recommendation system

Created on Jun 13, 2019

@author: Zach Monheim
'''
'''
import numpy as np
#uses dataset of movielens
from lightfm.datasets import fetch_movielens
from lightfm import LightFM
from lightfm.evaluation import precision_at_k


''
data = fetch_movielens(min_rating=4.0)

print(repr(data['train']))
print(repr(data['test']))


#instantiate and train the model
model = LightFM(loss='warp')
model.fit(data['train'], epochs=30, num_threads=2)

#evaluate the trained model
test_precision = precision_at_k(model, data['test'], k=5).mean()
'''
'''
model = LightFM(loss = 'warp')

model.fit(data['train'], epochs=30, num_threads=2)

def sample_recommendation(model, data, user_ids):
    n_users, n_items = data['train'].shape
    for user_id in user_ids:
        known_positives = data['item_labels'][data['train'].tocsr()                                    
                          [user_id].indices]
        
        scores = model.predict(user_id, np.arange(n_items))

        top_items = data['item_labels'][np.argsort(-scores)]

        print("User %s" % user_id)
        print(" Known positives:")
        
        for x in known_positives[:3]:
            print(" %s" % x)
        
        print(" Recommended:")
        
        for x in top_items[:3]:
            print(" %s" % x)


sample_recommendation(model, data, [3, 25, 451])
''

from lightfm.datasets import fetch_stackexchange

data = fetch_stackexchange('crossvalidated',
                           test_set_fraction=0.1,
                           indicator_features=False,
                           tag_features=True)

train = data['train']
test = data['test']

# Set the number of threads; you can increase this
# ify you have more physical cores available.
NUM_THREADS = 2
NUM_COMPONENTS = 30
NUM_EPOCHS = 3
ITEM_ALPHA = 1e-6

# Let's fit a WARP model: these generally have the best performance.
model = LightFM(loss='warp',
                item_alpha=ITEM_ALPHA,
               no_components=NUM_COMPONENTS)

import time

# Run 3 epochs and time it.
model = model.fit(train, epochs=NUM_EPOCHS, num_threads=NUM_THREADS)
seconds=time.time()
print(seconds)

# Import the evaluation routines
from lightfm.evaluation import auc_score

# Compute and print the AUC score
train_auc = auc_score(model, train, num_threads=NUM_THREADS).mean()
print('Collaborative filtering train AUC: %s' % train_auc)\

# We pass in the train interactions to exclude them from predictions.
# This is to simulate a recommender system where we do not
# re-recommend things the user has already interacted with in the train
# set.
test_auc = auc_score(model, test, train_interactions=train, num_threads=NUM_THREADS).mean()
print('Collaborative filtering test AUC: %s' % test_auc)

# Set biases to zero
model.item_biases *= 0.0

test_auc = auc_score(model, test, train_interactions=train, num_threads=NUM_THREADS).mean()
print('Collaborative filtering test AUC: %s' % test_auc)



item_features = data['item_features']
tag_labels = data['item_feature_labels']

print('There are %s distinct tags, with values like %s.' % (item_features.shape[1], tag_labels[:3].tolist()))


# Define a new model instance
model = LightFM(loss='warp',
                item_alpha=ITEM_ALPHA,
                no_components=NUM_COMPONENTS)

# Fit the hybrid model. Note that this time, we pass
# in the item features matrix.
model = model.fit(train,
                item_features=item_features,
                epochs=NUM_EPOCHS,
                num_threads=NUM_THREADS)


# Don't forget the pass in the item features again!
train_auc = auc_score(model,
                      train,
                      item_features=item_features,
                      num_threads=NUM_THREADS).mean()
print('Hybrid training set AUC: %s' % train_auc)


test_auc = auc_score(model,
                    test,
                    train_interactions=train,
                    item_features=item_features,
                    num_threads=NUM_THREADS).mean()
print('Hybrid test set AUC: %s' % test_auc)


def get_similar_tags(model, tag_id):
    # Define similarity as the cosine of the angle
    # between the tag latent vectors
    
    # Normalize the vectors to unit length
    tag_embeddings = (model.item_embeddings.T
                      / np.linalg.norm(model.item_embeddings, axis=1)).T
    
    query_embedding = tag_embeddings[tag_id]
    similarity = np.dot(tag_embeddings, query_embedding)
    most_similar = np.argsort(-similarity)[1:4]
    
    return most_similar


for tag in (u'bayesian', u'regression', u'survival'):
    tag_id = tag_labels.tolist().index(tag)
    print('Most similar tags for %s: %s' % (tag_labels[tag_id],
                                            tag_labels[get_similar_tags(model, tag_id)]))



'''
'''
training the movielens example
''

import numpy as np

from lightfm.datasets import fetch_movielens

movielens = fetch_movielens()


for key, value in movielens.items():
    print(key, type(value), value.shape)

train = movielens['train']
test = movielens['test']


from lightfm import LightFM
from lightfm.evaluation import precision_at_k
from lightfm.evaluation import auc_score

model = LightFM(learning_rate=0.05, loss='bpr')
model.fit(train, epochs=10)

train_precision = precision_at_k(model, train, k=10).mean()
test_precision = precision_at_k(model, test, k=10).mean()

train_auc = auc_score(model, train).mean()
test_auc = auc_score(model, test).mean()

print('Precision: train %.2f, test %.2f.' % (train_precision, test_precision))
print('AUC: train %.2f, test %.2f.' % (train_auc, test_auc))

model = LightFM(learning_rate=0.05, loss='warp')

model.fit_partial(train, epochs=10)

train_precision = precision_at_k(model, train, k=10).mean()
test_precision = precision_at_k(model, test, k=10).mean()

train_auc = auc_score(model, train).mean()
test_auc = auc_score(model, test).mean()

print('Precision: train %.2f, test %.2f.' % (train_precision, test_precision))
print('AUC: train %.2f, test %.2f.' % (train_auc, test_auc))







''
building dataset using xml zipped file
currently works with goodbooks-10k example dataset

import os
import zipfile
import csv

import requests


def _download(url: str, dest_path: str):

    req = requests.get(url, stream=True)
    req.raise_for_status()

    with open(dest_path, "wb") as fd:
        for chunk in req.iter_content(chunk_size=2 ** 20):
            fd.write(chunk)


def get_data():

    ratings_url = ("http://www2.informatik.uni-freiburg.de/" "~cziegler/BX/BX-CSV-Dump.zip")

    if not os.path.exists("data"):
        os.makedirs("data")

        _download(ratings_url, "data/data.zip")

    with zipfile.ZipFile("data/data.zip") as archive:
        return (
            csv.DictReader(
                (x.decode("utf-8", "ignore") for x in archive.open("BX-Book-Ratings.csv")),
                delimiter=";",
            ),
            csv.DictReader(
                (x.decode("utf-8", "ignore") for x in archive.open("BX-Books.csv")), delimiter=";"
            ),
        )


def get_ratings():

    return get_data()[0]


def get_book_features():

    return get_data()[1]
'''



















'''
featList = ['user_keywords', 'video_keywords', 'score']
itemid = ['1', '2', '3', '4', '5', '6']
feattup = tuple([itemid, featList])

listTup = []
for itemID in xrange(1, numVideos):
        
        score = []
        scAppend = score.append
        
        secWatched = str(random.randint(20, 1800))
        shared = str(random.randint(0, 1))
        liked = str(random.randint(0, 1))
        scAppend(secWatched)
        scAppend(shared)
        scAppend(liked)
        tup = [str(itemID), score]
        #add tuple to overall list
        listTup.append(tuple(tup))

import lightfm
from lightfm.data import Dataset

#creates dataset with IDs for users and videos
#and includes the features(keywords) for each
##but how to incorperate scores?
keywordsDataset = Dataset(True, True)
keywordsDataset.fit(userids, videoids, userIDs, videoIDs)
#keywordsDataset.build_interactions(userids, videoids)

keywordsDataset.build_item_features(listTup)
keywordsDataset.build_user_features(videoids, videoIDs)


##will this keep the score connected to both IDs?
ratingsDataset = Dataset(True, True)
ratingsDataset.fit(userids, videoids, scoreTuple, scoreTuple)
ratingsDataset.build_interactions(userids, videoids)

ratingsDataset.build_item_features(userids, scoreTuple)
ratingsDataset.build_user_features(videoids, scoreTuple)


print(ratingsDataset)
''



'''

import os

import zipfile

import csv

import requests

import json

from itertools import islice

from lightfm import LightFM

from lightfm.data import Dataset

''
def _download(url: str, dest_path: str):
    req = requests.get(url, stream=True)
    req.raise_for_status()

    with open(dest_path, "wb") as fd:
        for chunk in req.iter_content(chunk_size=2 ** 20):
            fd.write(chunk)


def get_data():
    ratings_url = ("http://www2.informatik.uni-freiburg.de/" "~cziegler/BX/BX-CSV-Dump.zip")
    
    if not os.path.exists("data"):
        os.makedirs("data")
        _download(ratings_url, "data/data.zip")
    
    with zipfile.ZipFile("data/data.zip") as archive:
        return (
            csv.DictReader(
                (x.decode("utf-8", "ignore") for x in archive.open("BX-Book-Ratings.csv")),
                delimiter=";",
            ),
            csv.DictReader(
                (x.decode("utf-8", "ignore") for x in archive.open("BX-Books.csv")), delimiter=";"
            ),
        )

def get_ratings():
    return get_data()[0]


def get_book_features():
    return get_data()[1]

print(get_data()[0])
print(get_data()[1])

#The data consists of book ratings and book details:

ratings, book_features = get_data()

#Ratings look like this:

for line in islice(ratings, 2):

    print(json.dumps(line, indent=4))

#and book features look like this:

for line in islice(book_features, 1):

    print(json.dumps(line, indent=4))
    
## Building the ID mappings

#The first thing we need to do is to create a mapping between the user and item ids from our input data to indices that will be used internally by our model.

#We do this because LightFM works with user and item ids that are consecutive non-negative integers. The `Dataset` class allow us to create a mapping between the IDs we use in our systems and the consecutive indices preferred by the model.

#To do this, we create a dataset and call its `fit` method. The first argument is an iterable of all user ids in our data, and the second is an iterable of all item ids. In this case, we use generator expressions to lazily iterate over our data and yield user and item ids:

dataset = Dataset()
dataset.fit((x['User-ID'] for x in get_ratings()),
            (x['ISBN'] for x in get_ratings()))

#This call will assign an internal numerical id to every user and item id we pass in. These will be contiguous (from 0 to however many users and items we have), and will also determine the dimensions of the resulting LightFM model.

#We can check that the mappings have been created by querying the dataset on how many users and books it knows about:

num_users, num_items = dataset.interactions_shape()

print('Num users: {}, num_items {}.'.format(num_users, num_items))

#Note that if we don't have all user and items ids at once, we can repeatedly call `fit_partial` to supply additional ids. In this case, we will use this capability to add some item feature mappings:

dataset.fit_partial(items=(x['ISBN'] for x in get_book_features()),

                    item_features=(x['Book-Author'] for x in get_book_features()))


#This will create a feature for every unique author name in the dataset.

#(Note that we fit some more item ids: this is to make sure our mappings are complete even if there are items in the features dataset that are not in the interactions set.)

## Building the interactions matrix

#Having created the mapping, we build the interaction matrix:

(interactions, weights) = dataset.build_interactions(((x['User-ID'], x['ISBN'])

                                                      for x in get_ratings()))
print(repr(interactions))

#This is main input into a LightFM model: it encodes the interactions betwee users and items.

#Since we have item features, we can also create the item features matrix:
item_features = dataset.build_item_features(((x['ISBN'], [x['Book-Author']])

                                              for x in get_book_features()))
print(repr(item_features))

## Building a model

#This is all we need to build a LightFM model:


model = LightFM(loss='bpr')

model.fit(interactions, item_features=item_features)





















''



def get_own_data():
    
    with zipfile.ZipFile("archive.zip") as archive:
        return (
            csv.DictReader(
                (x.decode("utf-8", "ignore") for x in archive.open("dataScore.csv")),
                delimiter=";",
            ),
            csv.DictReader(
                (x.decode("utf-8", "ignore") for x in archive.open("dataUser.csv")), delimiter=";"
            ),
            csv.DictReader(
                (x.decode("utf-8", "ignore") for x in archive.open("dataVideo.csv")), delimiter=";"
            ),
        )


def get_score():
    return get_own_data()[0]

def get_user_keywords():
    return get_own_data()[1]

def get_video_keywords():
    return get_own_data()[2]

print(get_own_data()[0])

ownRatings, user_keywords, video_keywords = get_own_data()

## shows "user_id, video_id, score": "1, 2, 4"
## should be "user_id":"1",
#            "video_id":"2",
#            "score":"4"

for line in islice(ownRatings, 2):

    print(json.dumps(line, indent=4))

for line in islice(user_keywords, 1):

    print(json.dumps(line, indent=4))
    
for line in islice(video_keywords, 1):

    print(json.dumps(line, indent=4))
    
##don't know how to get the specific rows or columns
##change the data format again?
#separate file for creating this alternate dataset or within the same matdict save?
#possibly use the matdict save loaded dictionaries and matrices to create new dataset
ownDataset = Dataset()
ownDataset.fit((x['user_id'] for x in get_score()),
            (x['video_id'] for x in get_score()))


own_num_users, own_num_items = ownDataset.interactions_shape()

print('Num users: {}, num_items {}.'.format(own_num_users, own_num_items))

#Note that if we don't have all user and items ids at once, we can repeatedly call `fit_partial` to supply additional ids. In this case, we will use this capability to add some item feature mappings:

ownDataset.fit_partial(items=(x['user_id'] for x in get_user_keywords()),

                    item_features=(x['keyword1'] for x in get_user_keywords()))


ownDataset.fit_partial(items=(x['video_id'] for x in get_video_keywords()),

                    item_features=(x['keyword1'] for x in get_video_keywords()))

(own_interactions, own_weights) = ownDataset.build_interactions(((x['user_id'], x['score'])

                                                      for x in get_score()))

print(repr(own_interactions))

#This is main input into a LightFM model: it encodes the interactions between users and items.

#Since we have item features, we can also create the item features matrix:
item_features = ownDataset.build_item_features(((x['video_id'], [x['keyword1']])

                                              for x in get_video_keywords()))
print(repr(item_features))

## Building a model

#This is all we need to build a LightFM model:


model = LightFM(loss='bpr')

model.fit(own_interactions, item_features=item_features)

''
