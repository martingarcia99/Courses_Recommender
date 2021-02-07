from gensim.models import Word2Vec, KeyedVectors
import pandas as pd 
import os, sys
import nltk

content_based_ordner = os.path.dirname(os.path.realpath(__file__))
recommedation_ordner = os.path.dirname(content_based_ordner)
machine_learning_ordner = os.path.dirname(recommedation_ordner)
data_ordner = os.path.dirname(machine_learning_ordner)

sys.path.append(data_ordner)
from nlp.cleaner import DataCleaner

data_cleaner = DataCleaner()
data = data_cleaner.cleaned_data()

#print(data.head(0))
combined = data['combined'].values
#print(combined)

combined_token = [nltk.word_tokenize(data_values) for data_values in combined]
#print(combined_token)

model = Word2Vec(combined_token, min_count=1, size=32)

print(model.most_similar('programming'))

#print(len(model.wv.vocab))

