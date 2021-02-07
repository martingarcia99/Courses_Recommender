import gensim
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import pandas as pd 
import os, sys
import nltk

content_based_ordner = os.path.dirname(os.path.realpath(__file__))
recommedation_ordner = os.path.dirname(content_based_ordner)
machine_learning_ordner = os.path.dirname(recommedation_ordner)
data_ordner = os.path.dirname(machine_learning_ordner)

sys.path.append(data_ordner)
from nlp.cleaner import DataCleaner



#print(data.head(0))
#print(combined)
class GensimD2VRecommender:

    __data_cleaner = DataCleaner()
    __data = __data_cleaner.cleaned_data()
    __data['combined'] = [nltk.word_tokenize(data_values) for data_values in __data['combined'].values]
    __documents = __data['combined'].values

    #docs = [TaggedDocument(doc, [i]) for i, doc in enumerate(documents, start=2)]
    __docs = [TaggedDocument(doc, [i]) for i, doc in enumerate(__documents)]
    #print(docs)


    words='IT engineer digital technology principles circuit design computer architecture basic programming and operating systems'.split()
    def recommend(self, interests, topn=5):
        modelDoc= gensim.models.Doc2Vec(self.__docs, vector_size=150, window=15, min_count=2, workers=4, epochs=40)
        new_vec = modelDoc.infer_vector(interests)
        #print(new_vec)
        similar_doc = modelDoc.docvecs.most_similar([new_vec], topn=topn)
        #print(similar_doc)
        for row,index in similar_doc:
            print(str(row) +'-'+ str(index))
            print(self.__data['name'][row]+ ' - Similarity= ' + str(index))
        #print(len(model.wv.vocab))


