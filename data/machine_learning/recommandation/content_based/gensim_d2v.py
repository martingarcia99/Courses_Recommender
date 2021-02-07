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
    #print(__docs)

    #for x in __data.study_courses:
        #data = __data['B.Sc. Applied Cognitive and Media Science, PO14 - B-KM-14' in x]
    #print(__data.study_courses)
    #print(self.__data['study_courses'])


    print(__data.shape)

    count = 0
    for y in __data['study_courses']:
        __data.drop(2)
        'B.Sc. Applied Cognitive and Media Science, PO19 - B-KM-19' not in y:
            print(count)
            if  __data.drop(__data.index[[count,count+1]])
        count+=1
    print(__data.shape)

    def recommend(self, interests, language, study_program, topn=5):
        recommendations = []
        print(self.__data['language'])
        print(self.__data['study_courses'])
        print(data.shape)

        count = 0
        for y in data['study_courses']:
            if study_program not in y:
                data.drop([count])
            count+=1
        print(data.shape)

        data = self.__data[self.__data['language'] == language]
        
        print(data.shape)

        modelDoc= gensim.models.Doc2Vec(self.__docs, vector_size=150, window=15, min_count=2, workers=4, epochs=40)
        new_vec = modelDoc.infer_vector(interests)
        #print(new_vec)
        similar_doc = modelDoc.docvecs.most_similar([new_vec], topn=topn)
        #print(similar_doc)
        for row,index in similar_doc:
            print(str(row) +'-'+ str(index))
            #print(data['name'][row]+ ' - Similarity= ' + str(index))
            
            recommendations.append((data['name'][row], index))
        return recommendations
        #print(len(model.wv.vocab))
