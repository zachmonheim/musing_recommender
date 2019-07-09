'''
Using lightFM as a recommendation system

Created on Jun 13, 2019

@author: Zach Monheim
'''


import os

import zipfile

import csv

import requests

import json

from itertools import islice

from lightfm import LightFM

from lightfm.data import Dataset



#example of downloading files into LightFM dataset
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








#trying to put own csv files into lightFM dataset

def get_own_data():
    
    with zipfile.ZipFile("archive.zip") as archive:
        return (
            csv.DictReader(
                (x.decode("utf-8", "ignore") for x in archive.open("dataScore.csv")),
                delimiter=",",
            ),
            csv.DictReader(
                (x.decode("utf-8", "ignore") for x in archive.open("dataUser.csv")), 
                delimiter=","
            ),
            csv.DictReader(
                (x.decode("utf-8", "ignore") for x in archive.open("dataVideo.csv")), 
                delimiter=","
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

for line in islice(ownRatings, 2):

    print(json.dumps(line, indent=4))

for line in islice(user_keywords, 1):

    print(json.dumps(line, indent=4))
    
for line in islice(video_keywords, 1):

    print(json.dumps(line, indent=4))
    

ownDataset = Dataset()
ownDataset.fit((x['user_id'] for x in get_score()),
            (x['video_id'] for x in get_score()))


own_num_users, own_num_items = ownDataset.interactions_shape()

print('Num users: {}, num_items {}.'.format(own_num_users, own_num_items))

#Note that if we don't have all user and items ids at once, we can repeatedly call `fit_partial` to supply additional ids. In this case, we will use this capability to add some item feature mappings:

ownDataset.fit_partial(items=(x['user_id'] for x in get_user_keywords()),
                    item_features=(x['keywords'] for x in get_user_keywords()))


ownDataset.fit_partial(items=(x['video_id'] for x in get_video_keywords()),
                    item_features=(x['keywords'] for x in get_video_keywords()))

(own_interactions, own_weights) = ownDataset.build_interactions(((x['user_id'], x['score'])
                                                      for x in get_score()))

print(repr(own_interactions))

#This is main input into a LightFM model: it encodes the interactions between users and items.

#Since we have item features, we can also create the item features matrix:
item_features = ownDataset.build_item_features(((x['video_id'], [x['keywords']])
                                              for x in get_video_keywords()))

print(repr(item_features))

## Building a model

#This is all we need to build a LightFM model:

model = LightFM(loss='bpr')

model.fit(own_interactions, item_features=item_features)


