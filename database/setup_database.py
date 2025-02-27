#!/usr/bin/env python3
from pymongo import MongoClient

def main():
    # Set up the database connection

    client = MongoClient("mongo.db//localhost:27017")
    db = client.webbase_database

    # Create a collection for the clocks called "clocks"
    global clocks
    clocks = db.clocks_collection

    # Remove everything so we're starting fresh
    clocks.delete_many({})

if __name__ == "__main__":
    main()
