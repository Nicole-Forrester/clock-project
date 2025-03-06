#!/usr/bin/env python3

# Import modules from flask:
#   Flask - a class, used to create a Flask instance
#   request - used to interact with APIs, to access incoming request data
#   render_template - enables the reference and use of external HTML code or scripts
#   make_response - sets additional headers in a view
from flask import Flask, request, render_template, make_response, jsonify
from pymongo import MongoClient
# import random
# from urllib.parse import quote_plus
# from bson.json_util import dumps
# from pathlib import Path
# import json

# Create instance of Flask class, assign to app
app = Flask(__name__)

data = []

@app.route("/")
def index():
    # Pull data from the database

    for clock in clock_data:

        breakpoint()
        data.append({
            "clock": clock.get("Clock"),
            "training_data_type": clock.get("Data type used in training"),
            "species": clock.get("Species"),
            "training_species": clock.get("Tissues used in training"),
            "training_age_range": clock.get("Age range in years (training)"),
            "mad": clock.get("Mean absolute deviance (years)"),
            "num_cpgs": clock.get("# of CpGs"),
            "genome_build": clock.get("Genome build"),
            "method": clock.get("Method"),
            "cpg_locs": clock.get("Got CpG locations?"),
            "language": clock.get("Language"),
            "code": clock.get("Code"),
            "paper": clock.get("Paper"),
            "url": clock.get("URL"),
        })

    
    return render_template("index.html", data=data)


def connect_to_database():
    client = MongoClient("mongodb://localhost:27017/")
    db = client.clocks_database

    global clocks
    clocks = db.clocks_collection
    global clock_data
    clock_data = clocks.find()

# Connect to the database
connect_to_database()
