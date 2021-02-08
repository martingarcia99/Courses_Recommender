import gensim
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import pandas as pd 
import os, sys
import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')

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
    # __documents = __data['combined'].values
    # #docs = [TaggedDocument(doc, [i]) for i, doc in enumerate(documents, start=2)]
    # __docs = [TaggedDocument(doc, [i]) for i, doc in enumerate(__documents)]


    def recommend(self, interests, language, study_program, topn=5):
        recommendations = []

        # print(self.__data.shape)

        count = 0
        for y in self.__data['study_courses']:
            if study_program not in y:
                self.__data = self.__data.drop(count)
            count+=1

        print(self.__data.shape)
        # print(self.__data.shape)
        # print(self.__data['language'])

        data = self.__data[self.__data['language'] == language]
        
        # print(data.shape)
        # print(data)

        print(data.shape)

        __documents = data['combined'].values
        #docs = [TaggedDocument(doc, [i]) for i, doc in enumerate(documents, start=2)]
        __docs = [TaggedDocument(doc, [i]) for i, doc in enumerate(__documents)]

        count = 0
        vec = {}
        for c in data.index:
            vec[count] = c
            count+=1

        modelDoc= gensim.models.Doc2Vec(__docs, vector_size=150, window=15, min_count=2, workers=4, epochs=40)
        new_vec = modelDoc.infer_vector(interests)
        similar_doc = modelDoc.docvecs.most_similar([new_vec], topn=topn)
        print(similar_doc)
        for row,index in similar_doc:
            pos = vec[row]
            print(str(pos) +'-'+ str(index))
            print(data['name'][pos]+ ' - Similarity= ' + str(index))
            
            recommendations.append((data['name'][pos], index))
        return recommendations
        #print(len(model.wv.vocab))
