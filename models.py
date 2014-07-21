import logging

from gensim.corpora import BleiCorpus
from gensim.models import LdaModel
from gensim import corpora, models
from pymongo import MongoClient


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

dbTags = MongoClient("mongodb://localhost:27030/").Tags
reviews_cursor = dbTags.Corpus.find()
dictionary_path = "models/dictionary.dict"
corpus_path_mm = "models/corpus.lda-c"
lda_model_10 = "models/lda_model_10_topics.lda"
lda_model_30 = "models/lda_model_30_topics.lda"
lda_model_50 = "models/lda_model_50_topics.lda"
lda_model_70 = "models/lda_model_70_topics.lda"
lda_model_100 = "models/lda_model_100_topics.lda"

dictionary = corpora.Dictionary(review["Words"].split() for review in reviews_cursor)
# remove_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq < 11 or docfreq > 1000]
dictionary.filter_extremes(keep_n=10000)
dictionary.compactify()
corpora.Dictionary.save(dictionary, dictionary_path)

#dictionary = corpora.Dictionary.load(dictionary_path)


class Corpus(object):
    def __init__(self, reviews_dictionary):
        self.cursor = dbTags.Corpus.find()
        self.reviews_dictionary = reviews_dictionary

    def __iter__(self):
        for review in self.cursor:
            yield self.reviews_dictionary.doc2bow(review["Words"].split())


corpus = Corpus(dictionary)
tfidf = models.TfidfModel(corpus)
corpus = tfidf[corpus]

BleiCorpus.serialize(corpus_path_mm, corpus, id2word=dictionary)

lda = LdaModel(corpus, num_topics=10, id2word=dictionary)
lda.save(lda_model_10)

lda = models.ldamodel.LdaModel(corpus, num_topics=30, id2word=dictionary)
lda.save(lda_model_30)

lda = models.ldamodel.LdaModel(corpus, num_topics=50, id2word=dictionary)
lda.save(lda_model_50)

lda = models.ldamodel.LdaModel(corpus, num_topics=70, id2word=dictionary)
lda.save(lda_model_70)

lda = models.ldamodel.LdaModel(corpus, num_topics=100, id2word=dictionary)
lda.save(lda_model_100)