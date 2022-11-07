import csv
from datetime import datetime
from tempfile import NamedTemporaryFile
import shutil

from flask import Flask, render_template, request, redirect, url_for

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
        courses = sorted(courses, key=lambda d: datetime.strptime(d[sort_by], "%B %d, %Y"), reverse=True)
    elif sort_by == 'start_time':
        courses = sorted(courses, key=lambda d: datetime.strptime(d[sort_by], "%I:%M %p"), reverse=True)
    else:
        courses = sorted(courses, key=lambda d: d[sort_by], reverse=True)
    
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
    course = list(filter(lambda courses: courses['id'] == course_id, courses))[0]
    return render_template('course.html', course=course)

@app.route('/courses/create', methods=['GET', 'POST'])
def add_course():

    if request.method == 'POST':
        # List to store courses
        courses = []
        # Open courses file for reading
        with open(csvpath) as f:
            reader = csv.DictReader(f)
            courses = list(reader)

        last_course = courses[-1]
        # Get new course id by incrementing last_course id by 1
        new_course_id = int(last_course['id']) + 1

        new_course = {}

        # add form data to new dict
        new_course['id'] = new_course_id
        new_course['name'] = request.form['course_name']
        new_course['pet'] = request.form['pet_type']
        new_course['level'] = request.form['level']
        # convert date to Oct D, Y format
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').strftime('%B %d, %Y')
        new_course['start_date'] = start_date
        new_course['length'] = request.form['length']
        # convert time to 12hour format
        try:
            start_time = datetime.strptime(request.form['start_time'], '%H:%M').strftime("%I:%M %p") 
        except:
            start_time_24 = request.form['start_time']
            start_time_24_hr = start_time_24[:2]
            start_time_24_min = start_time_24[-2:]
            pm_am = ''
            start_time_12_hr = ''
            start_time_12_min = start_time_24_min
            if int(start_time_24_hr) >= 12:
                pm_am = 'pm'

                if int(start_time_24_hr) != 12:
                    start_time_12_hr = int(start_time_24_hr) - 12
                else:
                    start_time_12_hr = 12
            else:
                pm_am = 'am'
                start_time_12_hr = start_time_24_hr
                
            start_time = f'{start_time_12_hr}:{start_time_12_min} {pm_am}'

        new_course['start_time'] = start_time
        new_course['duration'] = request.form['duration']
        new_course['trainer'] = request.form['trainer']
        new_course['description'] = request.form['description']

        # Open courses file for writing new row
        with open(csvpath, 'a', newline='\n') as f:
            # Pass the file object and a list
            # of column names to DictWriter()
            writer = csv.DictWriter(f, fieldnames=new_course.keys())
            writer.writerow(new_course)

        # since POST request, redirect after Submit goes to courses
        return redirect(url_for('courses'))
    return render_template('course_form.html', course={}, title="Add a Course")


@app.route('/courses/<course_id>/edit', methods=['GET', 'POST'])
def edit_course(course_id): 

    if request.method == 'POST':

        course_update = {}

        # add form data to new dict
        course_update['id'] = course_id
        course_update['name'] = request.form['course_name']
        course_update['pet'] = request.form['pet_type']
        course_update['level'] = request.form['level']
        # convert date to Oct D, Y format
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').strftime('%B %d, %Y')
        course_update['start_date'] = start_date
        course_update['length'] = request.form['length']
        # convert time to 12hour format
        try:
            start_time = datetime.strptime(request.form['start_time'], '%H:%M').strftime("%I:%M %p") #.strftime('%I:%M %p')
        except:
            start_time_24 = request.form['start_time']
            start_time_24_hr = start_time_24[:2]
            start_time_24_min = start_time_24[-2:]
            pm_am = ''
            start_time_12_hr = ''
            start_time_12_min = start_time_24_min
            if int(start_time_24_hr) >= 12:
                pm_am = 'pm'

                if int(start_time_24_hr) != 12:
                    start_time_12_hr = int(start_time_24_hr) - 12
                else:
                    start_time_12_hr = 12
            else:
                pm_am = 'am'
                start_time_12_hr = start_time_24_hr
                
            start_time = f'{start_time_12_hr}:{start_time_12_min} {pm_am}'
            
        course_update['start_time'] = start_time
        course_update['duration'] = request.form['duration']
        course_update['trainer'] = request.form['trainer']
        course_update['description'] = request.form['description']

        # to be used in doing update of a course
        tempfile = NamedTemporaryFile(mode='w', delete=False)

        # Open the original and temp file
        with open(csvpath, 'r') as csvfile, tempfile:
             # Create dict writer objects for the read and write operations on the respective files
            reader = csv.DictReader(csvfile, fieldnames=course_update.keys())
            writer = csv.DictWriter(tempfile, fieldnames=course_update.keys())

            for row in reader:
                # if the current row matches the row to be updated replace the values with the updates
                if row['id'] == str(course_id):
                    row['name'] = course_update['name']
                    row['pet'] = course_update['pet']
                    row['level'] = course_update['level']
                    row['start_date'] = course_update['start_date']
                    row['length'] = course_update['length']
                    row['start_time'] = course_update['start_time']
                    row['duration'] = course_update['duration']
                    row['trainer'] = course_update['trainer']
                    row['description'] = course_update['description']
                writer.writerow(row) 

        # Replace the original file with the new temp file containing updates
        shutil.move(tempfile.name, csvpath)
        #goes to the updated course
        return redirect(url_for('course',  course_id=course_id))

    course = None

    with open(csvpath) as f:
        reader = csv.DictReader(f)
        courses = list(reader)

    # Seach for course in the list of courses
    course = list(filter(lambda courses: courses['id'] == course_id, courses))[0] 

    # return the start date and start time in the format that can be presentedin the html form
    course['start_date'] = datetime.strptime(course['start_date'], '%B %d, %Y').strftime('%Y-%m-%d')
    course['start_time'] = datetime.strptime(course['start_time'], '%I:%M %p').strftime('%H:%M')
    # render the form to update the course
    return render_template('course_form.html', course=course, title="Update Course")

@app.route('/courses/<course_id>/delete', methods=['GET', 'POST'])
def delete_course(course_id): 
    course = None

    with open(csvpath) as f:
        reader = csv.DictReader(f)
        courses = list(reader)

    # Seach for course in the list of courses
    course = list(filter(lambda courses: courses['id'] == course_id, courses))[0] 

    if request.method == 'POST':

        # temporary file that will be used for the original file updates
        tempfile = NamedTemporaryFile(mode='w', delete=False)

        with open(csvpath, 'r') as csvfile, tempfile:
            # Create dict writer objects for the read and write operations on the respective files
            reader = csv.DictReader(csvfile, fieldnames=course.keys())
            writer = csv.DictWriter(tempfile, fieldnames=course.keys())

            # loop through the rows in courses csv file
            for row in reader:
                if row['id'] != str(course_id):                   
                    writer.writerow(row)                
        
        # Replace the original file with the new temp file containing updates
        shutil.move(tempfile.name, csvpath)
        return redirect(url_for('courses'))
    
    # render the delete confirmation file
    return render_template('delete_form.html', course=course)