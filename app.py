from flask import Flask, render_template, request
import pymongo
from pymongo import MongoClient
import json
from bson import json_util
from flask_pymongo import PyMongo
import numpy as np
import pandas as pd
from dotenv import load_dotenv
import os
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.embed import components
from bokeh.layouts import gridplot
from bokeh.resources import CDN
from bokeh.models import FactorRange, OpenURL, TapTool
import re

load_dotenv()

DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
PASSWORD = os.getenv("PASSWORD")

app=Flask(__name__)

##########################################################   DATABASE CONNECTION  #######################################################################################

client = MongoClient("mongodb+srv://martin:{}@cluster0.ehkpp.mongodb.net/{}?retryWrites=true&w=majority".format(DATABASE_PASSWORD,DATABASE_NAME))
db = client.get_database(DATABASE_NAME)
users = db.user_profiles
lectures = db.lecture_profiles

##########################################################   List of all the study courses  #######################################################################################
final_lectures = list()
for lecture in lectures.find():
    final_lectures.extend([element for element in lecture['study_courses'] if element not in final_lectures])


##########################################################     Bokeh Visualization Data 1  ############################################################################################
courses = ['Grundlagen der Sozialpsychologie', 'Learning Analytics', 'Cloud, Web and Mobile', 'Distributed Systems']
percentage = [50, 80, 40, 30]
    
source = ColumnDataSource(data=dict(courses=courses, percentage=percentage))

TOOLTIPS = [("percentage", "@percentage")]

# sorting the bars means sorting the range factors
sorted_courses = sorted(courses, key=lambda x: percentage[courses.index(x)])

p = figure(x_range=sorted_courses, plot_height=350, title="Courses %", tools="hover,pan,box_select,zoom_in,zoom_out,save,reset,tap", tooltips=TOOLTIPS) 

p.vbar(x='courses', top='percentage', width=0.5, source=source, color="rgb(52,101,164)")

url = "http://127.0.0.1:5000/course/@courses"

taptool = p.select(type=TapTool)
taptool.callback = OpenURL(url=url)

p.xgrid.grid_line_color = None
p.y_range.start = 0

script,div = components(p)
cdn_js = CDN.js_files[0]
cdn_css = CDN.css_files

##########################################################     Bokeh Visualization Data 2  ############################################################################################
semester = ["WS18/19", "SS19", "WS19/20", "SS20"]
#avg. of course rating
avg = [4.5, 6, 3, 2]

source = ColumnDataSource(data=dict(semester=semester, avg=avg))

TOOLTIPS = [("AverageRating", "@avg")]

p2 = figure(x_range=FactorRange(*semester), plot_height=250, tools="hover,pan,box_select,zoom_in,zoom_out,save,reset,tap", tooltips=TOOLTIPS)

p2.vbar(x=semester, top=avg, width=0.9, alpha=0.5, color="rgb(52,101,164)")

# p2.line(x=["WS18/19", "SS19", "WS19/20", "SS20"], y=[4.5, 6, 3, 2], color="red", line_width=2)

url = "https://trello.com/c/YcD1oQfR/36-bokeh-visualization-of-the-recommendation"
taptool = p2.select(type=TapTool)
taptool.callback = OpenURL(url=url)

p2.line(x='semester', y='avg', source=source, color="red", line_width=2)

p2.y_range.start = 0
p2.x_range.range_padding = 0.1
p2.xaxis.major_label_orientation = 1
p2.xgrid.grid_line_color = None

script2,div2 = components(p2)
cdn_js2 = CDN.js_files[0]
cdn_css2 = CDN.css_files


##########################################################   ROOTS   ############################################################################################
global ps

@app.route("/", methods=['GET', 'POST'])
def home():
    global ps 
    ps = False
    print(ps)
    if request.method == "GET":
        return render_template("index.html")

@app.route("/app", methods=['GET', 'POST'])
def perfil():
    print(ps)
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
            print(ps)
            return render_template("app.html", lectures=final_lectures)
        else:
            print("incorrect password")
            return render_template("signin.html",login="false")

global interests 
interests = list()

@app.route("/success_user", methods=['POST'])
def add_data():
    if request.method == "POST":
        degree = request.form['degree']
        language = request.form['language']
        sp = request.form['study_program']
        # users.insert({"semester":semester, "degree":degree, "language":language, "courses":courses, "study_program":sp, "interest":interests})
        interests.clear()
        return render_template("app.html",lectures=final_lectures, interests=interests, graph=True, animation = "off",script=script,div=div,cdn_js = cdn_js,cdn_css = cdn_css) 

@app.route("/add_interest", methods=['GET','POST'])
def add_interest():
    if request.method == "POST":
        data = request.form['interest']
        interests.append(data)
    return render_template("app.html", interests=interests, lectures=final_lectures, animation="off")

        
@app.route("/course/<course>", methods=['GET','POST'])
def info_course(course):
    print(course)
    lecture = lectures.find({"name": course})
    for l in lecture:
        name = l['name']
        description = l['description']
        description = re.sub("<.*?>", "", description)
        professor = l['assigned_people']
        targets = l['learning_targets']
        targets = re.sub("<.*?>", "", targets)
        course_format = l['course_format']
        # comments = l['comments']
        rating = l['avg_rating']
    if request.method == "GET":
        return render_template("course.html", script=script2,div=div2,cdn_js = cdn_js2,cdn_css = cdn_css2, name=name,desc=description,prof=professor,targets=targets,
                                cf=course_format,rating=rating)

@app.route("/aboutus", methods=['GET','POST'])
def info_us():
    if request.method == "GET":
        return render_template("aboutus.html")


if __name__ == "__main__":
    app.run(debug=True)