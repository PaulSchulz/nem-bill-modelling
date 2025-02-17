#!/usr/bin/env python3

import os
import sqlite3
import yaml
import csv
from datetime import datetime

##############################################################################
# Load configuration
with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)
# Read Configuration
debug     = config["debug"]
input_dir = config["data"]["path"]
db_path   = config["database"]["path"]

if debug == True:
    print("Debug: ", debug)
    print("Input data directory: ", input_dir)
    print("Database file: ", db_path)

##############################################################################
# Database table name and schema
table_name = "price_and_demand"
schema = """
CREATE TABLE IF NOT EXISTS price_and_demand (
    REGION TEXT,
    SETTLEMENTDATE TEXT,
    TOTALDEMAND REAL,
    RRP REAL,
    PERIODTYPE TEXT
);
"""

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create the table
cursor.execute(schema)
conn.commit()

# Function to transform date format
def transform_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y/%m/%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return date_str  # Return as-is if conversion fails

# Iterate through all CSV files in the input directory
for file_name in os.listdir(input_dir):
    if file_name.endswith(".csv"):
        file_path = os.path.join(input_dir, file_name)
        print(f"Processing file: {file_name}")

        with open(file_path, "r") as csv_file:
            csv_reader = csv.reader(csv_file)

            # Skip the header row
            next(csv_reader, None)

            # Insert transformed rows into the database
            rows = [(row[0], transform_date(row[1]), row[2], row[3], row[4]) for row in csv_reader]
            cursor.executemany(f"INSERT INTO {table_name} (REGION, SETTLEMENTDATE, TOTALDEMAND, RRP, PERIODTYPE) VALUES (?, ?, ?, ?, ?)", rows)

# Commit changes and close the connection
conn.commit()
conn.close()

print("All files have been merged into the SQLite database with transformed dates.")
