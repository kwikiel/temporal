from flask import Flask, render_template, jsonify, request, redirect, url_for

# Temporal App related requirements 
import requests
import json
from sqlalchemy import create_engine


#Helper functions TODO put in another module 
from utils import flat_dict 
from utils import flatten_json

app = Flask(__name__)

# Config to another file which is not commited to Github

db_string = "postgres://jmpghcklooyqqc:829aa0758cbf569bc0e9f59351c32d08cf65f7ac9bb72cdd93517d9f7ae51c4f@ec2-54-247-169-129.eu-west-1.compute.amazonaws.com:5432/ddntt771qmmvnr"
db = create_engine(db_string)

def insert_records():
    result_set = db.execute("SELECT * FROM urls")  
    for r in result_set:  
        print("URL ID"+str(r[0])) # Record_ID external key 
        print("Downloaded: "+str(r[1])) # URL value 
        for x,y in flat_dict(r[1]).items():
            db.execute(f"INSERT INTO records (url_id, path, metric) VALUES ({r[0]},'{x}',{y})")

@app.route('/')
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
        dates.append(r[4].strftime("%Y-%m-%d %H:%M:%S"))
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
