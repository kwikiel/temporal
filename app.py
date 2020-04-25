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

@app.route('/create_db')
def create_db():
    db.execute("CREATE TABLE urls (id serial,http varchar(100) NOT NULL UNIQUE,status varchar(100) NOT NULL,PRIMARY KEY (id));")
    db.execute("CREATE TABLE records (id serial,url_id integer NOT NULL,path text, metric real,published_date timestamp DEFAULT CURRENT_TIMESTAMP,PRIMARY KEY (id)FOREIGN KEY (url_id) REFERENCES urls(id) ON DELETE CASCADE;")

    return "DB created"






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
    result_set = db.execute(f"SELECT * FROM records WHERE url_id={url_id} AND path='{path}' ORDER BY published_date") 
    for r in result_set:
        dates.append(r[4].strftime("%Y-%m-%dT%H:%M:%S"))
        jr.append(r[3])
    #return jsonify({'data': [dict(row) for row in jr]})
    #return jsonify({"data1":jr})
    return json.dumps({path:jr, "dates":dates})

# This is similar to above json but with csv
@app.route('/time_series/<int:url_id>/<string:path>/csv')
def show_csv(url_id, path):
    output = "date,value\n"
    result_set = db.execute(f"SELECT * FROM records WHERE url_id={url_id} AND path='{path}' ORDER BY published_date") 
    for r in result_set:
        output += r[-1].strftime("%Y-%m-%dT%H:%M:%S") +","+str(int(r[3])) +"\n"
    response = make_response(output)
    response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    return response


    

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
