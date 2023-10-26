from flask import Flask, render_template, request, redirect, url_for, abort
from func import Course, User
import sqlite3
import json
from dotenv import load_dotenv

app = Flask(__name__)
import os

load_dotenv() 
app.config['SECRET KEY'] = os.getenv('SECRET_KEY')

"""
Obtains a database connection, convert rows to dictionary cursors.
Easier to access using dictionary cursors as apposed to tuples
"""
def getdbConnection():
    con = sqlite3.connect('database.db')
    con.row_factory = sqlite3.Row
    # cursor = con.cursor() on hold due to commit error, using simple DB connection instead
    return con

"""
Takes in all rows from course table in database as parameter.
Uses all the cells from each row to initiate Course object and appends the object to an array
Returns the array of courses
Purpose is too make formatting of the schedule easier on the html template and use an object oriented approach
"""
def formatCourses(_courses):
    courses = []
    for course in _courses:
        courses.append(Course(course['title'], course['instructor'], [course['start_time'], course['end_time']], course['grade'], json.loads(course['meeting_days']), course['rowid'])) # json.loads converts json file back to python list
    return courses

"""
Renders the view schedule html.
Obtains DB connection then pulls all the rows from the course table in the database.
Passes those rows to formatCourses function to return list of course objects.
Finally, we obtain a schedule dictionary using create schedule function from User class and pass that to html template to render.
"""
@app.route('/view-schedule')
def view_schedule():
    cur = getdbConnection()
    _courses = cur.execute('SELECT rowid, * FROM course').fetchall()
    cur.close()

    courses = formatCourses(_courses)
    user1 = User('Christian', 'Junior', courses) # temporary
    schedule = user1.create_schedule()

    if _courses is None:
        abort(404)

    return render_template('view_schedule.html',schedule=schedule)


"""
Simple index page that greets the user
"""
@app.route('/')
def index():
    user1 = User('Christian', 'Junior', []) # temp
    return render_template('index.html', user=user1.name)


"""
Renders the add course html page that allows a user to add courses to their schedule.
We explicitely state the POST method as users will be passing data from a form to our function.
Then we pull all the information we need from the form to create a course and assign them to variables.
We convert the meeting days of type list to a JSON string so we can store it in our database. ( SQL Lite does not support python lists )
Then we execute SQL command to insert this new course into our database.
Finally, we redirect the user the the view-schedule page to view their newly added course
"""
@app.route('/add-course', methods=('GET', 'POST'))
def add_course():
    if request.method == 'POST':
        title = request.form['title']
        grade = request.form['grade']
        instructor = request.form['instructor']
        start = request.form['start']
        end = request.form['end']
        meeting_days = request.form.getlist('check')
        json_meeting_days = json.dumps(meeting_days) # convert meeting days ( type list ) into json string to store in SQL database

        cur = getdbConnection()
        cur.execute('INSERT INTO course (title, instructor, start_time, end_time, grade, meeting_days) VALUES (?,?,?,?,?,?)',
                    (title, instructor, start, end, grade, json_meeting_days))

        cur.commit()
        cur.close()

        return(redirect(url_for('view_schedule')))


    return render_template('add_course.html')


"""
Established connection to database and executes command pulling all of the posts from the database as well as the row id.
The row id needs to explicitely stated because it is a hidden column in SQLite. Then we format the courses and create
a schedule. We save the length of the courses iterable for later use to conditionally display a button on our frontend.
Then we pull the post id's from our frontend and loop through the list of id's deleting each course from the database.
"""
@app.route('/delete-course', methods=('GET', 'POST'))
def del_course():
    cur = getdbConnection()
    _courses = cur.execute('SELECT rowid, * FROM course').fetchall()

    courses = formatCourses(_courses)
    user1 = User('Christian', 'Junior', courses) # temporary
    schedule = user1.create_schedule()
    count = len(courses)

    if request.method == 'POST':
        post_ids = request.form.getlist('courses')
        post_ids = set(post_ids) # remove duplicates by converting to a set
        print(post_ids)
        for id in post_ids:
            cur.execute('DELETE FROM course WHERE rowid = ?', (id))

        cur.commit()
        cur.close()
        return(redirect(url_for('view_schedule')))

    return render_template('delete_course.html', schedule=schedule, count=count)











