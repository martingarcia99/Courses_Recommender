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

from flask import Flask
from flask_pymongo import PyMongo

app=Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/database"

# HELLO, I DID THIS PART

mongo = PyMongo(app)


if __name__ == "__main__":
    app.run(debug=True)