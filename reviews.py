import os
import time

from pymongo import MongoClient
import nltk

from settings import Settings


reviews_collection = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.REVIEWS_DATABASE][
    Settings.REVIEWS_COLLECTION]
tags_collection = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.TAGS_DATABASE][Settings.REVIEWS_COLLECTION]

reviews_cursor = reviews_collection.find()
reviewsCount = reviews_cursor.count()
reviews_cursor.batch_size(1000)

stopwords = {}
with open('stopwords.txt', 'rU') as f:
    for line in f:
        stopwords[line.strip()] = 1

done = 0
start = time.time()

for review in reviews_cursor:
    words = []
    sentences = nltk.sent_tokenize(review["text"].lower())

    for sentence in sentences:
        tokens = nltk.word_tokenize(sentence)
        text = [word for word in tokens if word not in stopwords]
        tagged_text = nltk.pos_tag(text)

        for word, tag in tagged_text:
            words.append({"word": word, "pos": tag})

    tags_collection.insert({
        "reviewId": review["reviewId"],
        "business": review["business"],
        "text": review["text"],
        "words": words
    })

    done += 1
    if done % 100 == 0:
        end = time.time()
        os.system('cls')
        print 'Done ' + str(done) + ' out of ' + str(reviewsCount) + ' in ' + str((end - start))