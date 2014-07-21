import os
import time

from bson.objectid import ObjectId
from pymongo import MongoClient
from nltk.stem.wordnet import WordNetLemmatizer


dbTags = MongoClient("mongodb://localhost:27030/").Tags
reviews_cursor = dbTags.Reviews.find()
reviewsCount = reviews_cursor.count()
done = 0
reviews_cursor.batch_size(5000)
start = time.time()
lem = WordNetLemmatizer()
for review in reviews_cursor:
    nouns = []
    words = [word for word in review["Words"] if word["Pos"] in ["NN", "NNS"]]
    for word in words:
        nouns.append(lem.lemmatize(word["Word"]))
    result = " ".join(nouns)

    dbTags.Corpus.insert({
        "ReviewId": ObjectId(review["_id"]),
        "Words": result
    })
    done += 1
    if done % 100 == 0:
        end = time.time()
        os.system('cls')
        print 'Done ' + str(done) + ' out of ' + str(reviewsCount) + ' in ' + str((end - start))