from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import mail as m
from datetime import date

today = date.today()
today = today.strftime("%Y-%m-%d")

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'sqlproject'

# Enter your database connection details below
app.config['MYSQL_HOST'] = '65.2.151.198'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mysql'
app.config['MYSQL_DB'] = 'threatre'

# Intialize MySQL
mysql = MySQL(app)

movieName = ""
movietype=""
time = ""
Primary_location=""
email=""
Age=0
T_name=""
Price=0
Person=0
url300=""
username=""
hall_id=0


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
        url196 = request.form['url196']
        url300 = request.form['url300']
        url360 = request.form['url360']
     
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM movies WHERE movie_id = %s AND movie_name = %s AND hall_id=%s AND show_time=%s', (movie_id, movie_name,hall_id, show_time))

        movies  = cursor.fetchone()
        
        if movies:
            msg = 'movie already exists!'
        elif not movie_id or not movie_name:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO movies VALUES (%s, %s, %s, %s,%s,%s,%s,%s,%s,%s)', (movie_id,movie_name,duration,movie_type,genre,hall_id,show_time,url196,url300,url360))
            mysql.connection.commit()
            msg = 'Movie is successfully registered!'

    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('movieinsert.html', msg=msg)

@app.route('/Moviedeletion', methods=['GET', 'POST'])
def Moviedeletion():
    msg = ''
    if request.method == 'POST' and 'to_movie_name' in request.form and 'from_movie_name' in request.form and 'duration' in request.form and 'movie_type' in request.form and 'genre' in request.form:
        #movie_id = request.form['movie_id']
        #abc=str(movie_id)
        from_movie_name = request.form['from_movie_name']
        to_movie_name = request.form['to_movie_name']
        duration = request.form['duration']
        movie_type = request.form['movie_type']
        genre = request.form['genre']
        url196 = request.form['url196']
        url300 = request.form['url300']
        url360 = request.form['url360']
     
     
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        
        cursor.execute('SELECT * FROM movies WHERE movie_name = %s ', (from_movie_name,))
        
        movies  = cursor.fetchone()
        
        if movies:
            cursor.execute('update movies set movie_name=%s,duration=%s,movie_type=%s,genre=%s,url196=%s,url300=%s,url360=%s WHERE movie_name = %s ', (to_movie_name,duration,movie_type,genre,url196,url300,url360,from_movie_name))
            mysql.connection.commit()
            msg = 'Movie is successfully Updated!!!'
        elif not to_movie_name or not from_movie_name:
            msg = 'Please fill out the form!!!!!!!!!'
        else:
            msg = 'You did some mistake in form so correct it!!'

    elif request.method == 'POST':
        msg = 'Please fill out the form!!!'
    return render_template('moviedeletion.html', msg=msg)

@app.route('/theatreinsert', methods=['GET', 'POST'])
def theatreinsert():
    msg = ''
    if request.method == 'POST' and 'hall_id' in request.form and 'hall_name' in request.form and 'location' in request.form and 'price' in request.form :
        hall_id = request.form['hall_id']
        hall_name = request.form['hall_name']
        location = request.form['location']
        price = request.form['price']
        
     
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM theatre WHERE hall_id = %s AND hall_name = %s AND location=%s AND price=%s', (hall_id,hall_name,location,price))

        movies  = cursor.fetchone()
        
        if movies:
            msg = 'Theatre already exists!'
        elif not hall_id or not hall_name or not location or not price:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO theatre VALUES (%s, %s,%s, %s, %s)', (hall_id,"admin",hall_name,location,price))
            mysql.connection.commit()
            msg = 'Theatre is successfully registered!'

    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('theatreinsert.html', msg=msg)

@app.route('/theatredeletion', methods=['GET', 'POST'])
def theatredeletion():
    msg = ''
    if request.method == 'POST' and 'hall_id' in request.form and 'hall_name' in request.form  :
        hall_id = request.form['hall_id']
        hall_name = request.form['hall_name']
           
     
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM theatre WHERE hall_id = %s AND hall_name = %s ', (hall_id,hall_name))
        
        movies  = cursor.fetchone()
        
        if movies:
            cursor.execute('delete from theatre where hall_id=%s and hall_name=%s',(hall_id,hall_name))
            mysql.connection.commit()
            msg = 'Theatre deleted!'
        elif not hall_id or not hall_name :
            msg = 'Please fill out the form!'
        else:
            msg = 'You made some error please solve!'

    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('theatredeletion.html', msg=msg)





@app.route('/', methods=['GET', 'POST'])
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('select distinct movie_name,movie_type,duration,url196,genre from movies where genre = "Drama"')
    data = cursor.fetchall()
    cursor.execute('select distinct movie_name, duration, url196 , movie_type,genre from movies where genre = "Action"')
    action=cursor.fetchall()
    cursor.execute('select distinct movie_name, duration, url196 , movie_type,genre from movies where genre = "Science Fiction"')
    sifi=cursor.fetchall()
    return render_template('1.html',data=data,action=action,sifi=sifi)

@app.route('/dashboard/<var>', methods=['GET', 'POST'])
def movie_name(var):
    global movieName
    global movietype
    spill2=var.split(",")

    movieName = spill2[0]
    movietype=spill2[1]
    return movieName

@app.route('/moviebooking', methods=['GET', 'POST'])
def details():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('select distinct movie_name,movie_type,duration,url360,genre from movies where movie_name="{}"'.format(movieName))
    data = cursor.fetchall()
    
    return render_template('2.html',data=data)


@app.route('/moviebooking/<var>', methods=['GET', 'POST'])
def get_data(var):
    global time
    time = var
    
    return time

@app.route('/location/<var>', methods=['GET', 'POST'])
def get_location(var):
    global Primary_location
    global T_name
    global Price
    global Person
    spill=var.split(',')
    Primary_location = spill[0]
    T_name=spill[1]
    P=int(spill[2])
    Price=Person*P
    print(Price)
    return Primary_location
'''
@app.route('/theatre/<var>', methods=['GET', 'POST'])
def get_threatre(var):
    
    T_name = var
    print(T_name)
    return T_name
'''  

@app.route('/choosetheatre', methods=['GET', 'POST'])
def choosetheatre():
    if request.method == 'POST' and 'billing_first_name' in request.form and 'billing_last_name' in request.form and 'noofperson' in request.form:
        movie_name  = movieName
        show_time = time
        global Age
        global Person
        global url300
        global hall_id
        #print("Movie Name: "+movie_name)
        #print("Show Time: "+ show_time)
        prefered_location = request.form['billing_first_name']
        Age = request.form['billing_last_name']
        Age=int(Age)
        Person=request.form['noofperson']
        Person=int(Person)
        
        #print(prefered_location)
        #print(Age)
        if movietype=="A":
            if Age>=18:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                # cursor.execute("select movie_name,movie_type,movies.hall_id,show_time,location from movies, theatre where movies.hall_id = theatre.hall_id and movie_name = {} and  show_time = {} and location = {}".format(movie_name.movie,get_data.t,prefered_location))
                cursor.execute("select movie_name,movie_type,url300,movies.hall_id,show_time,location,theatre.hall_name,theatre.hall_id,theatre.price from movies, theatre where movies.hall_id = theatre.hall_id and movie_name = '{}' and  show_time = '{}' and location = '{}'".format(movie_name,show_time,prefered_location))
                movieData = cursor.fetchall()
                url300=movieData[0]['url300']
                hall_id=movieData[0]['hall_id']
            else:
                return "You are Under aged for this Movie Please select another one !!"
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # cursor.execute("select movie_name,movie_type,movies.hall_id,show_time,location from movies, theatre where movies.hall_id = theatre.hall_id and movie_name = {} and  show_time = {} and location = {}".format(movie_name.movie,get_data.t,prefered_location))
            cursor.execute("select movie_name,movie_type,url300,movies.hall_id,show_time,location,theatre.hall_name,theatre.hall_id,theatre.price from movies, theatre where movies.hall_id = theatre.hall_id and movie_name = '{}' and  show_time = '{}' and location = '{}'".format(movie_name,show_time,prefered_location))
            movieData = cursor.fetchall()
            url300=movieData[0]['url300']
            hall_id=movieData[0]['hall_id']
        if movieData:
            length_moviedata=len(movieData)
            return render_template('3.html',data=movieData, length=length_moviedata)
        else:
            return "No Data Available"

    return redirect(url_for('details'))


@app.route('/choosetheatre/different', methods=['GET', 'POST'])
def choosetheatrediff():
    movie_name  = movieName
    show_time = time
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select movie_name,movie_type,url300,movies.hall_id,show_time,location,theatre.hall_name,theatre.price from movies, theatre where movies.hall_id = theatre.hall_id and movie_name = '{}' and  show_time = '{}' ".format(movie_name,show_time))
    movieDatadiff = cursor.fetchall()
    length_moviedatadiff=len(movieDatadiff)
    if length_moviedatadiff>=6:
        length_moviedatadiff=6
    else:
        return "Movie data is too short. Please Try another one!!"
    
    return render_template('3_1.html',data=movieDatadiff, length=length_moviedatadiff)








# http://localhost:5000/pythonlogin/ - this will be the login page, we need to use both GET and POST requests

@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        global email
        global username
        email = request.form['email']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email_id = %s AND password = %s', (email, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        username=account['username']
        # If account exists in user table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['user_id']
            session['email_id'] = account['email_id']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or email/password incorrect
            msg = 'Incorrect email/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)

# http://localhost:5000/python/logout - this will be the logout page
@app.route('/pythonlogin/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))


# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'dob' in request.form:
        # Create variables for easy access
        
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        dob=request.form['dob']

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into user table
            cursor.execute("insert into user values (null,'{}','{}','{}','{}')".format(username,password,email,dob))
            #cursor.execute('INSERT INTO user VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
@app.route('/pythonlogin/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        #return render_template('home.html', username=session['username'])
        return redirect(url_for('Billing_details'))

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for loggedin users
@app.route('/pythonlogin/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE user_id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))



@app.route('/billing', methods=['GET', 'POST'])
def Billing_details():
    data=Primary_location
    user_email=email
    user_Age=Age
    time_slot=time
    Theratre_name=T_name
    moviename=movieName  
    global Price  
    return render_template('4.html',data=data,useremail=user_email,user_age=user_Age,timeslot=time_slot,Theratrename=Theratre_name,Movie=moviename,Price=Price,person=Person)

@app.route('/onlinepay', methods=['GET', 'POST'])
def onlinepay():
    global url300
    global movieName
    
    
    return render_template('onlinepay.html',url=url300,moviename=movieName,Price=Price)

@app.route('/mailing',methods=['GET','Post'])
def mailing():
    
    global today
   
    print(Price,0,Person,Primary_location,time,T_name,today,movieName,username,T_name)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)     
    #cursor.execute('INSERT INTO ticket_cnf VALUES (%s, %s,%s, %s, %s,%s, %s,%s, %s, %s)', (Price,0,Person,Primary_location,time,T_name,movieName,))
    #cursor.execute('insert into ticket_cnf values(%s, %s,%s, %s, %s,%s, %s,%s, %s, %s)', (Price,0,Person,Primary_location,time,T_name,today,movieName,('select user_id from user where username = %s'),('select hall_id from theatre where location = %s ')),(username,T_name))
    cursor.execute("insert into ticket_cnf(total_cost,payment,no_of_tickets,hall_name,show_time,location,date,movie_name,user_id,hall_id) values ('{}','{}','{}','{}','{}','{}','{}','{}',(select user_id from user where email_id = '{}'),(select hall_id from theatre where location = '{}' ))".format(Price,0,Person,Primary_location,time,T_name,today,movieName,email,Primary_location))
    mysql.connection.commit()
    
    m.mail(username,movieName,T_name,Primary_location,time,Price,email)
    return "0"






@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        if cursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, password,)):
            # Fetch one record and return result
            account = cursor.fetchone()
            username=account['username']
            # If account exists in user table in out database
            if account:
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account['user_id']
                session['email_id'] = account['email_id']
                session['username'] = account['username']
                # Redirect to home page
                return redirect(url_for('adminhome'))
            else:
                # Account doesnt exist or email/password incorrect
                msg = 'Incorrect Username/password!'
        else:
            msg= 'Incorrect Username/Password!'
    # Show the login form with message (if any)
    return render_template('adminlogin.html', msg=msg)

@app.route('/admin_home')
def adminhome():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        #return render_template('home.html', username=session['username'])
        return render_template('home.html', username=session['username'])

    # User is not loggedin redirect to login page
    return redirect(url_for('admin_login'))

@app.route('/adminlogout')
def adminlogout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('admin_login'))



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