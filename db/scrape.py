import requests
import datetime
from bs4 import BeautifulSoup
import json
import re
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")




client = pymongo.MongoClient('mongodb+srv://mvpp:${DATABASE_PASSWORD}@lectures.b4cq3.mongodb.net/${DATABASE_NAME}?retryWrites=true&w=majority')

#client = MongoClient()
db = client.test_database

lectures = db.lectures


urls = ['https://www.uni-due.de/vdb/en_EN/pruefung/1245/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/1245/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/745/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/226/detail', 
        'https://www.uni-due.de/vdb/en_EN/pruefung/1053/detail', 
        'https://www.uni-due.de/vdb/en_EN/pruefung/1241/detail', 
        'https://www.uni-due.de/vdb/en_EN/pruefung/749/detail', 
        'https://www.uni-due.de/vdb/en_EN/pruefung/93/detail', 
        'https://www.uni-due.de/vdb/en_EN/pruefung/101/detail', 
        'https://www.uni-due.de/vdb/en_EN/pruefung/728/detail', 
        'https://www.uni-due.de/vdb/en_EN/pruefung/721/detail', 
        'https://www.uni-due.de/vdb/en_EN/pruefung/305/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/48/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/70/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/48/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/740/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/65/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/74/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/63/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/71/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/729/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/41/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/89/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/603/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/727/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/90/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/63/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/39/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/720/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/75/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/44/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/800/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/601/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/723/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/722/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/79/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/45/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/587/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/596/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/68/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/582/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/73/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/83/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/69/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/735/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/80/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/591/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/67/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/49/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/746/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/728/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/227/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/713/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/43/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/748/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/47/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/40/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/730/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/82/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/737/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/1095/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/1093/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/1091/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/2011/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/120/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/1093/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/1089/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/2007/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/94/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/95/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/1071/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/96/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/91/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/109/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/1067/detail']
 
with requests.Session() as sesh:
    def get_elements(list):
        strings = []
        for element in list:
            strings.append(element.string)
        return strings

    for url in urls:
        response = sesh.get(url)
        html = response.text
        print(response.status_code)

        soup = BeautifulSoup(html, features="lxml")   
        lectureName = soup.select_one('#masttitle').span.extract().get_text() if soup.select_one('#masttitle').span != None else soup.select_one('#masttitle').get_text()
        assigned_people = get_elements(soup.select_one('fieldset.highlight-blue:nth-child(8) > ul:nth-child(2)').find_all('a') if soup.select_one('fieldset.highlight-blue:nth-child(8) > ul:nth-child(2)') != None else [])
        study_courses = get_elements(soup.select_one('fieldset.highlight-blue:nth-child(7) > ul:nth-child(2)').find_all('a') if soup.select_one('fieldset.highlight-blue:nth-child(7) > ul:nth-child(2)') != None else []) 
        language = soup.select_one('fieldset.highlight-blue > table > tr:nth-child(3) > td:nth-child(2)').string if soup.select_one('fieldset.highlight-blue > table > tr:nth-child(3) > td:nth-child(2)') != None else ""
        description = soup.select_one('#en_EN > table > tr > td:nth-child(2)') or ""
        learning_targets = soup.select_one('#en_EN > table > tr:nth-child(2) > td:nth-child(2)') or ""
        pre_qualifications = soup.select_one('#en_EN > table > tr:nth-child(4) > td:nth-child(2)').get_text() if soup.select_one('#en_EN > table > tr:nth-child(4) > td:nth-child(2)') != None else ""
        course_format = soup.select_one ('fieldset.highlight-blue > table > tr:nth-child(2) > td:nth-child(2) > p').get_text() if soup.select_one ('fieldset.highlight-blue > table > tr:nth-child(2) > td:nth-child(2) > p') != None else ""
        
        print(lectureName)
        
        lecture = {
            'name': lectureName,
            'description': str(description),
            'assigned_people': assigned_people,
            'language': language,
            'learning_targets': str(learning_targets),
            'pre_qualifications': pre_qualifications,
            'course_format': course_format,
            'study_courses': study_courses,
            'date': datetime.datetime.utcnow()
        }

        lecture_id = lectures.insert_one(lecture).inserted_id


