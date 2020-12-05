from flask import Flask, render_template, request, url_for,send_from_directory
import os
from geo import getTweetLocation

PEOPLE_FOLDER = os.path.join('static', 'people_photo')

app = Flask(__name__)
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

if __name__=='__main__':
    app.run(debug=True)
