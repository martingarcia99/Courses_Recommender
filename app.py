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
from bokeh.models import FactorRange

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

for user in users.find():
    print(user['interest'])

##########################################################   List of all the study courses  #######################################################################################
final_lectures = list()
for lecture in lectures.find():
    final_lectures.extend([element for element in lecture['study_courses'] if element not in final_lectures])


##########################################################     Bokeh Visualization Data 1  ############################################################################################
courses = ['Information Mining', 'Learning Analytics', 'Fortgeschrittene Programmiertechniken', 'Advanced Web Technologies']
percentage = [50, 80, 40, 30]
    
source = ColumnDataSource(data=dict(courses=courses, percentage=percentage))

TOOLTIPS = [("percentage", "@percentage")]

# sorting the bars means sorting the range factors
sorted_courses = sorted(courses, key=lambda x: percentage[courses.index(x)])

p = figure(x_range=sorted_courses, plot_height=350, title="Courses %", tools="hover,pan,box_select,zoom_in,zoom_out,save,reset", tooltips=TOOLTIPS) 

p.vbar(x='courses', top='percentage', width=0.5, source=source)

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

p2 = figure(x_range=FactorRange(*semester), plot_height=250, tools="hover,pan,box_select,zoom_in,zoom_out,save,reset", tooltips=TOOLTIPS)

p2.vbar(x=semester, top=avg, width=0.9, alpha=0.5)

p2.line(x=["WS18/19", "SS19", "WS19/20", "SS20"], y=[4.5, 6, 3, 2], color="red", line_width=2)

p2.y_range.start = 0
p2.x_range.range_padding = 0.1
p2.xaxis.major_label_orientation = 1
p2.xgrid.grid_line_color = None

script2,div2 = components(p2)
cdn_js2 = CDN.js_files[0]
cdn_css2 = CDN.css_files


##########################################################   ROOTS   ############################################################################################
@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "GET":
        return render_template("index.html")

@app.route("/app", methods=['GET', 'POST'])
def perfil():
    if request.method == "GET":
        return render_template("app.html",lectures=final_lectures)

    
@app.route("/signin", methods=['GET', 'POST'])
def singin():
    if request.method == "GET":
        return render_template("signin.html")

@app.route("/success_login", methods=['GET','POST'])
def login():
    if request.method == "POST":
        if request.form['password'] == PASSWORD:
            return render_template("app.html", lectures=final_lectures)
        else:
            print("incorrect password")
            return render_template("signin.html",login="false")


@app.route("/success_user", methods=['POST'])
def add_data():
    if request.method == "POST":
        semester = request.form['semester']
        degree = request.form['degree']
        language = request.form['language']
        sp = request.form['study_program']
        # users.insert({"semester":semester, "degree":degree, "language":language, "courses":courses, "study_program":sp, "interest":interests})
        courses.clear()
        interests.clear()
        return render_template("app.html",lectures=final_lectures,graph=True, animation = "off",script=script,div=div,cdn_js = cdn_js,cdn_css = cdn_css) 

global interests 
interests = list()

@app.route("/add_interest", methods=['GET','POST'])
def add_interest():
    if request.method == "POST":
        data = request.form['interest']
        interests.append(data)
    return render_template("app.html", interests=interests,courses=courses, lectures=final_lectures, animation="off")

        
@app.route("/course", methods=['GET','POST'])
def info_course():
    if request.method == "GET":
        return render_template("course.html", script=script2,div=div2,cdn_js = cdn_js2,cdn_css = cdn_css2)

@app.route("/aboutus", methods=['GET','POST'])
def info_us():
    if request.method == "GET":
        return render_template("aboutus.html")


if __name__ == "__main__":
    app.run(debug=True)