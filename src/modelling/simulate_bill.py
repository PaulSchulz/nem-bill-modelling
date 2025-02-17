import yaml
import sqlite3
import tariffs
from datetime import datetime

##############################################################################
# Load configuration
with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)
# Read Configuration
debug         = config["debug"]
database_path = config["database"]["path"]

# db_path   = config["database"]["path"]

if debug == True: print("Debug: ", debug)
if debug == True: print("Database file: ", database_path)

region = "SA1"
if debug == True: print("region: ", region)

##############################################################################

def calculate_bill(region, start_date, end_date, tariff_function, tariff_name, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = """
    SELECT REGION, SETTLEMENTDATE, TOTALDEMAND
    FROM price_and_demand
    WHERE REGION = ? AND SETTLEMENTDATE BETWEEN ? AND ?
    """
    cursor.execute(query, (region, start_date, end_date))
    records = cursor.fetchall()

    total_cost = 0.0
    record_num = 0;
    for record in records:
        energy_kwh = 0.5
        region, timestamp, demand = record
        total_cost += tariff_function(energy_kwh, timestamp)
        record_num += 1

    # Save results to database
    cursor.execute("""
        INSERT INTO simulated_bills (region, start_date, end_date, tariff_name, total_cost, record_num)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (region, start_date, end_date, tariff_name, total_cost, record_num))

    if debug == True: print("simulated_bills - insert")
    conn.commit()
    conn.close()

    # Generate text report
    report = f"""
    Simulated Electricity Bill
    --------------------------
    Region:      {region}
    Tariff Used: {tariff_name}
    Time Period: {start_date} to {end_date}
    Records:     {record_num}
    Total Bill: ${total_cost:.2f}
    """

    with open("simulated_bill.txt", "w") as f:
        f.write(report)

    print("Simulated bill generated: simulated_bill.txt")
    if debug == True: print(report)

# Example usage
if __name__ == "__main__":
    calculate_bill(region,
                   "2024-01-01 00:00:01",
                   "2025-01-01 00:00:01",
                   tariffs.time_of_use_tariff,
                   "Time-of-Use Tariff",
                   database_path)

    calculate_bill(region,
                   "2024-01-01 00:00:01",
                   "2025-01-01 00:00:01",
                   tariffs.flat_rate_tariff,
                   "Flat-Rate Tariff",
                   database_path)
