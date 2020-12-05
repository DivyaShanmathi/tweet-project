from flask import Flask ,render_template,request,jsonify,session

import sqlite3 as sql
import base64
import pandas as pd
from sklearn.preprocessing import LabelEncoder
#from flask_bootstrap import Bootstrap
import numpy as np
from sklearn.utils import shuffle
import os
from flask import Flask, render_template, request, url_for,send_from_directory
import os
from geo import getTweetLocation


app = Flask(__name__)
app.secret_key = 'any random string'
PEOPLE_FOLDER = os.path.join('static', 'people_photo')
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

   
def validate(username,password):
    con = sql.connect('static/chat.db')
    completion = False
    with con:
        cur = con.cursor()
        cur.execute('SELECT * FROM persons')
        rows = cur.fetchall()
        for row in rows:
            dbuser = row[1]
            dbpass = row[2]
            if dbuser == username:
                completion = (dbpass == password)
    return completion


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        completion = validate(username,password)
        if completion == False:
            error = 'invalid Credentials. please try again.'
        else:
            session['username'] = request.form['username']
            return render_template('pic.html')
    return render_template('index.html', error=error)



    
@app.route('/register', methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        try:
            name = request.form['name']
            username = request.form['username']
            password = request.form['password']
            with sql.connect("static/chat.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO persons(name,username,password) VALUES (?,?,?)",(name,username,password))
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"
        finally:
            return render_template("index.html",msg = msg)
            con.close()
    return render_template('register.html')


@app.route('/list')
def list():
   con = sql.connect("static/chat.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from persons")
   
   rows = cur.fetchall();
   return render_template("list.html",rows = rows)
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

@app.route('/pic')
def show_index():
    full_filename = 'tweet.png'
    return render_template("pic.html", filename = full_filename)


@app.route('/search', methods = ['POST'])
def search_tweet():
    print("Serching",request.form['sear'])
    getTweetLocation(request.form['sear'])
    full_filename = 'tweet.png'
    return send_from_directory(".", filename=full_filename)
    return render_template("pic.html", filename = full_filename)


@app.route('/upload/<filename>')
def send_file(filename):
    print(PEOPLE_FOLDER)
    print(os.path.join("."))
    return send_from_directory(".", filename=filename)



if __name__ == '__main__':
   app.run(debug = True )
