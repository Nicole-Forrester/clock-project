#!/usr/bin/env python3
from pymongo import MongoClient
import pandas as pd
import numpy as np
from pathlib import Path
from urllib.parse import quote_plus
import json

def parse_data(filename):
    # Use pandas to load the csv file/excel spread sheet to a dataframe
    df = pd.read_csv(filename)
    print(df.head())

     # Replace NaN values with None (translates to null in MongoDB) to avoid parser errors in MongoDB
    df = df.replace({np.nan: None})

    # "Jsonify"/convert dataframe to a dict
    data = df.to_dict(orient = "records")
    print(data)

    # Return the new dictionary of records to add
    return data


def main():
    # Set up the database connection
    with open(Path(__file__).parent.parent / "configuration/conf.json") as infh:
        conf = json.loads(infh.read())

    print("Server",quote_plus(conf['server']['address']))
    print("Username",quote_plus(conf['server']['username']))
    print("Password",quote_plus(conf['server']['password']))

    client = MongoClient(
        conf['server']['address'],
        username = conf['server']['username'],
        password = conf['server']['password'],
        authSource = "clocks_database"
    )
    db = client.clocks_database

    # Create a collection for the clocks called "clocks"
    global clocks
    clocks = db.clocks_collection

    # Create a collection for the CpGs called "cpgs"
    global cpgs
    cpgs = db.cpgs_collection

    # Remove everything so we're starting fresh
    clocks.delete_many({})
    cpgs.delete_many({})

    # Add a test document into the collection
    # clocks.insert_one({ "name": "Hannum"})
    # cpgs.insert_one({ "clock" : "Hannum"})

    # Using the parse_data function above, put all records into mongodb
    db = client["clocks_database"]
    db.clocks_collection.insert_many(parse_data("data/clocks_with_stats.csv"))
    db.cpgs_collection.insert_many(parse_data("data/updated_clock_cpgs.csv"))

if __name__ == "__main__":
    main()
