# from flask import Flask, render_template, request, make_response
# import json
# from time import time

# app=Flask(__name__)

# global dataList
# dataList = []


# @app.route("/", methods=['GET', 'POST'])
# def home():
#     if request.method == "GET":
#         return render_template("app.html")        

# @app.route("/data", methods=['GET', 'POST'])
# def datas():
#     if request.method == "GET":
#         if len(dataList) > 0:
#             print(len(dataList))
#             response = make_response(json.dumps(dataList.pop(0)))
#             response.content_type = 'application/json'
#             return response
#         else: return make_response()
#     else:
#         print(request.json)
#         data = {
#             'time' : time() * 1000,
#             'beat' : request.json['temperature'],
#         }
#         dataList.append(data)
#         print(dataList)
#         return make_response("ACK")

from flask import Flask, render_template, request
import pymongo
from pymongo import MongoClient
import json
from bson import json_util

app=Flask(__name__)

client = MongoClient('mongodb+srv://martin:xu6wqoAm@cluster0.ehkpp.mongodb.net/courses?retryWrites=true&w=majority')
db = client.courses
collection = db.subjects

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "GET":
        return render_template("app.html") 

@app.route("/success_user", methods=['POST'])
def show_data():
    if request.method == "POST":
        

@app.route("/users", methods=['POST'])
def create_user():

    course = {"name":"Learning Analytics", "description":"ahksjdlfhaklsjdhfklsadhfksladf"}
    dbResponse = collection.insert_one(course)
    for attr in dir(dbResponse):
        print(attr)

@app.route("/show", methods=['GET'])
def get_course():
    all_courses = list(collection.find({}))
    return json.dumps(all_courses, default=json_util.default)


if __name__ == "__main__":
    app.run(debug=True)