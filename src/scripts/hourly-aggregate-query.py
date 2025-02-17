#!/usr/bin/env python3

import sqlite3
import yaml
##############################################################################
# Load configuration
with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

# Database path from config
database_path = config["database"]["path"]
debug = config["debug"]

if debug == True:
    print("Debug: ", debug)
    print("Database file: ", database_path)

##############################################################################
# Query to clear the aggregation table before inserting new data
clear_table_query = "DELETE FROM price_and_demand_aggregation;"

# Query to aggregate data into hourly bins and insert into aggregation table
aggregation_query = """
INSERT INTO price_and_demand_aggregation (REGION, HOUR, COUNT, AVG_DEMAND, MIN_DEMAND, MAX_DEMAND, AVG_RRP, MIN_RRP, MAX_RRP, SUM_RRP, SUM_RRP_SQUARED, SUM_DEMAND, SUM_DEMAND_SQUARED)
SELECT REGION,
       strftime('00-00-0000 %H:00:00', SETTLEMENTDATE) AS HOUR,
       COUNT(*) AS COUNT,
       AVG(TOTALDEMAND) AS AVG_DEMAND,
       MIN(TOTALDEMAND) AS MIN_DEMAND,
       MAX(TOTALDEMAND) AS MAX_DEMAND,
       AVG(RRP) AS AVG_RRP,
       MIN(RRP) AS MIN_RRP,
       MAX(RRP) AS MAX_RRP,
       SUM(RRP) AS SUM_RRP,
       SUM(RRP * RRP) AS SUM_RRP_SQUARED,
       SUM(TOTALDEMAND) AS SUM_DEMAND,
       SUM(TOTALDEMAND * TOTALDEMAND) AS SUM_DEMAND_SQUARED
FROM price_and_demand
GROUP BY REGION, HOUR
ORDER BY REGION, HOUR;
"""

# Connect to the SQLite database
conn = sqlite3.connect(database_path)
cursor = conn.cursor()

# Clear existing data in the aggregation table
if debug == True: print("price_and_demand_aggregation - clear")
cursor.execute(clear_table_query)
conn.commit()

# Execute the aggregation query
if debug == True: print("price_and_demand_aggregation - insert")
cursor.execute(aggregation_query)
conn.commit()

##############################################################################
print(f"Hourly aggregation data inserted into {database_path} successfully.")

# Close connection
conn.close()
