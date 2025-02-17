import yaml
from datetime import datetime

# Load tariff configurations
def load_tariffs(config_file="tariffs.yaml"):
    with open(config_file, "r") as f:
        return yaml.safe_load(f)

TARIFFS = load_tariffs()

# Flat Rate Tariff
def flat_rate_tariff(energy_kwh, timestamp):
    rate = TARIFFS["flat_rate"]["price_per_kwh"]
    return energy_kwh * rate / 12.0

# Time-of-Use Tariff
def time_of_use_tariff(energy_kwh, timestamp):
    hour = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").hour
    if hour in TARIFFS["tou"]["peak_hours"]:
        rate = TARIFFS["tou"]["peak_price"]
    elif hour in TARIFFS["tou"]["shoulder_hours"]:
        rate = TARIFFS["tou"]["shoulder_price"]
    else:
        rate = TARIFFS["tou"]["off_peak_price"]
    return energy_kwh * rate / 12.0

# Demand Tariff (based on max demand)
def demand_tariff(energy_kwh, max_demand_kw):
    base_cost = energy_kwh * TARIFFS["demand"]["energy_price"] / 12.0
    demand_charge = max_demand_kw * TARIFFS["demand"]["demand_price_per_kw"]
    return base_cost + demand_charge

# Feed-in Tariff (for exported energy)
def feed_in_tariff(export_kwh):
    return export_kwh * TARIFFS["feed_in"]["price_per_kwh"] / 12.0
