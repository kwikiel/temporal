from flask import Flask, render_template

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

@app.route('/time_series/<int:url_id>/<string:path>')
def show(url_id, path):
    jr = []
    result_set = db.execute(f"SELECT * FROM records WHERE url_id={url_id} AND path='{path}'") 
    for r in result_set:
        jr.append(r)
    return render_template("show.html", jr=jr)


@app.route('/10minutes')
def hello_world():
    insert_records()
    return '200'