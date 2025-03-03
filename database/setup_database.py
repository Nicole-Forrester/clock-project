#!/usr/bin/env python3
from pymongo import MongoClient
import pandas as pd

def parse_data(filename):
    # Use pandas to load the csv file/excel spread sheet to a dataframe
    df = pd.read_csv(filename)
    print(df.head())

    # "Jsonify"/convert dataframe to a dict
    data = df.to_dict(orient = "records")
    print(data)

    # Return the new dictionary of records to add
    return data



def main():
    # Set up the database connection

    client = MongoClient("mongodb://localhost:27017/")
    db = client.clocks_database

    # Create a collection for the clocks called "clocks"
    global clocks
    clocks = db.clocks_collection

    # Remove everything so we're starting fresh
    clocks.delete_many({})

    # Add a test document into the collection
    # clocks.insert_one({ "name": "Hannum"})

    # Using the parse_data function above, put all records into mongodb
    db = client["clocks_database"]
    db.clocks_collection.insert_many(parse_data("data/epigenetic_clocks.csv"))

if __name__ == "__main__":
    main()
