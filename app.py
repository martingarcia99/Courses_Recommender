from flask import Flask, render_template, request
import pymongo
from pymongo import MongoClient
import json
from bson import json_util
from flask_pymongo import PyMongo
import numpy as np
from dotenv import load_dotenv
import os
from urllib.parse import quote
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

def clean_lecture_name(lecture_name):

    cleaned_lecture_name = re.sub('[&,:]', '', lecture_name).replace('/', '').replace('  ', ' ').replace(' ', '_').replace('-', '_').lower()
    if cleaned_lecture_name.endswith('_'): cleaned_lecture_name = cleaned_lecture_name[:-1]
    return cleaned_lecture_name

lecture_mapping = {
    'learning_analytics': 'Learning Analytics_Chatti_Auswertung.pdf',
    'cloud_web_and_mobile': 'Cloud, Web Mobile_Weis_Auswertung.pdf',
    'distributed_systems': 'Distributed System_Weis_Auswertung.pdf',
    'advanced_web_technologies': 'Advanced Web Technologies_Chatti_Auswertung.pdf',
    'natural_language_based_human_computer_interaction': 'Natürlichsprachliche_Mensch_Computer_Interaktion.pdf',
    'grundlagen_der_sozialpsychologie':'grundlagen_der_sozialpsychologie.pdf',
    'grundlagen_der_medienpsychologie': 'grundlagen_der_medienpsychologie.pdf',
    'electronic_communities_and_social_networks': 'electronic_communities_and_social_networks.pdf',
    'scientific_visualization': 'scientific_visualization.pdf',
    'computer_graphics': 'computer_graphics.pdf',
    'advanced_image_synthesis': 'advanced_image_synthesis.pdf',
    'information_mining': 'information_mining.pdf',
    'information_engineering': 'information_engineering.pdf',
    'internet_search_engines': 'information_engineering.pdf',
    'real_time_systems': 'real_time_systems',
    'knowledge_based_systems': 'knowledge_based_systems.pdf',
    'interactive_systems': 'interactive_systems.pdf',
    'formal_aspects_of_software_security_and_cryptography': 'formal_aspects_of_software_security_and_cryptography.pdf',
    'modelling_of_concurrent_systems': 'modelling_of_concurrent_systems.pdf',
    'multimedia_systems': 'multimedia_systems.pdf',
    'general_psychology_perception_cognition_and_behavior': 'general_psychology_perception_cognition_and_behavior.pdf',
    'general_psychology_motivation_and_emotion': 'general_psychology_motivation_and_emotion.pdf',
    'empirische_aspekte_der_mensch_computer_interaktion': 'empirische_aspekte_der_mensch_computer_interaktion.pdf',
    'basics_in_psychology_of_teaching_and_learning': 'statistics_ii_inferential_statistics.pdf',
    'kommunikationspsychologische_vertiefung': 'kommunikationspsychologische_vertiefung.pdf',
    'peer_to_peer_systems': 'Peer-to-Peer Sytseme_Weis_Auswertung.pdf',
    'formal_specification_of_software_systems': 'Formale Spezifikation von Software-Systemen_Heisel_Auswertung.pdf',
    'embedded_systems': 'Embedded Systems_Schiele_Auswertung.pdf',
    'internet_technologie_and_web_engineering': 'Internet Technologie und Web Engineering_Weis_Auswertung.pdf',
    'computer_networks_and_communication_systems': 'Rechnernetze und Kommunikationssysteme_Otten_Auswertung.pdf',
    'recommender_systems': 'Recommender Systeme_ Ziegler_Auswertung.pdf',
    'security_in_communication_networks': 'Sicherheit und Kommunikationssysteme_Weis_Auswertung.pdf',
    'operating_systems': 'Betriebssysteme_Weis_Auswertung.pdf',
    'programming_in_c': 'Programmieren in C_Schiele_Auswertung.pdf',
    'internet_of_things_protocols_and_system_software': 'Internet of Things_Schiele_Auswertung.pdf',
    'modeling': 'Modellierung_Voigtländer_Auswertung.pdf',
    'einführung_in_die_logik': 'Einführung in die Logik_Hoppe_Auswertung.pdf',
    'compiler_construction': 'Compilerbau_Voigtländer_Auswertung.pdf',
    'mathematical_structures': 'Mathematische Strukturen_Voigtländer_Auswertung.pdf',
    'programming_paradigm': 'Programmierparadigmen_Voigtländer_Auswertung.pdf',
    'basic_programming_skills': 'Grundlegende Programmiertechniken_Krüger_Auswertung.pdf',
    'databases': 'Datenbanken_Fuhr_Auswertung.pdf',
    'data_structures_and_algorithms': 'DUA_Krüger_Auswertung.pdf',
    'information_retrieval': 'Information Retrieval_Fuhr_Auswertung.pdf',
    'advanced_programming_technologies': 'Fortgeschrittene Programmiertechniken_Pauli_Auswertung.pdf',
    'computer_robot_vision': 'Computer Robot Vision_Pauli_Auswertung.pdf',
    'cognitive_robot_systems': 'Cognitive Robot Systems_Pauli_Auswertung.pdf',
    'fundamentals_of_image_processing': 'Grundlagen der Bildverarbeitung_Pauli_Dovletov_Auswertung.pdf',
    'neurocomputing_and_organic_computing': 'Neuroinformatik und Organic Computing_Pauli_Pham_Auswertung.pdf',
    'language_technology': 'Sprachtechnologie_Zesch_Auswertung.pdf',
    'foundations_of_artificial_intelligence': 'Grundlagen künstlicher Intelligenz_ Zesch_Auswertung.pdf',
    'human_computer_interaction': 'Mensch-Computer-Interaktion_Ziegler_Auswertung.pdf',
    'interactive_systems': 'Interaktive Systeme_Ziegler_Auswertung.pdf',
    'electronic_business': 'E-Business_Ziegler_Gaulke_Auswertung.pdf',
    'software_engineering': 'Softwaretechnik_Heisel_Auswertung.pdf',
    'pattern_and_component_based_software_development': 'Muster- und komponentenbasierte Softwareentwicklung_Wirtz_Auswertung.pdf',
    'development_of_safe_and_secure_software': 'Entwicklung sicherer Software_Hatebur_Auswertung.pdf',
    'automata_and_formal_languages': 'Automaten und Formale Sprache_König_Auswertung.pdf',
    'computability_and_complexity': 'Berechenbarkeit und Komplexität_König_Auswertung.pdf',
    'logic': 'Logik_König_Auswertung.pdf',
    'modelling_analysis_verification': 'Modellierung, Analyse, Verifikation_König_Auswertung.pdf',
    'digital_games_research': 'Digitale Spiele_Masuch_Auswertung.pdf',
    'internet_research': 'Internet Research_Stieglitz_Auswertung.pdf',
    'business_communications': 'Business Communication_Stieglitz_Brachten_Auswertung.pdf',
    'digital_society': 'Digital Society_Marx_Stieglitz_Auswertung.pdf',
    'communication_and_collaboration_systems': 'Communication Collaboration Systems_Stieglitz_Fromm_Auswertung.pdf',
    'media_production': 'Medienproduktion_Stieglitz_Brachten_Auswertung.pdf',
    'digital_enterprise': 'Digital Enterprise_Stieglitz_Auswertung.pdf',
    'web_science': 'WebScience_Stieglitz_Auswertung.pdf',
    'statistics_i_introduction_to_research_methods': 'Statistik I Einführung in die Methodenlehre_Bodemer_Auswertung.pdf',
    'statistics_ii_inferential_statistics': 'Inferenzstatistik_Bodemer_Heimbuch_Auswertung.pdf',
    'digital_system_design': 'Digitaltechnische Grundlagen und Mikrocomputer_Schiele_Auswertung.pdf'
}

def get_file_mapping(lectureName):
    #print(lecture_mapping['lectureName'])
    return lecture_mapping[lectureName]

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
            cleaned_lecture_name = clean_lecture_name(name)
            pdf_name = get_file_mapping(cleaned_lecture_name)

            evaluation = 'https://moodle.uni-due.de/pluginfile.php/1622606/mod_folder/content/0/'+quote(pdf_name, safe='')+'?forcedownload=1' if semester == 'ws19-20' else 'https://moodle.uni-due.de/pluginfile.php/1423259/mod_folder/content/0/'+quote(pdf_name, safe='')+'?forcedownload=1' if semester == 'ss19' else ''
            print(evaluation)
            graph = RecommendationGraph()
            if rating != None and semester != None:
                script, div, cdn_css, cdn_js = graph.createAverageRatingGraph(rating, semester)
                return render_template("course.html", script=script,div=div,cdn_js = cdn_js,cdn_css = cdn_css, name=name,desc=description,prof=professor,targets=targets,
                                cf=course_format,comments=comments,language=language, evaluation=evaluation)
"""            
https://moodle.uni-due.de/pluginfile.php/1622606/mod_folder/content/0/Betriebssysteme_Weis_Auswertung.pdf?forcedownload=1
https://moodle.uni-due.de/pluginfile.php/1622606/mod_folder/content/0/Cloud%2C%20Web%20%20Mobile_Weis_Auswertung.pdf?forcedownload=1
https://moodle.uni-due.de/pluginfile.php/1622606/mod_folder/content/0/Cognitive%20Robot%20Systems_Pauli_Auswertung.pdf?forcedownload=1
https://moodle.uni-due.de/pluginfile.php/1622606/mod_folder/content/0/Learning%20Analytics_Chatti_Auswertung.pdf?forcedownload=1
https://moodle.uni-due.de/pluginfile.php/1423259/mod_folder/content/0/Advanced%20Web%20Technologies_Chatti_Auswertung.pdf?forcedownload=1
https://moodle.uni-due.de/pluginfile.php/1423259/mod_folder/content/0/E-Business_Ziegler_Gaulke_Auswertung.pdf?forcedownload=1
"""
@app.route("/aboutus", methods=['GET','POST'])
def info_us():
    if request.method == "GET":
        return render_template("aboutus.html")


if __name__ == "__main__":
    app.run(debug=True)