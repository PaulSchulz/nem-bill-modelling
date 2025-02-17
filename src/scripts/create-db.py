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
debug         = config["debug"]
database_path = config["database"]["path"]

if debug == True: print("Debug: ", debug)
if debug == True: print("Database file: ", database_path)

##############################################################################
# Connect to the SQLite database
conn = sqlite3.connect(database_path)
cursor = conn.cursor()

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

# Create the table
if debug == True: print("price_and_demand - create")
cursor.execute(schema)
conn.commit()

##############################################################################
# Create or update the aggregation table
table_name = "price_and_demand_aggregation"
schema = """
CREATE TABLE IF NOT EXISTS price_and_demand_aggregation (
    REGION TEXT,
    HOUR TEXT,
    COUNT INTEGER,
    AVG_DEMAND REAL,
    MIN_DEMAND REAL,
    MAX_DEMAND REAL,
    AVG_RRP REAL,
    MIN_RRP REAL,
    MAX_RRP REAL,
    SUM_RRP REAL,
    SUM_RRP_SQUARED REAL,
    SUM_DEMAND REAL,
    SUM_DEMAND_SQUARED REAL
);
"""

# Create the table
if debug == True: print("price_and_demand_aggregation - create")
cursor.execute(schema)
conn.commit()

##############################################################################
# Database table name and schema
table_name = "simulated_bills"
schema = """
CREATE TABLE IF NOT EXISTS simulated_bills (
    region      TEXT,
    start_date  TEXT,
    end_date    TEXT,
    tariff_name TEXT,
    total_cost  TEXT,
    record_num  INTEGER
);
"""

# Create the table
if debug == True: print("simulated_bills - create")
cursor.execute(schema)
conn.commit()
