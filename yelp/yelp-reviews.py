import os
import time
import json

from pymongo import MongoClient


dbReviews = MongoClient("mongodb://localhost:27030/").Reviews
dataset_file = 'dataset/yelp_phoenix_academic_dataset'

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
            dbReviews.Reviews.insert({
                "reviewId": data["review_id"],
                "business": data["business_id"],
                "text": data["text"]
            })

        done += 1
        if done % 100 == 0:
            end = time.time()
            os.system('cls')
            print 'Done ' + str(done) + ' out of ' + str(count) + ' in ' + str((end - start))
