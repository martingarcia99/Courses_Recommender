import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

class MyDatabase:
    __client = MongoClient("mongodb+srv://martin:{}@cluster0.ehkpp.mongodb.net/{}?retryWrites=true&w=majority".format(DATABASE_PASSWORD,DATABASE_NAME))

    #client = MongoClient()
    __db = __client.get_database(DATABASE_NAME)

    lectures = __db.lecture_profiles
    #lectures.remove( { } )
    lectures.create_index([('lecture_id', pymongo.ASCENDING)], unique=True)
