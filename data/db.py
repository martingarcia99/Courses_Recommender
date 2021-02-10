import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
import os
# from boto.s3.connection import S3Connection

# MONGO_URL = S3Connection(os.environ['MONGODB_URI'])
MONGO_URL = os.environ.get('MONGODB_URI')
load_dotenv()
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

# DATABASE_NAME = os.environ.get("DATABASE_NAME")

class MyDatabase:
    # __client = MongoClient(MONGO_URL)
    __client = MongoClient("mongodb+srv://martin:{}@cluster0.ehkpp.mongodb.net/{}?retryWrites=true&w=majority".format(DATABASE_PASSWORD,DATABASE_NAME))

    #client = MongoClient()
    __db = __client.get_database(DATABASE_NAME)

    lectures = __db.lecture_profiles
    #lectures.remove( { } )
    lectures.create_index([('lecture_id', pymongo.ASCENDING)], unique=True)
