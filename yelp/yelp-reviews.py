import os
import time
import json

from pymongo import MongoClient

from settings import Settings


dataset_file = Settings.DATASET_FILE
reviews_collection = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.REVIEWS_DATABASE][
    Settings.REVIEWS_COLLECTION]

count = 0
done = 0
start = time.time()

with open(dataset_file) as dataset:
    count = sum(1 for line in dataset)

with open(dataset_file) as dataset:
    next(dataset)
    for line in dataset:
        try:
            data = json.loads(line)
        except ValueError:
            print 'Oops!'
        if data["type"] == "review":
            reviews_collection.insert({
                "reviewId": data["review_id"],
                "business": data["business_id"],
                "text": data["text"]
            })

        done += 1
        if done % 100 == 0:
            end = time.time()
            os.system('cls')
            print 'Done ' + str(done) + ' out of ' + str(count) + ' in ' + str((end - start))
