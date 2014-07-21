import logging

from gensim.models import LdaModel
from gensim import corpora


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

dictionary_path = "models/dictionary.dict"
corpus_path_mm = "models/corpus.lda-c"
lda_model_10 = "models/lda_model_10_topics.lda"
lda_model_30 = "models/lda_model_30_topics.lda"
lda_model_50 = "models/lda_model_50_topics.lda"
lda_model_70 = "models/lda_model_70_topics.lda"
lda_model_100 = "models/lda_model_100_topics.lda"

dictionary = corpora.Dictionary.load(dictionary_path)
corpus = corpora.BleiCorpus(corpus_path_mm)

lda = LdaModel.load(lda_model_30)
for i in lda.show_topics(topics=30, topn=10):
    print i