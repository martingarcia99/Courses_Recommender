from flask import Flask, render_template, request
import pymongo
from pymongo import MongoClient
import json
from bson import json_util
from flask_pymongo import PyMongo
import numpy as np
from dotenv import load_dotenv
import os
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.embed import components
from bokeh.layouts import gridplot
from bokeh.resources import CDN
from bokeh.models import FactorRange, OpenURL, TapTool
import re
from data.machine_learning.recommandation.content_based.gensim_d2v import GensimD2VRecommender
from data.bokeh.recommendation_graph import RecommendationGraph
from db import MyDatabase

load_dotenv()

# DATABASE_NAME = os.getenv("DATABASE_NAME")
# DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
PASSWORD = os.environ.get("PASSWORD")

app=Flask(__name__)



##########################################################   DATABASE CONNECTION  #######################################################################################

# client = MongoClient("mongodb+srv://martin:{}@cluster0.ehkpp.mongodb.net/{}?retryWrites=true&w=majority".format(DATABASE_PASSWORD,DATABASE_NAME))
# client = MongoClient(MONGO_URL)
# db = client.get_database(DATABASE_NAME)
# users = db.user_profiles
# lectures = db.lecture_profiles

database = MyDatabase()
lectures = database.lectures

##########################################################   List of all the study courses  #######################################################################################
final_lectures = list()
for lecture in lectures.find():
    final_lectures.extend([element for element in lecture['study_courses'] if element not in final_lectures])

##########################################################   ROOTS   ############################################################################################
#variable to define if the password was written or not
global ps

@app.route("/", methods=['GET', 'POST'])
def home():
    global ps 
    ps = False
    if request.method == "GET":
        return render_template("index.html")

@app.route("/app", methods=['GET', 'POST'])
def perfil():
    if request.method == "GET":
        if ps == True:
            return render_template("app.html",lectures=final_lectures)
        else:
            return render_template("signin.html")

    
@app.route("/signin", methods=['GET', 'POST'])
def singin():
    if request.method == "GET":
        return render_template("signin.html")

@app.route("/success_login", methods=['GET','POST'])
def login():
    if request.method == "POST":
        if request.form['password'] == PASSWORD:
            global ps 
            ps = True
            return render_template("app.html", lectures=final_lectures)
        else:
            return render_template("signin.html",login="false",ps=PASSWORD, password=request.form['password'])

#array of interests that the user writes on the formn
global interests 
interests = list()

@app.route("/success_user", methods=['POST'])
def add_data():
    recommendations = []
    if request.method == "POST":
        language = request.form['language']
        study_program = request.form['study_program']
        recommender = GensimD2VRecommender()
        recommendations= recommender.recommend(interests, language, study_program)

        if recommendations != "No Results for this Search":
            graph = RecommendationGraph()
            script, div, cdn_css, cdn_js = graph.createRecommendationGraph(recommendations)
            return render_template("app.html",lectures=final_lectures, interests=interests, graph=True, animation = "off",script=script,div=div,cdn_js = cdn_js,cdn_css = cdn_css) 
        else:
            return render_template("app.html",lectures=final_lectures, interests=interests, graph=True, animation = "off",string=recommendations, alert=True) 


@app.route("/add_interest", methods=['GET','POST'])
def add_interest():
    if request.method == "POST":
        data = request.form['interest']
        interests.append(data)
    return render_template("app.html", interests=interests, lectures=final_lectures, animation="off")

@app.route("/delete_interest", methods=['GET','POST'])
def delete_interests():
    interests.clear()
    return render_template("app.html", interests=interests, lectures=final_lectures, animation="off")

        
@app.route("/course/<course>", methods=['GET','POST'])
def info_course(course):
    if request.method == "GET":
        print(course)
        lecture = lectures.find({"name": course})
        for l in lecture:
            name = l['name']
            description = l['description']
            description = description.replace("span","p")
            description = description.replace("white","none")
            language = l['language']
            professor = l['assigned_people']
            targets = l['learning_targets']
            targets = targets.replace("span","p")
            # targets = re.sub("<.*?>", "", targets)
            course_format = l['course_format']
            comments = l['comments']
            semester = l['semester'] if l['semester'] != None else ''
            rating = l['avg_rating'] if l['avg_rating'] != None else  ''
            graph = RecommendationGraph()
            if rating != None and semester != None:
                script, div, cdn_css, cdn_js = graph.createAverageRatingGraph(rating, semester)
                return render_template("course.html", script=script,div=div,cdn_js = cdn_js,cdn_css = cdn_css, name=name,desc=description,prof=professor,targets=targets,
                                cf=course_format,comments=comments,language=language)
            

@app.route("/aboutus", methods=['GET','POST'])
def info_us():
    if request.method == "GET":
        return render_template("aboutus.html")


if __name__ == "__main__":
    app.run(debug=True)