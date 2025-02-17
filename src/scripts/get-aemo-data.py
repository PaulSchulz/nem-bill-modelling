#!/usr/bin/python

import os
import subprocess
from datetime import datetime
import yaml

##############################################################################
# Load configuration
with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)
# Read Configuration
debug      = config["debug"]
data_year  = config["data"]["year"]
data_path  = config["data"]["path"]
# db_path   = config["database"]["path"]

if debug == True:
    print("Debug: ", debug)
    print("Data year: ",      data_year)
    print("Data directory: ", data_path)

##############################################################################
# Define states and months
states = ["NSW1", "QLD1", "VIC1", "SA1", "TAS1"]

# Generate a list of months in YYYYMM format
months = [f"{data_year}{str(month).zfill(2)}" for month in range(1, 13)]

# Base URL
base_url = "https://aemo.com.au/aemo/data/nem/priceanddemand"

# Output directory
os.makedirs(data_path, exist_ok=True)

# Iterate through states and months and download files
for state in states:
             for month in months:
                          file_name = f"PRICE_AND_DEMAND_{month}_{state}.csv"
                          url = f"{base_url}/{file_name}"
                          output_path = os.path.join(data_path, file_name)

                          # Use wget to download the file
                          try:
                                       print(f"Downloading {url}...")
                                       subprocess.run(["wget", "-q", "-O", output_path, url], check=True)
                                       print(f"Downloaded: {output_path}")
                          except subprocess.CalledProcessError:
                                       print(f"Failed to download {url}")
