from flask import Flask, render_template, jsonify, request, redirect, url_for, make_response
from flask_cors import CORS

# Temporal App related requirements 
import requests
import json
from sqlalchemy import create_engine


#Helper functions TODO put in another module 
from utils import flat_dict 
from utils import flatten_json
import os 
SQLALCHEMY_DATABASE_URI = os.environ['HEROKU_POSTGRESQL_CYAN_URL']
app = Flask(__name__)

CORS(app)

# Config to another file which is not commited to Github
app.config['TEMPLATES_AUTO_RELOAD'] = True


db_string = SQLALCHEMY_DATABASE_URI


db = create_engine(db_string)

def insert_records():
    result_set = db.execute("SELECT * FROM urls")  
    for r in result_set:  
        print("URL ID"+str(r[0])) # Record_ID external key 
        print("Downloaded: "+str(r[1])) # URL value 
        for x,y in flat_dict(r[1]).items():
            db.execute(f"INSERT INTO records (url_id, path, metric) VALUES ({r[0]},'{x}',{y})")


@app.route('/')
def landing_page():
    return render_template("landing.html")


@app.route('/app')
def index():
    # Todo link to url_id and possible paths 
    jr = []
    result_set = db.execute("SELECT * FROM urls") 
    for r in result_set:
        jr.append(r)
    return render_template("index.html", jr=jr)

@app.route("/time_series/<int:url_id>")
def paths_for_url(url_id):
    jr = []
    result_set = db.execute(f"SELECT path FROM records WHERE url_id={url_id} GROUP BY path") 
    for r in result_set:
        jr.append(r)
    return render_template("paths.html", jr=jr, url_id=url_id)



@app.route('/time_series/<int:url_id>/<string:path>')
def show(url_id, path):
    jr = []
    result_set = db.execute(f"SELECT * FROM records WHERE url_id={url_id} AND path='{path}'") 
    for r in result_set:
        jr.append(r)
    return render_template("show.html", jr=jr)

@app.route('/time_series/<int:url_id>/<string:path>/json')
def show_json(url_id, path):
    jr = []
    dates = [] 
    result_set = db.execute(f"SELECT * FROM records WHERE url_id={url_id} AND path='{path}'") 
    for r in result_set:
        dates.append(r[4].strftime("%Y-%m-%dT%H:%M:%S"))
        jr.append(r[3])
    #return jsonify({'data': [dict(row) for row in jr]})
    #return jsonify({"data1":jr})
    return json.dumps({path:jr, "dates":dates})

@app.route('/add_url', methods=["GET", "POST"])
def add_url():
    if request.method == "GET":
        return render_template('addurl.html')
    if request.method == "POST":
        url = request.form['url']
        db.execute(f"INSERT INTO urls (http, status) VALUES ('{url}','active')")
        return redirect(url_for('hello_world'))

@app.route('/10minutes')
def hello_world():
    insert_records()
    return redirect(url_for('index'))


@app.route('/download')
def download():
    csv = '''price
75.0
104.0
369.0
300.0
92.0
64.0
265.0
35.0
287.0
69.0
52.0
23.0
287.0
87.0
114.0
114.0
98.0
137.0
87.0
90.0
63.0
69.0
80.0
113.0
58.0
115.0
30.0
35.0
'''
    response = make_response(csv)
    response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    #response.headers["Content-Disposition"] = "attachment; filename=books.csv"
    return response
