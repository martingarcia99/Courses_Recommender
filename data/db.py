import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
import os
# from boto.s3.connection import S3Connection

# MONGO_URL = S3Connection(os.environ['MONGODB_URI'])
MONGO_URL = os.environ.get('MONGODB_URI')
load_dotenv()

DATABASE_NAME = os.environ.get("DATABASE_NAME")

class MyDatabase:
    __client = MongoClient(MONGO_URL)

    #client = MongoClient()
    __db = __client.get_database(DATABASE_NAME)

    lectures = __db.lecture_profiles
    #lectures.remove( { } )
    lectures.create_index([('lecture_id', pymongo.ASCENDING)], unique=True)
