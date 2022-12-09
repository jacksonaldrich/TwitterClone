'''
This is a "hello world" flask webpage.
During the last 2 weeks of class,
we will be modifying this file to demonstrate all of flask's capabilities.
This file will also serve as "starter code" for your Project 5 Twitter webpage.

NOTE:
the module flask is not built-in to python,
so you must run pip install in order to get it.
After doing do, this file should "just work".
'''

from datetime import datetime
import json

from flask import Flask, render_template, request, make_response, redirect
app = Flask(__name__)

import argparse
parser = argparse.ArgumentParser(description='Create a database for the twitter project')
parser.add_argument('--db_file', default='twitter_clone.db')
args = parser.parse_args()

import sqlite3

# anything that starts with a @ is called a "decorator" in python
# in general, decorators modify the fuctions that follow them
"""
@app.route('/')
def root(): # put HTML in here
    '''
    text = 'hello cs40'
    text = '<strong>' + text + '</strong>' # + 100
    return text
    #return "hello <strong>world</strong>"
    '''
    # render_template does preprocessing of the input html file;
    # techically, the input to the render_template function is in a language called jinja2
    # the output of render_template is html
    return render_template('root.html')
"""

@app.route('/')
def root():
    print_debug_info()
    # connect to the database
    con = sqlite3.connect(args.db_file)
    username = request.cookies.get('username')
    print("cookie username = ", username)
    # construct messages,
    # which is a list of dictionaries,
    # where each dictionary contains the information about a message
    messages = []
    sql = """
    SELECT sender_id,message,created_at
    FROM messages
    ORDER BY created_at DESC;
    """
    cur_messages = con.cursor()
    cur_messages.execute(sql)
    for row_messages in cur_messages.fetchall():

        # convert sender_id into a username
        sql = """
        SELECT username,age
        FROM users
        WHERE id=?;
        """
        cur_users = con.cursor()
        cur_users.execute(sql, [str(row_messages[0])])
        for row_users in cur_users.fetchall():
            pass

        # build the message dictionary ## put in a tags 
        messages.append({ 
            'message': row_messages[1],
            'username': row_users[0],
            'age': row_users[1],
            'posted at' : row_messages[2]
            })

    # check if logged in correctly
    username = request.cookies.get('username')
    password = request.cookies.get('password')
    good_credentials = are_credentials_good(username, password)
    print('good_credentials=', good_credentials)

    # render the jinja2 template and pass the result to firefox
    return render_template('root.html', messages=messages, logged_in=good_credentials, username=username)


def print_debug_info():
    # GET method
    print('request.args.get("username")=', request.args.get("username"))
    print('request.args.get("password")=', request.args.get("password"))

    # POST method
    print('request.form.get("username")=', request.form.get("username"))
    print('request.form.get("password")=', request.form.get("password"))

     # cookies 
    print('request.coookies.get("username")=', request.cookies.get("username"))
    print('request.cookies.get("password")=', request.cookies.get("password"))


def are_credentials_good(username, password):
    con = sqlite3.connect(args.db_file)
    user_dict = {}
    sql = """
    SELECT username,password
    FROM users
    """
    cur_users = con.cursor()
    cur_users.execute(sql)
    for user in cur_users.fetchall():
        user_dict.update({user[0]:user[1]})


    if username in user_dict and password == user_dict[username]:
        return True
    else:
        return False


@app.route('/login', methods=['GET', 'POST']) # put this after the "standard" URL to display
def login(): # this is the login route
    print_debug_info()
    # requests (plural) librry for downloading;
    # now we need request singular
    username = request.form.get('username')
    password = request.form.get('password')
    print('username=', username)
    print('password=', password)

    good_credentials = are_credentials_good(username, password)
    print('good_credentials=', good_credentials)

    # the first time we've visited, no form submission
    if username is None:
        return render_template('login.html', bad_credentials=False)

    # they submitted a form; we're on the POST method
    else:
        if not good_credentials:
            return render_template('login.html', bad_credentials=True)
        else:
            # if we get here, the we're logged in
            #return 'login successful'

            # create a cookie that contains the username/password info
            username = request.cookies.get('username')
            password = request.cookies.get('password')

            username = request.form.get('username')
            password = request.form.get('password')
            template = render_template('login.html', bad_credentials=False, username=username)
            response = make_response(template) 
            response.set_cookie('username', username)
            response.set_cookie('password', password)
            #return template
            return response
            #return redirect("http://127.0.0.1:5000/", code=302)
            #return render_template('login.html', bad_credentials=False, username=username)


# schema://hostname/path
# the @app.route defines the path
# the hostname and schema are given to you in the output of the triangle button
# the url is http://127.0.0.1:5000/logout
@app.route('/logout') # AssertionError means that the def are probably the same 
def logout():
    print_debug_info()
    #1 + 'error' # this will throw an error
    template = render_template('logout.html')
    response = make_response(template) 
    response.delete_cookie('username')
    response.delete_cookie('password')

    return response

@app.route('/create_message', methods=['GET', 'POST'])
def create_message():
    print_debug_info()

    username = request.cookies.get('username')
    message = request.form.get('message')

    con = sqlite3.connect(args.db_file)
    cur=con.cursor()

    sql = """
        SELECT id
        FROM users
        WHERE username=?;
        """
    cur.execute(sql, [username])

    for row_users in cur.fetchall():
        pass

    id = row_users[0]
    now = datetime.now()

    dt_string= now.strftime("%Y-%m-%d %H:%M:%S")
    print(dt_string)    
    try: #ADD a message with this
        if message: #stores it into db
            sql = """
            insert into messages (sender_id,message,created_at) values (?, ?, ?);
            """
        
            con=sqlite3.connect(args.db_file)
            cur=con.cursor()
            cur.execute(sql, [str(id), message, dt_string])
            con.commit()
            return render_template('create_message.html', good_message = True, username=username)

        else:
            return render_template('create_message.html', good_message = False, username=username)
    except (sqlite3.OperationalError): 
        return render_template('create_message.html', good_message = False, username=username)
   

@app.route('/create_user', methods=['GET', 'POST']) 
def create_user():
    print_debug_info()

    username = request.form.get('username')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    age = request.form.get('age')
    print('username=', username)
    print('password=', password)
    print('age=', age)
    if password == password2:
        if username and password:
            if is_valid_username(username):
                if age: 
                    sql = """
                    INSERT into users (username, password, age) values (?, ?, ?);
                    """ 
                    ###USE THE bndings with ?? just like problem 4 
                    #change the execute to have the list 
                    con = sqlite3.connect(args.db_file)
                    cur_users = con.cursor()

                    try:
                        cur_users.execute(sql, [username, password, age])
                        con.commit()
                        return render_template('create_user.html', bad_username = False, created_user = True)
                    except (sqlite3.IntegrityError):
                        return render_template('create_user.html', bad_username = True, created_user = False)

                else:
                    sql = """
                    INSERT into users (username, password) values (?, ?);
                    """
                    con = sqlite3.connect(args.db_file)
                    cur_users = con.cursor()
                    try:
                        cur_users.execute(sql, [username, password])
                        return render_template('create_user.html', bad_username = False, created_user = True)
                    except (sqlite3.IntegrityError):
                        return render_template('create_user.html', bad_username = True, created_user = False)
            else:
                return render_template('create_user.html', bad_username = True, created_user = False)
        else:
            return render_template('create_user.html', created_user = False)
    else:
        return render_template('create_user.html', bad_password = True, created_user = False)

def is_valid_username(username):
    con = sqlite3.connect(args.db_file)
    users = []
    sql = """
    SELECT username
    FROM users
    """
    cur_users = con.cursor()
    cur_users.execute(sql)
    for user in cur_users.fetchall():
        users.append({user[0]})

    if username in users:
        return False
    else:
        return True

@app.route('/search_message', methods=['POST', 'GET'])
def search_message():
    if request.form.get('search'):
        con = sqlite3.connect(args.db_file)
        cur = con.cursor()
        cur.execute('''
            SELECT sender_id, message, created_at, id from messages;
        ''')
        rows = cur.fetchall()
        messages = []
        
        for row in rows:
            if request.form.get('search') in row[1]:
                messages.append({'username': row[0], 'text': row[1], 'created_at':row[2], 'id':row[3]})
        messages.reverse()
        return render_template('search_message.html', messages=messages, username=request.cookies.get('username'), password=request.cookies.get('password'))
    else:
        return render_template('search_message.html', default=True, username=request.cookies.get('username'), password=request.cookies.get('password'))

"""
def compile_code_inline(line):
    accumulator = ''
    inline_code = False
    count = line.count('`') ## check for all circumstances
    if count == 3:
        return line
    for c in line:
        if c == '<' and inline_code == True:
            accumulator+='&lt;'
        elif c == '>' and inline_code == True:
            accumulator+='&gt;'
        elif c == '`':
            count -= 1
            if inline_code==False and count>=1:
                accumulator+='<code>'
            if inline_code==False and count<1:
                accumulator+=c
            if inline_code == True:
                accumulator+= '</code>'
            inline_code=not inline_code
        else:
            accumulator += c
    line=accumulator
    return line
"""

"""
##add this to base: <li><a href='/change_password'>change password</a></li>
@app.route('/change_password/<username>', methods=['POST', 'GET'])
def change_password(username):
    if request.form.get('oldPassword'):
        if request.cookies.get('username') == username:
            con = sqlite3.connect(args.db_file) 
            cur = con.cursor()
            cur.execute('''
                SELECT password from users where username=?;
            ''', (username,))
            rows = cur.fetchall()
            oldPassword = rows[0][0]
            
            if request.form.get('oldPassword') == oldPassword:
                if request.form.get('password1') == request.form.get('password2'):
                    cur.execute('''
                        UPDATE users
                        SET password = ?
                        WHERE username = ?
                    ''', (request.form.get('password1'), request.cookies.get('username')))
                    con.commit()
                    return make_response(render_template('change_password.html', allGood=True, username=request.cookies.get('username'), password=request.cookies.get('password')))
                else: 
                    return make_response(render_template('change_password.html', repeatPass=True, username=request.cookies.get('username'), password=request.cookies.get('password')))
            else: 
                return make_response(render_template('change_password.html', wrongPass=True, username=request.cookies.get('username'), password=request.cookies.get('password')))
        else: 
            return make_response(render_template('change_password.html', not_your_username=True, username=request.cookies.get('username'), password=request.cookies.get('password')))
    else: return make_response(render_template('change_password.html', username=request.cookies.get('username'), password=request.cookies.get('password')))
"""

@app.route('/home.json')

def home_json():
    """
    con = sqlite3.connect(args.db_file)
    cur = con.cursor()
    cur.execute('''
        SELECT sender_id, message, created_at, id from messages;
    ''')
    rows = cur.fetchall()
    messages = []
    for row in rows:
        messages.append({'username': row[0], 'text': row[1], 'created_at':row[2], 'id':row[3]})
    messages.reverse()
    """
########

    print_debug_info()
    # connect to the database
    con = sqlite3.connect(args.db_file)
    username = request.cookies.get('username')
    print("cookie username = ", username)
    # construct messages,
    # which is a list of dictionaries,
    # where each dictionary contains the information about a message
    messages = []
    sql = """
    SELECT sender_id,message,created_at
    FROM messages
    ORDER BY created_at DESC;
    """
    cur_messages = con.cursor()
    cur_messages.execute(sql)
    for row_messages in cur_messages.fetchall():

        # convert sender_id into a username
        sql = """
        SELECT username,age
        FROM users
        WHERE id=?;
        """
        cur_users = con.cursor()
        cur_users.execute(sql, [str(row_messages[0])])
        for row_users in cur_users.fetchall():
            pass

        # build the message dictionary ## put in a tags 
        messages.append({
            'username': row_users[0],
            'age': row_users[1],
            'message': row_messages[1],
            'posted at' : row_messages[2]
            })

    return json.dumps(messages)


app.run()


# http://127.0.0.1:5000 paste this into URL to get webpage
# "Unable to connect" is usually because the Flask program is not running 
# need to stop and restart program to see changes 
# "Internal Server Error" means error in code
# '127.0.0.1 - - [28/Nov/2022 10:12:03] "GET /logout HTTP/1.1" 200 -' is a log
# 200 is a status code
# "Not Found" returns a 404 status code. No route defined  
# status code 500 is like 404 but the server died somehow (not the route)

###how to prevent SQL INJECTION?
# make sure to use this with ALL of the inputs where there is execute 
# change the execute and can mix ? with python 

#delete messages 

