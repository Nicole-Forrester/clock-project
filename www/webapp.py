#!/usr/bin/env python3

# Import modules from flask:
#   Flask - a class, used to create a Flask instance
#   request - used to interact with APIs, to access incoming request data
#   render_template - enables the reference and use of external HTML code or scripts
#   jsonify - converts Python dictionaries or lists into a JSON response
#   Response - manually constructs a Flask HTTP response, allows for returning a downloadable csv file
#   redired - sends the user to a different route (HTTP redirect)
#   flash - stores short message to be displayed to user on next page load (e.g. error/success notifications), requires app.secret_key
from flask import Flask, request, render_template, jsonify, Response, redirect, flash
from pymongo import MongoClient
from pathlib import Path
import json
import pandas as pd
from collections import OrderedDict
import csv
import io
import os
import random
import subprocess


# Map from methyAge internal names to database clock names
methyAge_name_map = {
    "HorvathS2013": "Horvath",
    "HannumG2013": "Hannum",
    "HorvathS2018": "SkinBlood",
    "LevineM2018": "PhenoAge",
    "YangZ2016": "epiTOC",
    "epiTOC2": "epiTOC2",
    "DunedinPACE": "DunedinPACE",
    # Add others as needed
}

# Random ID generator
def generate_id(size):
    """
    Generic function used for creating IDs.  Makes random IDs
    just using uppercase letters
    @size:    The length of ID to generate
    @returns: A random ID of the requested size
    """
    alphanumeric = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    code = ""
    for _ in range(size):
        code += random.choice(alphanumeric)
    return code


# Create instance of Flask class, assign to app
app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for flashing messages


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

  # Readable labels for chart display
  annotation_labels = OrderedDict([
      ("kb1to5_cpgs", "1 to 5 kb"),
      ("firstexon_cpgs", "First Exon"),
      ("utr3_cpgs", "3' UTR"),
      ("utr5_cpgs", "5' UTR"),
      ("body_cpgs", "Gene Body"),
      ("cds_cpgs", "CDS"),
      ("exon_cpgs", "Exon"),
      ("igr_cpgs", "Intergenic Region"),
      ("intron_cpgs", "Intron"),
      ("promoter_cpgs", "Promoter"),
      ("gene_cpgs", "Gene"),
      ("tss1500_cpgs", "TSS1500"),
      ("tss200_cpgs", "TSS200"),
      ("no_ucsc_annotation_cpgs", "No UCSC Annotation")
      ])
  island_labels = OrderedDict([
      ("island_cpgs", "Island"),
      ("shore_cpgs", "Shore"),
      ("shelf_cpgs", "Shelf"),
      ("no_island_info_cpgs", "No Island Info")
      ])
  
  # Extract only non-zero values for the charts using dictionary comprehension
  annotation_data = {
      annotation_labels[k]: (clock.get(k) or 0)
      for k in annotation_labels if (clock.get(k) or 0) > 0
      }
  island_data = {
      island_labels[k]: (clock.get(k) or 0)
      for k in island_labels if (clock.get(k) or 0) > 0
      }
  
  return render_template("clock_page.html",
                         clock_name=clock_name,
                         clock=clock,
                         cpgs=cpg_list,
                         annotation_data=annotation_data,
                         island_data=island_data)

# Download link for CpGs per clock on indv clock page
@app.route("/clock/<clock_name>/download_cpgs")
def download_cpgs(clock_name):
    # Get CpGs for the clock
    cpg_list = list(cpgs.find({"clock": clock_name}, {"_id": 0}))

    # If empty, return 404
    if not cpg_list:
        return f"No CpGs found for clock '{clock_name}'", 404

    # Create CSV in memory
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=cpg_list[0].keys())
    writer.writeheader()
    writer.writerows(cpg_list)
    output.seek(0)

    # Create response
    return Response(
        output,
        mimetype="text/csv",
        headers={
            "Content-Disposition": f"attachment;filename={clock_name} CpGs.csv"
        }
    )


# Run clocks page
@app.route("/run_clocks", methods=["GET", "POST"])
def run_clocks():
    if request.method == "POST": # If user uploaded a file
        try:
            file = request.files["betas_file"] # The uploaded file
            selected_clocks = request.form.getlist("clock_name") # The list of clock name(s) selected

            # Generate a random ID and temporary folder for the job
            job_id = generate_id(20)
            job_folder = f"./data/temp/{job_id}"
            os.makedirs(job_folder, exist_ok=True)

            # Save the uploaded file into temp folder
            csv_path = os.path.join(job_folder, "data.csv")
            file.save(csv_path)
            
            # Save clock selection to a file
            with open(os.path.join(job_folder, "clocks.txt"), "w") as f:
                f.write(",".join(selected_clocks))
            
            # Start process in background
            subprocess.Popen(["nohup",
                              "python3",
                              "run_clocks.py",
                              job_id],
                              stdout=open(os.path.join(job_folder, "log.txt"), "w"),
               stderr=subprocess.STDOUT)

            # Redirect to results page
            return redirect(f"/clock/results/{job_id}")
        
        # Error handling
        except Exception as e:
            flash(f"Error: {str(e)}")
            return redirect(request.url)

    # If page was just accessed via GET, not POST, just show upload page
    return render_template("run_clocks.html")

# Clock results
@app.route("/clock/results/<job_id>")
def clock_results(job_id):
    # Define the job folder and path to results file
    job_folder = f"./data/temp/{job_id}"
    results_file = os.path.join(job_folder, "results.csv")

    # If results don't exist yet, return holding page with refresh
    if not os.path.exists(results_file):
        return render_template("holding_page.html", job_id=job_id)
    
    # Read selected clocks
    clocks_path = os.path.join(job_folder, "clocks.txt")
    selected_clocks = []
    if os.path.exists(clocks_path):
        with open(clocks_path, "r") as f:
            selected_clocks = f.read().strip().split(",")

    # Load results.csv into DataFrame
    df = pd.read_csv(results_file)

    # Convert to nested dictionary format expected by the template
    # (sample, {clock: age})
    all_results = []
    for _, row in df.iterrows():
        sample = row["Sample"]
        age_data = row.drop("Sample").to_dict()
        all_results.append((sample, age_data))

    # Return results page
    return render_template("run_clocks.html",
                           selected_clocks=selected_clocks,
                           all_results=all_results,
                           methyAge_name_map=methyAge_name_map)


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


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, threaded=False)