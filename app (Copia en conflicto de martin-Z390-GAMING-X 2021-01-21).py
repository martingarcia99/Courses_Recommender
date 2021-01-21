# from flask import Flask, render_template, request, make_response
# import json
# from time import time

# app=Flask(__name__)

# dataList
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
from flask_pymongo import PyMongo
import numpy as np

app=Flask(__name__)

client = MongoClient("mongodb+srv://martin:xu6wqoAm@cluster0.ehkpp.mongodb.net/LA?retryWrites=true&w=majority")
db = client.get_database("LA")
user = db.profiles

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "GET":
        return render_template("index.html") 

@app.route("/app", methods=['GET', 'POST'])
def perfil():
    if request.method == "GET":
        return render_template("app.html")
    
    # if request.method == "POST":


@app.route("/success_user", methods=['POST'])
def add_data():
    if request.method == "POST":
        semester = request.form['semester']
        degree = request.form['degree']
        language = request.form['language']
        courses = request.form['courses']
        sp = request.form['study_program']
        interest = request.form['interest']
        print(semester)
        print(degree)
        print(language)
        print(courses)
        print(sp)
        print(interest)

        # user.insert({"semester":semester, "degree":degree, "language":language, "courses":courses, "study_program":sp, "interest":interest})
        return render_template("index.html") 

global courses,interest
courses = []

@app.route("/add_course", methods=['GET','POST'])
def add_course():
    if request.method == "POST":
        courses.append(request.form['courses'])
        for i in courses:
            print(i)
    return render_template("app.html")

@app.route("/add_interest", methods=['GET','POST'])
def add_interest():
    if request.method == "POST":
        courses.append(request.form['interest'])
        for i in courses:
            print(i)
    return render_template("app.html")

        

# @app.route("/users", methods=['POST'])
# def create_user():

    # user = {"semester":semester, "degree":degree, "language":language, "courses":courses, "study_program":sp, "interest":interes}
    # dbResponse = user.insert_one(course)
    # for attr in dir(dbResponse):
    #     print(attr)

@app.route("/show", methods=['GET'])
def get_course():
    all_courses = list(user.find({}))
    return json.dumps(all_courses, default=json_util.default)


if __name__ == "__main__":
    app.run(debug=True)