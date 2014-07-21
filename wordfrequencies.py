import os
import time

from pymongo import MongoClient


dbTags = MongoClient("mongodb://localhost:27030/").Tags
reviews_cursor = dbTags.Reviews.find()
reviewsCount = reviews_cursor.count()
done = 0
reviews_cursor.batch_size(5000)
start = time.time()
for review in reviews_cursor:
    words = [word["Word"] for word in review["Words"] if word["Pos"] in ["NN", "NNS"]]
    for word in words:
        found = dbTags.WordFrequencies.find_one({"Word": word})
        if found is None:
            count = dbTags.Reviews.find({"Words.Word": word}).count()
            dbTags.WordFrequencies.insert({
                "Word": word,
                "Count": count
            })
    done += 1
    if done % 100 == 0:
        end = time.time()
        os.system('cls')
        print 'Done (' + str(done * 100 / reviewsCount) + ' %) - ' + str(done) + ' out of ' + str(
            reviewsCount) + ' in ' + str((end - start))