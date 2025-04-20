from flask import Flask, render_template, url_for, request
import sqlite3
import os
import shutil
import subprocess

connection = sqlite3.connect('user_data.db')
cursor = connection.cursor()

command = """CREATE TABLE IF NOT EXISTS user(name TEXT, password TEXT, mobile TEXT, email TEXT)"""
cursor.execute(command)

command = """CREATE TABLE IF NOT EXISTS records(Date TEXT, Time TEXT, Number TEXT, image TEXT)"""
cursor.execute(command)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('userlog.html')

@app.route('/userlog', methods=['GET', 'POST'])
def userlog():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']

        query = "SELECT name, password FROM user WHERE name = '"+name+"' AND password= '"+password+"'"
        cursor.execute(query)

        result = cursor.fetchall()

        if result:
            return render_template('userlog.html')
        else:
            return render_template('index.html', msg='Sorry, Incorrect Credentials Provided,  Try Again')
    return render_template('index.html')


@app.route('/userreg', methods=['GET', 'POST'])
def userreg():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']
        mobile = request.form['phone']
        email = request.form['email']
        
        print(name, mobile, email, password)

        command = """CREATE TABLE IF NOT EXISTS user(name TEXT, password TEXT, mobile TEXT, email TEXT)"""
        cursor.execute(command)

        cursor.execute("INSERT INTO user VALUES ('"+name+"', '"+password+"', '"+mobile+"', '"+email+"')")
        connection.commit()

        return render_template('index.html', msg='Successfully Registered')
    
    return render_template('index.html')

@app.route('/analyse', methods=['GET', 'POST'])
def analyse():
    if request.method == 'POST':
        image = request.form['img']
        path = 'static/test/'+image

        os.system(f'python detect.py --source {path}')
        if '.mp4' in image:
            return render_template('userlog.html', videDisplay="http://127.0.0.1:5000/static/test/"+image, videDisplay1="http://127.0.0.1:5000/static/result/output.mp4")
        else:
            return render_template('userlog.html', ImageDisplay="http://127.0.0.1:5000/static/test/"+image, ImageDisplay1="http://127.0.0.1:5000/static/result/output.jpg")
    return render_template('userlog.html')

@app.route('/livestream')
def livestream():
    os.system(f'python detect.py --source 0')
    return render_template('userlog.html', videDisplay="http://127.0.0.1:5000/static/result/output.mp4")

@app.route('/records')
def records():
    connection = sqlite3.connect('user_data.db')
    cursor = connection.cursor()
    query = "SELECT * FROM records"
    cursor.execute(query)
    result = cursor.fetchall()
    return render_template('records.html', result=result)

@app.route('/logout')
def logout():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
