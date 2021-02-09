import requests
import datetime
from bs4 import BeautifulSoup
import json
import os
import re
from db import MyDatabase
from PyPDF2 import PdfFileWriter, PdfFileReader

database = MyDatabase()
lectures = database.lectures
lectures.remove( { } )
lecture_id = 1

urls = ['https://www.uni-due.de/vdb/en_EN/pruefung/1245/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/1245/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/745/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/226/detail', 
        'https://www.uni-due.de/vdb/en_EN/pruefung/1053/detail', 
        'https://www.uni-due.de/vdb/en_EN/pruefung/1241/detail', 
        'https://www.uni-due.de/vdb/en_EN/pruefung/749/detail', 
        'https://www.uni-due.de/vdb/en_EN/pruefung/93/detail', 
        'https://www.uni-due.de/vdb/en_EN/pruefung/101/detail', 
        'https://www.uni-due.de/vdb/en_EN/pruefung/728/detail', 
        'https://www.uni-due.de/vdb/en_EN/pruefung/305/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/70/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/48/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/740/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/65/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/74/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/71/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/729/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/41/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/89/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/603/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/727/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/90/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/63/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/39/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/720/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/75/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/44/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/800/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/601/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/723/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/722/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/79/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/45/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/587/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/596/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/68/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/582/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/73/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/83/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/69/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/735/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/80/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/591/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/67/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/49/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/746/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/227/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/713/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/43/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/748/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/47/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/40/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/730/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/82/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/737/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/1095/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/1093/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/1091/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/2011/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/120/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/1089/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/2007/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/94/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/95/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/1071/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/96/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/91/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/109/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/1067/detail',
        'https://www.uni-due.de/vdb/en_EN/pruefung/37/detail']
       
lecture_mapping = {
    'learning_analytics': 'Learning_Analytics.pdf',
    'cloud_web_and_mobile': 'Cloud_Web_Mobile.pdf',
    'distributed_systems': 'Distributed_Systems.pdf',
    'natural_language_based_human_computer_interaction': 'Natürlichsprachliche_Mensch_Computer_Interaktion.pdf',
    'advanced_web_technologies': 'Advanced_Web_Technologies.pdf',
    'peer_to_peer_systems': 'Peer_to_Peer_Systems.pdf',
    'grundlagen_der_sozialpsychologie':'grundlagen_der_sozialpsychologie.pdf',
    'grundlagen_der_medienpsychologie': 'grundlagen_der_medienpsychologie.pdf',
    'formal_specification_of_software_systems': 'Formale_Spezifikation_von_Software_Systemen.pdf',
    'electronic_communities_and_social_networks': 'electronic_communities_and_social_networks.pdf',
    'embedded_systems': 'Embedded_Systems.pdf',
    'internet_technologie_and_web_engineering': 'Internet_Technologie_und_Web_Engineering.pdf',
    'computer_networks_and_communication_systems': 'Rechnernetze_und_Kommunikationssysteme.pdf',
    'recommender_systems': 'Recommender_Systems.pdf',
    'security_in_communication_networks': 'Sicherheit_und_Kommunikationssysteme.pdf',
    'operating_systems': 'Betriebssysteme.pdf',
    'programming_in_c': 'Programmieren_in_C.pdf',
    'internet_of_things_protocols_and_system_software': 'Internet_of_Things.pdf',
    'modeling': 'Modellierung.pdf',
    'einführung_in_die_logik': 'Einführung_in_die_Logik.pdf',
    'scientific_visualization': 'scientific_visualization.pdf',
    'compiler_construction': 'Compilerbau.pdf',
    'mathematical_structures': 'Mathematische_Strukturen.pdf',
    'programming_paradigm': 'Programmierparadigmen.pdf',
    'basic_programming_skills': 'Grundlegende_Programmiertechniken.pdf',
    'computer_graphics': 'computer_graphics.pdf',
    'databases': 'Datenbanken.pdf',
    'data_structures_and_algorithms': 'data_structures_and_algorithms.pdf',
    'advanced_image_synthesis': 'advanced_image_synthesis.pdf',
    'information_mining': 'information_mining.pdf',
    'information_retrieval': 'Information_Retrieval.pdf',
    'information_engineering': 'information_engineering.pdf',
    'internet_search_engines': 'information_engineering.pdf',
    'advanced_programming_technologies': 'Fortgeschrittene_Programmiertechniken.pdf',
    'computer_robot_vision': 'Computer_Robot_Vision.pdf',
    'cognitive_robot_systems': 'Cognitive_Robot_Systems.pdf',
    'fundamentals_of_image_processing': 'Grundlagen_der_Bildverarbeitung.pdf',
    'neurocomputing_and_organic_computing': 'Neuroinformatik_und_Organic_Computing.pdf',
    'real_time_systems': 'real_time_systems',
    'language_technology': 'Sprachtechnologie.pdf',
    'foundations_of_artificial_intelligence': 'Grundlagen_künstlicher_Intelligenz.pdf',
    'knowledge_based_systems': 'knowledge_based_systems.pdf',
    'human_computer_interaction': 'Mensch-Computer-Interaktion.pdf',
    'interactive_systems': 'interactive_systems.pdf',
    'electronic_business': 'E-Business.pdf',
    'software_engineering': 'Softwaretechnik.pdf',
    'formal_aspects_of_software_security_and_cryptography': 'formal_aspects_of_software_security_and_cryptography.pdf',
    'pattern_and_component_based_software_development': 'Muster-_und_komponentenbasierte_Softwareentwicklung.pdf',
    'development_of_safe_and_secure_software': 'Entwicklung_sicherer_Software.pdf',
    'automata_and_formal_languages': 'Automaten_und_Formale_Sprache.pdf',
    'modelling_of_concurrent_systems': 'modelling_of_concurrent_systems.pdf',
    'computability_and_complexity': 'Berechenbarkeit_und_Komplexität.pdf',
    'logic': 'Logik.pdf',
    'modelling_analysis_verification': 'Modellierung_Analyse_Verifikation.pdf',
    'multimedia_systems': 'multimedia_systems.pdf',
    'digital_games_research': 'Digitale_Spiele.pdf',
    'internet_research': 'Internet_Research.pdf',
    'business_communications': 'Business_Communication.pdf',
    'digital_society': 'Digital_Society.pdf',
    'communication_and_collaboration_systems': 'Communication_Collaboration_Systems.pdf',
    'media_production': 'Medienproduktion.pdf',
    'digital_enterprise': 'Digital_Enterprise.pdf',
    'web_science': 'WebScience.pdf',
    'general_psychology_perception_cognition_and_behavior': 'general_psychology_perception_cognition_and_behavior.pdf',
    'general_psychology_motivation_and_emotion': 'general_psychology_motivation_and_emotion.pdf',
    'empirische_aspekte_der_mensch_computer_interaktion': 'empirische_aspekte_der_mensch_computer_interaktion.pdf',
    'statistics_i_introduction_to_research_methods': 'Statistik_I_Einführung_in_die_Methodenlehre.pdf',
    'statistics_ii_inferential_statistics': 'Inferenzstatistik.pdf',
    'basics_in_psychology_of_teaching_and_learning': 'statistics_ii_inferential_statistics.pdf',
    'kommunikationspsychologische_vertiefung': 'kommunikationspsychologische_vertiefung.pdf',
    'digital_system_design': 'Digitaltechnische_Grundlagen_und_Mikrocomputer.pdf'
}

def get_path(directory, lectureName):
    #print(directory)
    for path in os.listdir(directory):
        full_path = os.path.join(directory, get_file_mapping(lectureName))
        if os.path.isfile(full_path):
            #print ('true '+full_path)
            return full_path
        else:
            #print ('false '+ path)
            pass
    return None

def get_file_mapping(lectureName):
    #print(lecture_mapping['lectureName'])
    return lecture_mapping[lectureName]

def get_avg_rating_page(path_to_pdf_file, lecture_name):
    pdf_dir = 'data/docs/pdf_page_gesamtbewertung'
    html_dir = 'data/docs/html_page_gesamtbewertung'
    
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)
        os.makedirs(html_dir)

    pdf_page_path = pdf_dir + '/'+ lecture_name +'.pdf'
    output = PdfFileWriter()
    outputStream = open(pdf_page_path, "wb")
    input = PdfFileReader(open(path_to_pdf_file, "rb"))
    for page in input.pages:
        if(input.getPageNumber(page)<7):
            pass
        else:
            text = page.extractText()
            if("Gesamtbewertung" in text):
                output.addPage(page)
                output.write(outputStream)
                #print('****************')
                #print(pdf_page_path)
                break 
    return pdf_page_path

def get_comments_page(path_to_pdf_file, lecture_name):
    pdf_dir = 'data/docs/pdf_page_comments'
    html_dir = 'data/docs/html_page_comments'
    
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)
        os.makedirs(html_dir)

    pdf_page_path = pdf_dir + '/'+ lecture_name +'.pdf'
    output = PdfFileWriter()
    outputStream = open(pdf_page_path, "wb")
    input = PdfFileReader(open(path_to_pdf_file, "rb"))
    for page in input.pages:
        if(input.getPageNumber(page)<7):
            pass
        else:
            text = page.extractText()
            if("Freitext_Kritik" in text or ("Positive Resonanz" in text)):
                output.addPage(page)
                output.write(outputStream)
                #print('++++++++++++++++')
                #print(pdf_page_path)

    for page in input.pages:
        if(input.getPageNumber(page)<7):
            pass
        else:
            text = page.extractText()
            if("Freitext_Kritik" in text or ('Verbesserungsvorschläge'in text)):
                output.addPage(page)
                output.write(outputStream)
                #print('++++++++++++++++')
                #print(pdf_page_path)
                 
    return pdf_page_path

def create_html_file(pdf_page_path, title, lecture_name):
    html_file_path = 'data/docs/html_page_' + title + '/'+ lecture_name +'.html'
    command = 'pdf2txt.py -o'+ html_file_path + ' -t html '+ pdf_page_path 
    os.system(command) 
    return html_file_path

def get_avg_rating(file, semester):
    avg_rating = None
    if(semester == 'ws19-20'):
        with open(file, 'r') as f:
            contents = f.read()
            soup = BeautifulSoup(contents, features="lxml")
            avg_rating = soup.select_one('body > div:nth-child(61) > span:nth-child(3)').get_text() if soup.select_one('body > div:nth-child(61) > span:nth-child(3)') != None else  soup.select_one('body > div:nth-child(62) > span:nth-child(3)').get_text() if soup.select_one('body > div:nth-child(62) > span:nth-child(3)') else soup.select_one('body > div:nth-child(64) > span:nth-child(3)').get_text() if soup.select_one('body > div:nth-child(64) > span:nth-child(3)') else soup.select_one('body > div:nth-child(60) > span:nth-child(3)').get_text() if soup.select_one('body > div:nth-child(60) > span:nth-child(3)') else soup.select_one('body > div:nth-child(66) > span:nth-child(3)').get_text() if soup.select_one('body > div:nth-child(66) > span:nth-child(3)') else soup.select_one('body > div:nth-child(65) > span:nth-child(3)').get_text() if soup.select_one('body > div:nth-child(65) > span:nth-child(3)') else soup.select_one('body > div:nth-child(63) > span:nth-child(3)').get_text() if soup.select_one('body > div:nth-child(63) > span:nth-child(3)') else ''
    elif(semester == 'ss19'):
        with open(file, 'r') as f:
            contents = f.read()
            soup = BeautifulSoup(contents, features="lxml")
            avg_rating = soup.select_one('body > div:nth-child(3) > span:nth-child(2)').get_text() if soup.select_one('body > div:nth-child(3) > span:nth-child(2)') else soup.select_one('body > div:nth-child(21) > span:nth-child(2)').get_text() if soup.select_one('body > div:nth-child(21) > span:nth-child(2)') else soup.select_one('body > div:nth-child(22) > span:nth-child(2)').get_text() if soup.select_one('body > div:nth-child(22) > span:nth-child(2)') != None else soup.select_one('body > div:nth-child(24) > span:nth-child(2)').get_text() if soup.select_one('body > div:nth-child(24) > span:nth-child(2)') != None else soup.select_one('body > div:nth-child(25) > span:nth-child(2)').get_text() if soup.select_one('body > div:nth-child(25) > span:nth-child(2)') else soup.select_one('body > div:nth-child(26) > span:nth-child(2)').get_text() if soup.select_one('body > div:nth-child(26) > span:nth-child(2)') else soup.select_one('body > div:nth-child(28) > span:nth-child(3)').get_text() if soup.select_one('body > div:nth-child(28) > span:nth-child(3)') else soup.select_one('body > div:nth-child(29) > span:nth-child(2)').get_text() if soup.select_one('body > div:nth-child(29) > span:nth-child(2)') else ''
    
    if avg_rating.endswith('\n'): avg_rating = avg_rating[:-1]
    return avg_rating.strip()

def get_comments(comment_files):
    students_comments = []
    with open(comment_files, 'r') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, features="lxml")
        students_comments = soup.select_one('body > div:nth-child(4) > span:nth-child(1)').get_text().split('\n') if soup.select_one('body > div:nth-child(4) > span:nth-child(1)') != None else ''
    return students_comments[:-1]

def get_positive_comments(comment_files):
    with open(comment_files, 'r') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, features="html5lib")
        start = soup.find(string=re.compile("Positive Resonanz"))
        if start: 
            positive_comments = start.find_parent('div').find_next_siblings("div")[0].get_text()
            if 'Anz' in positive_comments or 'Was hat Ihnen an' in positive_comments:
                positive_comments = start.find_parent('div').find_next_siblings("div")[1].get_text()
            elif '%' in positive_comments:
                positive_comments = soup.select_one('body > div:nth-child(79)').get_text() if soup.select_one('body > div:nth-child(79)') != None else soup.select_one('body > div:nth-child(50)').get_text() if soup.select_one('body > div:nth-child(50)') != None else []
          
            positive_comments = positive_comments.split('\n')
            if 'Keine Angabe' in positive_comments: positive_comments.remove('Keine Angabe')                 
          
            return positive_comments[:-1]
        else: return []

def get_negative_comments(comment_files):
    with open(comment_files, 'r') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, features="lxml")
        negative_comments = soup.find(string=re.compile("Verbesserungsvorschläge")).find_parent('div').find_next_siblings("div")[0].get_text().split('\n') if soup.find(string=re.compile("Verbesserungsvorschläge")) else []
        if 'Keine Angabe' in negative_comments: negative_comments.remove('Keine Angabe')
        negative_comments = negative_comments
    return negative_comments[:-1]

def get_lecture(semester, lecture, full_path_pdf, cleaned_lecture_name):
    lecture_copie = lecture
    global lecture_id
    full_path_avg_pdf_page = get_avg_rating_page(full_path_pdf, cleaned_lecture_name)

    if full_path_avg_pdf_page != None:
        full_path_avg_html_page = create_html_file(full_path_avg_pdf_page, 'gesamtbewertung', cleaned_lecture_name)
    if full_path_avg_html_page != None and semester == 'ws19-20':
        avg_rating = get_avg_rating(full_path_avg_html_page, 'ws19-20')
        #print('avg_rating = '+str(avg_rating))
    elif full_path_avg_html_page != None and semester == 'ss19':
        avg_rating = get_avg_rating(full_path_avg_html_page, 'ss19')

    full_path_comments_pdf_page = get_comments_page(full_path_pdf, cleaned_lecture_name)
    if full_path_comments_pdf_page != None:
        full_path_comments_html_page = create_html_file(full_path_comments_pdf_page, 'comments', cleaned_lecture_name)
    if full_path_comments_html_page != None and semester == 'ws19-20':
        comments = get_comments(full_path_comments_html_page)
        lecture_copie['avg_rating'] = avg_rating
        lecture_copie['semester'] = semester
        lecture_copie['comments'] = comments
        lecture_copie['lecture_id'] = lecture_id
        lecture_id+=1
    elif full_path_comments_html_page != None and semester == 'ss19':
        positive_comments = get_positive_comments(full_path_comments_html_page)
        negative_comments = get_negative_comments(full_path_comments_html_page)
        comments = positive_comments + negative_comments 
        
        lecture_copie['avg_rating'] = avg_rating
        lecture_copie['semester'] = semester
        lecture_copie['comments'] = comments
        lecture_copie['lecture_id'] = lecture_id
        lecture_id+=1
    return lecture_copie

def clean_lecture_name(lecture_name):

    cleaned_lecture_name = re.sub('[&,:]', '', lecture_name).replace('/', '').replace('  ', ' ').replace(' ', '_').replace('-', '_').lower()
    if cleaned_lecture_name.endswith('_'): cleaned_lecture_name = cleaned_lecture_name[:-1]
    return cleaned_lecture_name

with requests.Session() as sesh:
    def get_elements(list):
        strings = []
        for element in list:
            strings.append(element.string)
        return strings

    f = open("data/docs/readMe.md", "a")
    f.write("# List of Lectures with their url:\n")

    for url in urls:
        response = sesh.get(url)
        html = response.text

        soup = BeautifulSoup(html, features="lxml")   
        lecture_name = soup.select_one('#masttitle').span.extract().get_text() if soup.select_one('#masttitle').span != None else soup.select_one('#masttitle').get_text()
        if lecture_name.endswith(' '): lecture_name = lecture_name[:-1]
        if '&' in lecture_name: lecture_name = lecture_name.replace('&', 'and')
        if '/' in lecture_name: lecture_name = lecture_name.replace('/', '')
        if '-' in lecture_name: lecture_name = lecture_name.replace('-', ' ')
        assigned_people = get_elements(soup.select_one('fieldset.highlight-blue:nth-child(8) > ul:nth-child(2)').find_all('a') if soup.select_one('fieldset.highlight-blue:nth-child(8) > ul:nth-child(2)') != None else [])
        study_courses = get_elements(soup.select_one('fieldset.highlight-blue:nth-child(7) > ul:nth-child(2)').find_all('a') if soup.select_one('fieldset.highlight-blue:nth-child(7) > ul:nth-child(2)') != None else []) 
        language = soup.select_one('fieldset.highlight-blue > table > tr:nth-child(3) > td:nth-child(2)').string if soup.select_one('fieldset.highlight-blue > table > tr:nth-child(3) > td:nth-child(2)') != None else ""
        description = soup.select_one('#en_EN > table > tr > td:nth-child(2)') or ""
        learning_targets = soup.select_one('#en_EN > table > tr:nth-child(2) > td:nth-child(2)') or ""
        pre_qualifications = soup.select_one('#en_EN > table > tr:nth-child(4) > td:nth-child(2)').get_text() if soup.select_one('#en_EN > table > tr:nth-child(4) > td:nth-child(2)') != None else ""
        course_format = soup.select_one ('fieldset.highlight-blue > table > tr:nth-child(2) > td:nth-child(2) > p').get_text() if soup.select_one ('fieldset.highlight-blue > table > tr:nth-child(2) > td:nth-child(2) > p') != None else ""
        
        f.write('* ['+ lecture_name +'](' + url + ')\n')
        cleaned_lecture_name = clean_lecture_name(lecture_name)
        print('cleaned Lecture name: '+cleaned_lecture_name)
        full_path_pdf_ws19_20 = get_path('data/docs/ws_19_20', cleaned_lecture_name)
        full_path_pdf_ss19 = get_path('data/docs/ss2019', cleaned_lecture_name)
        semester = None
        
        lecture = {
            'name': lecture_name,
            'description': str(description),
            'assigned_people': assigned_people,
            'language': language,
            'learning_targets': str(learning_targets),
            'pre_qualifications': pre_qualifications,
            'course_format': course_format,
            'study_courses': study_courses                                               
        }

        if full_path_pdf_ws19_20 != None and full_path_pdf_ss19 != None:
            semesters = ['ws19-20', 'ss19']
            path = {'ws19-20': full_path_pdf_ws19_20, 'ss19': full_path_pdf_ss19}
            for semester in semesters:
                lecture_new = get_lecture(semester, lecture, path[semester], cleaned_lecture_name)
                #print('Both Semester---'+lecture_name)
                if lecture_new != None: id = lectures.insert_one(lecture_new.copy()).inserted_id
        elif full_path_pdf_ws19_20 != None and full_path_pdf_ss19 == None:
            semester = 'ws19-20'
            lecture_new = get_lecture(semester, lecture, full_path_pdf_ws19_20, cleaned_lecture_name)
            #print('Only Winter---'+lecture_name)
            if lecture_new != None: id = lectures.insert_one(lecture_new).inserted_id
        elif full_path_pdf_ws19_20 == None and full_path_pdf_ss19 != None:
            semester = 'ss19'
            lecture_new = get_lecture(semester, lecture, full_path_pdf_ss19, cleaned_lecture_name)
            #print('Only Sommer---'+lecture_name)
            if lecture_new != None: id = lectures.insert_one(lecture_new).inserted_id
        else:
            print('None---'+lecture_name)
            lecture_new = lecture
            lecture_new['lecture_id'] = lecture_id
            lecture_new['comments'] = ''
            lecture_new['avg_rating'] = ''
            lecture_new['semester'] = ''

            id = lectures.insert_one(lecture_new).inserted_id
            lecture_id+=1
            
    f.close()
