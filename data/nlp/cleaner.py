import re
import nltk
import string
import pandas as pd
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pymongo import MongoClient
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer 
from nltk.tokenize import RegexpTokenizer 
from nltk.stem import WordNetLemmatizer 
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from db import MyDatabase

database = MyDatabase()
lectures = database.lectures

nltk.download('wordnet')
nltk.download('stopwords')

class DataCleaner:
    __ps = PorterStemmer() 
    __lemmatizer = WordNetLemmatizer() 
    __stop_words = set(stopwords.words('english')) 
    __tokenizer = RegexpTokenizer(r'\w+')
    __df = pd.DataFrame(list(lectures.find()))
    data = __df.drop(columns = ['_id', 'avg_rating', 'assigned_people', 'course_format', 'semester', 'comments'])
    
    def __remove_html(self, text):
        soup = BeautifulSoup(text, 'lxml')
        html_free = soup.get_text()
        return html_free

    def __remove_punctuation(self, text):
        no_punct = ''.join([c for c in text if c not in string.punctuation.replace('-','')])
        return no_punct

    def __remove_stop_word(self, text):
        no_stop_word = [c for c in text if c not in self.__stop_words]
        return no_stop_word

    def __word_lemmatizer(self, text):
        lem_text = [ self.__lemmatizer.lemmatize(i[0]) for i in text]
        return lem_text
    
    def __word_stemmer(self, text):
        stem_text = [self.__ps.stem(i[0]) for i in text]
        return stem_text

    def __clean(self, data):
        html_free_data = data.apply(lambda x: self.__remove_html(x))
        no_punct_data = html_free_data.apply(lambda x: self.__remove_punctuation(x))
        tokenized_data = no_punct_data.apply(lambda x: self.__tokenizer.tokenize(x.lower()))
        no_stop_word_data = tokenized_data.apply(lambda x: self.__remove_stop_word(x))         
        tagged_data = no_stop_word_data.apply(lambda x: nltk.pos_tag(x))
        lemmatized_data = tagged_data.apply(lambda x: ' '.join(self.__word_lemmatizer(x)))

        return lemmatized_data

    def cleaned_data(self):
        self.data['description'] = self.__clean(self.data['description'])
        self.data['learning_targets'] = self.__clean(self.data['learning_targets'])
        self.data['pre_qualifications'] = self.__clean(self.data['pre_qualifications'])
        self.data['combined'] = self.data['description'] + ' ' + self.data['learning_targets'] + ' ' + self.data['pre_qualifications']
        return self.data