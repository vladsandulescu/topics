Topics
====
I played with extracting topics from short documents and tried it out on Yelp reviews. My code uses [gensim](http://radimrehurek.com/gensim/ "Gensim") and its [Online LDA](http://radimrehurek.com/gensim/tut2.html#id4 "Online LDA") implementation. It might be useful to read this[ paper](http://www.yelp.com/html/pdf/YelpDatasetChallengeWinner_ImprovingRestaurants.pdf) first, before checking out the source code.

Get the [Yelp academic dataset](http://www.yelp.com/dataset_challenge) and import the reviews from the json file into your local MongoDB by running the **yelp/yelp-reviews.py** file.

If you clone the repository, you will see 4 python files which make up the execution pipeline: reviews.py, corpus.py, train.py and predict.py. 

* **reviews.py** - loops through all the reviews in the initial dataset and for each review it: splits the review into sentences, removes stopwords, extracts parts-of-speech tags for all the remaining tokens, stores each review (reviewId, business name, review text and <word,pos tag> pairs vector) to a MongoDB collection
* **corpus.py** - loops through all the reviews from the MongoDB collection in the previous step, filters out all words which are not nouns, uses WordNetLemmatizer to lookup the lemma of each noun, stores each review together with nouns' lemmas to a new MongoDB collection
* **train.py** - feeds the reviews corpus created in the previous step to the gensim LDA model, keeping only the 10000 most frequent tokens and using 50 topics
* **predict.py** - loads the saved LDA model from the previous step and displays the extracted topics
* **stopwords.txt** - [stopwords list](http://www.lextek.com/manuals/onix/stopwords2.html) created by Gerard Salton and Chris Buckley for the experimental SMART information retrieval system at Cornell University
