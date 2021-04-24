from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'sqlproject'

# Enter your database connection details below
app.config['MYSQL_HOST'] = '13.233.85.192'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mysql'
app.config['MYSQL_DB'] = 'threatre'

# Intialize MySQL
mysql = MySQL(app)
global t

# http://localhost:5000/insertmovie/ - this will be the login page, we need to use both GET and POST requests
@app.route('/insertmovie/', methods=['GET', 'POST'])
def insertmovie():
    msg = ''
    if request.method == 'POST' and 'movie_id' in request.form and 'movie_name' in request.form and 'duration' in request.form and 'movie_type' in request.form and 'genre' in request.form and 'hall_id' in request.form:
        movie_id = request.form['movie_id']
        movie_name = request.form['movie_name']
        duration = request.form['duration']
        movie_type = request.form['movie_type']
        genre = request.form['genre']
        hall_id = request.form['hall_id']
        show_time=request.form['show_time']
        url = request.form['url']
     
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM movies WHERE movie_id = %s AND movie_name = %s AND hall_id=%s AND show_time=%s', (movie_id, movie_name,hall_id, show_time))

        movies  = cursor.fetchone()
        
        if movies:
            msg = 'movie already exists!'
        elif not movie_id or not movie_name:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO movies VALUES (%s, %s, %s, %s,%s,%s,%s,%s)', (movie_id,movie_name,duration,movie_type,genre,hall_id,show_time,url))
            mysql.connection.commit()
            msg = 'You have successfully registered!'

    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('movieinsert.html', msg=msg)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('select * from movies')
    data = cursor.fetchall()
    return render_template('1.html',data=data)
@app.route('/moviebooking', methods=['GET', 'POST'])
def details():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('select * from movies')
    data = cursor.fetchall()
    if request.method == 'POST' and 'billing_first_name' in request.form and 'billing_last_name':
        prefered_location = request.form['billing_first_name']
        Age = request.form['billing_last_name']
    return render_template('2.html',data=data)


@app.route('/moviebooking/<time>', methods=['GET', 'POST'])
def get_data(time):
     t =time
    #t=request.values.get('Name')
    
@app.route('/choosetheatre', methods=['GET', 'POST'])
def choosetheatre():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('select * from movies')
    data = cursor.fetchall()
    
    return render_template('3.html',data=data)
'''
@app.route('/', methods=['GET', 'POST'])
def abc():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('select * from movies')
    data = cursor.fetchall()
    for row in data:
        movie_name = row['movie_id']
        duration = row['duration']
        movie_type = row['movie_type']
        print('===============================================')
        print('movie name', movie_name)
        print('duration :', duration)
        print('movie type   :', movie_type)
        print('===============================================')

    return "hello"
'''