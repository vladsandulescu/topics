import os
import time

from pymongo import MongoClient
import nltk


connectionString = "mongodb://localhost:27030/"
dbYelp = MongoClient(connectionString).Yelp
dbTags = MongoClient(connectionString).Tags

businesses_cursor = dbYelp.RestaurantsNY.find()
businessesCount = businesses_cursor.count()
businesses_cursor.batch_size(5000)

stopwords = {}
with open('stopwords.txt', 'rU') as f:
    for line in f:
        stopwords[line.strip()] = 1

done = 0
start = time.time()

for business in businesses_cursor:
    for review in business["activeReviews"]:
        sentences = nltk.sent_tokenize(review["text"].lower())
        words = []
        for sentence in sentences:
            tokens = nltk.word_tokenize(sentence)
            text = [word for word in tokens if word not in stopwords]
            tagged_text = nltk.pos_tag(text)

            for word, tag in tagged_text:
                words.append({"Word": word, "Pos": tag})

        dbTags.Reviews.insert({
            "Business": business["name"],
            "Text": review["text"],
            "Words": words
        })

    done += 1
    if done % 100 == 0:
        end = time.time()
        os.system('cls')
        print 'Done ' + str(done) + ' out of ' + str(businessesCount) + ' in ' + str((end - start))