import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel 
import os, sys
content_based_ordner = os.path.dirname(os.path.realpath(__file__))
recommedation_ordner = os.path.dirname(content_based_ordner)
machine_learning_ordner = os.path.dirname(recommedation_ordner)
data_ordner = os.path.dirname(machine_learning_ordner)

sys.path.append(data_ordner)
from nlp.cleaner import DataCleaner

data_cleaner = DataCleaner()
data = data_cleaner.cleaned_data()
data.to_csv(r'data/data.csv', index = False)
#print (print(data.iloc[0]['combined']))
tfidf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0)
tfidf_matrix = tfidf.fit_transform(data['combined'])
#print(tfidf_matrix)
#print(len(tfidf.get_feature_names()))

#print(tfidf_matrix.shape)

cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix) 
results = {}
for idx, row in data.iterrows():
   similar_indices = cosine_similarities[idx].argsort()[:-100:-1] 
   similar_items = [(cosine_similarities[idx][i], data['lecture_id'][i]) for i in similar_indices] 
   results[row['lecture_id']] = similar_items[1:]

#print(results)

def item(id):  
    return data.loc[data['lecture_id'] == id]['name'].tolist()[0].split(' - ')[0] 

#Just reads the results out of the dictionary.

def recommend(item_id, num):
    print("Recommending " + str(num) + " products similar to " + item(item_id) + "...")   
    print("-------")    
    recs = results[item_id][:num]   
    for rec in recs: 
       print("Recommended: " + item(rec[1]) + " (score:" + str(rec[0]) + ")")

print(recommend(item_id=41, num=5))