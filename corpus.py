import os
import time

from pymongo import MongoClient
from nltk.stem.wordnet import WordNetLemmatizer


connection = "mongodb://localhost:27030/"
dbTags = MongoClient(connection).Tags

reviews_cursor = dbTags.Reviews.find()
reviewsCount = reviews_cursor.count()
reviews_cursor.batch_size(5000)

lem = WordNetLemmatizer()

done = 0
start = time.time()

for review in reviews_cursor:
    nouns = []
    words = [word for word in review["words"] if word["pos"] in ["NN", "NNS"]]

    for word in words:
        nouns.append(lem.lemmatize(word["word"]))

    dbTags.Corpus.insert({
        "reviewId": review["reviewId"],
        "business": review["business"],
        "text": review["text"],
        "words": nouns
    })

    done += 1
    if done % 100 == 0:
        end = time.time()
        os.system('cls')
        print 'Done ' + str(done) + ' out of ' + str(reviewsCount) + ' in ' + str((end - start))