#!/usr/bin/env python3

# Import modules from flask:
#   Flask - a class, used to create a Flask instance
#   request - used to interact with APIs, to access incoming request data
#   render_template - enables the reference and use of external HTML code or scripts
#   make_response - sets additional headers in a view
from flask import Flask, request, render_template, make_response, jsonify
from pymongo import MongoClient
from pathlib import Path
import json
import numpy as np

# Create instance of Flask class, assign to app
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


def get_server_configuration():
    with open(Path(__file__).resolve().parent.parent / "configuration/conf.json") as infh:
        conf = json.loads(infh.read())
    return conf

def connect_to_database(conf):
    client = MongoClient("mongodb://localhost:27017/")
    db = client.clocks_database

    global clocks
    clocks = db.clocks_collection

    global cpgs
    cpgs = db.cpgs_collection

@app.route("/data", methods=["GET"])
def get_data():
    # Fetch all records from MongoDB
    clock_data = clocks.find({}, {"_id": 0})
    cpg_data = list(cpgs.find({}, {"_id": 0}))

    # Convert Clock Mongo cursor to list of dictionaries and handle None values
    clean_clock_data = []
    for item in clock_data:
        clean_clock_item = {key: ("" if value is None else value) for key, value in item.items()}
        clean_clock_data.append(clean_clock_item)

    # Convert CpG Mongo cursor to list of dictionaries and handle None values
    clean_cpg_data = []
    for item in cpg_data:
        clean_cpg_item = {key: ("" if value is None else value) for key, value in item.items()}
        clean_cpg_data.append(clean_cpg_item)

    # Return the data in a format DataTables expects
    return jsonify({"clocks": clean_clock_data,
                    "cpgs": clean_cpg_data})


# Individual clock pages
@app.route("/clock/<clock_name>")
def clock_page(clock_name):
  # Find the specific clock in MongoDB
  clock = clocks.find_one({"clock": clock_name}, {"_id": 0})

  # Find all CpGs related to this clock
  cpg_list = list(cpgs.find({"clock": clock_name}, {"_id": 0}))
  
  return render_template("clock_page.html", clock_name=clock_name, clock=clock, cpgs=cpg_list)


# Run clocks page
@app.route("/runclocks")
def run_clocks():
    return render_template("run_clocks.html")


# Don't need now but might need later
def get_form():
    # In addition to the main arguments we also add the session
    # string from the cookie
    session = ""

    if "groupactivity_session_id" in request.cookies:
        session = request.cookies["groupactivity_session_id"]

    if request.method == "GET":
        form = request.args.to_dict(flat=True)
        form["session"] = session
        return form

    elif request.method == "POST":
        form = request.form.to_dict(flat=True)
        form["session"] = session
        return form


# Read the main configuration
server_conf = get_server_configuration()

# Connect to the database
connect_to_database(server_conf)
