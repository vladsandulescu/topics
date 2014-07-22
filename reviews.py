import os
import time

from pymongo import MongoClient
import nltk


connection = "mongodb://localhost:27030/"
dbReviews = MongoClient(connection).Reviews
dbTags = MongoClient(connection).Tags

reviews_cursor = dbReviews.Reviews.find()
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

    dbTags.Reviews.insert({
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