import csv
from datetime import datetime

from flask import Flask, render_template, request

app = Flask(__name__)
csvpath = app.root_path + '/courses.csv'
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/courses/', methods=['GET', 'POST'])
def courses():
    args = request.args
    
    # List to store courses
    courses = []
    # Open courses file for reading
    with open(csvpath) as f:
        # Read file using csv
        reader = csv.DictReader(f)
        # Convert csv data into list
        courses = list(reader)

    if request.method == 'POST':
        # Searcg by pet type
        pet = request.form['pet']
        if pet:         
            # Seach for course in the list of courses
            courses = list(filter(lambda courses: courses['pet'] == pet, courses))

    # Get sort by which column
    sort_by = args.get("sort", default="start_date", type=str)    

    # Sort courses list using start date
    if sort_by == 'start_date':
        # The strptime() method creates a datetime object from the given string
        courses = sorted(courses, key=lambda d: datetime.strptime(d[sort_by], "%B %d, %Y"))
    elif sort_by == 'start_time':
        courses = sorted(courses, key=lambda d: datetime.strptime(d[sort_by], "%I:%M %p"))
    else:
        courses = sorted(courses, key=lambda d: d[sort_by])
    
    return render_template('courses.html', courses=courses)

@app.route('/courses/<course_id>')
def course(course_id):
    course = None
    # Open courses file for reading
    with open(csvpath) as f:
        # Read file using csv
        reader = csv.DictReader(f)
        # Convert csv data into list
        courses = list(reader)

    # Seach for course in the list of courses
    course = list(filter(lambda courses: courses['name'] == course_id, courses))[0]
    return render_template('course.html', course=course)