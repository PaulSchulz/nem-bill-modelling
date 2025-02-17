import tariffs

# Test data
energy_kwh = 10  # Example energy usage
timestamp = "2025-01-01 18:30:00"  # Peak hour example
max_demand_kw = 5  # Example demand peak
export_kwh = 2  # Example energy exported

# Test flat rate tariff
flat_cost = tariffs.flat_rate_tariff(energy_kwh)
print(f"Flat Rate Tariff Cost: ${flat_cost:.2f}")

# Test time-of-use tariff
tou_cost = tariffs.time_of_use_tariff(energy_kwh, timestamp)
print(f"Time-of-Use Tariff Cost: ${tou_cost:.2f}")

# Test demand tariff
demand_cost = tariffs.demand_tariff(energy_kwh, max_demand_kw)
print(f"Demand Tariff Cost: ${demand_cost:.2f}")

# Test feed-in tariff
feed_in_credit = tariffs.feed_in_tariff(export_kwh)
print(f"Feed-in Tariff Credit: ${feed_in_credit:.2f}")
