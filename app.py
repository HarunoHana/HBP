import csv
from datetime import datetime
from tempfile import NamedTemporaryFile
import shutil
from os.path import exists

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config.from_pyfile(app.root_path + '/config_defaults.py')
if exists(app.root_path + '/config.py'):
    app.config.from_pyfile(app.root_path + '/config.py')

import database

csvpath = app.root_path + '/courses.csv'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/courses/', methods=['GET', 'POST'])
def courses():
    args = request.args
    
    # List to store courses
    courses = []

    courses = database.get_courses()

    if request.method == 'POST':
        # Search by pet type
        pet = request.form['pet']
        if pet:         
            # Seach for course in the list of courses
            courses = list(filter(lambda courses: courses['pet'] == pet, courses))

    # Get sort by which column
    sort_by = args.get("sort", default="start_date", type=str)    

    # Sort courses list using start date
    if sort_by == 'start_date':
        # The strptime() method creates a datetime object from the given string
        courses = sorted(courses, key=lambda d: d['start_date'], reverse=True)
    elif sort_by == 'start_time':
        courses = sorted(courses, key=lambda d: d['start_time'], reverse=True)
    else:
        courses = sorted(courses, key=lambda d: d[sort_by], reverse=True)

    for count,course in enumerate(courses):
        courses[count]['start_date'] = course['start_date'].strftime("%B %d, %Y")
        courses[count]['start_time'] = course['start_time'].strftime("%I:%M %p")
        
    
    return render_template('courses.html', courses=courses)

@app.route('/courses/<course_id>')
def course(course_id):
    course = None
    
    course = database.get_course(course_id)
    
    course['start_date'] = course['start_date'].strftime("%B %d, %Y")
    course['start_time'] = course['start_time'].strftime("%I:%M %p")

    return render_template('course.html', course=course)

@app.route('/courses/create', methods=['GET', 'POST'])
def add_course():

    if request.method == 'POST':
        new_course = {}

        # add form data to new dict
        new_course['name'] = request.form['course_name']
        new_course['pet'] = request.form['pet_type']
        new_course['level'] = request.form['level']
        # convert date to Oct D, Y format
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
        new_course['start_date'] = start_date
        new_course['length'] = request.form['length']
        start_time = f"2022-1-1 {request.form['start_time']}" 
        new_course['start_time'] = start_time
        new_course['duration'] = request.form['duration']
        new_course['trainer'] = request.form['trainer']
        new_course['description'] = request.form['description']

        database.add_course(new_course['name'],new_course['pet'],new_course['level'],new_course['start_date'],new_course['start_time'], new_course['duration'], new_course['length'],new_course['trainer'],new_course['description'])
        # since POST request, redirect after Submit goes to courses
        return redirect(url_for('courses'))
    return render_template('course_form.html', course={}, title="Add a Course")


@app.route('/courses/<course_id>/edit', methods=['GET', 'POST'])
def edit_course(course_id): 

    if request.method == 'POST':

        course_update = {}

        # add form data to new dict
        course_update['id'] = int(course_id)
        course_update['name'] = request.form['course_name']
        course_update['pet'] = request.form['pet_type']
        course_update['level'] = request.form['level']
        # convert date to Oct D, Y format
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
        course_update['start_date'] = start_date
        course_update['length'] = request.form['length']
        # convert time to 24hour format        
        start_time = f"2022-1-1 {request.form['start_time']}" 
            
        course_update['start_time'] = start_time
        course_update['duration'] = request.form['duration']
        course_update['trainer'] = request.form['trainer']
        course_update['description'] = request.form['description']

        database.update_course(course_update['id'], course_update['name'],course_update['pet'],course_update['level'],course_update['start_date'],course_update['start_time'], course_update['duration'], course_update['length'],course_update['trainer'],course_update['description'])

        #goes to the updated course
        return redirect(url_for('course',  course_id=course_id))

    course = None 
    course = database.get_course(course_id)
    # return the start date and start time in the format that can be presentedin the html form
    # course['start_date'] = course['start_date'].strftime("%B %d, %Y")
    course['start_time'] = course['start_time'].strftime("%H:%M")
    # render the form to update the course
    return render_template('course_form.html', course=course, title="Update Course")

@app.route('/courses/<course_id>/delete', methods=['GET', 'POST'])
def delete_course(course_id): 
    if request.method == 'POST':
        course_id = int(course_id)
        database.delete_course(course_id)
        return redirect(url_for('courses'))
        
    course = None 
    course = database.get_course(course_id)
    # return the start date and start time in the format that can be presentedin the html form
    course['start_date'] = course['start_date'].strftime("%B %d, %Y")
    course['start_time'] = course['start_time'].strftime("%I:%M %p")
    # render the delete confirmation file
    return render_template('delete_form.html', course=course)

@app.route('/test/courses', methods=['GET',])
def test_sql_get_courses():
    courses = database.get_courses()
    print(courses)
    return redirect(url_for('courses'))

@app.route('/test/course', methods=['GET',])
def test_sql_get_course():
    course = database.get_course(1)
    print(course)
    return redirect(url_for('courses'))

@app.route('/test/courses/create', methods=['GET',])
def test_sql_add_course():
    database.add_course("Morning Obedience 1","Dogs","Beginner","2022-9-07","08:00:00", "45", "4","Pie Caso","Get the best pics of your pet")
    return redirect(url_for('courses'))

@app.route('/test/courses/update', methods=['GET',])
def test_sql_update_course():
    database.update_course(2, "Morning Obedience 2","Dogs","Beginner","2022-9-07","08:00:00", "45", "4","Pie Caso","Get the best pics of your pet")
    return redirect(url_for('courses'))

@app.route('/test/attendees', methods=['GET',])
def test_sql_get_attendees():
    attendees = database.get_attendees()
    print(attendees)
    return redirect(url_for('courses'))

@app.route('/test/attendees/create', methods=['GET',])
def test_sql_add_attendee():
    database.add_attendee(1, "John","Doe","25479585352","johndoe@mail.com", "2022-9-07")
    return redirect(url_for('courses'))

@app.route('/test/attendees/edit', methods=['GET',])
def test_sql_update_attendee():
    database.edit_attendee(1, 1, "John","Doe","25479585352","johndoe@gmail.com", "2002-9-07")
    return redirect(url_for('courses'))

@app.route('/test/attendees/delete', methods=['GET',])
def test_sql_delete_attendee():
    database.delete_attendee(1)
    return redirect(url_for('courses'))