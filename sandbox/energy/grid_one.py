import pypsa
# import pandas as pd

# 1. Setup network
n = pypsa.Network()
n.set_snapshots(range(24))
n.add("Bus", "Main Grid")

# 2. Add Carriers (defining CO2 intensity in t/MWh)
n.add("Carrier", "wind", co2_emissions=0.0)
n.add("Carrier", "gas", co2_emissions=0.19) # Approximate t/MWh for CCGT

# 3. Add Load
n.add("Load", "Town", bus="Main Grid", p_set=50)

# 4. Add Renewable Generator (Wind)
wind_data = [0.8, 0.7, 0.4, 0.2, 0.1, 0.0, 0.0, 0.1, 0.5, 0.9, 1.0, 0.8] * 2
n.add("Generator", "Wind Park", bus="Main Grid", carrier="wind",
      p_nom=100, p_max_pu=wind_data, marginal_cost=5)

# 5. Add Fossil Backup (The "Insurance")
n.add("Generator", "Gas Turbine", bus="Main Grid", carrier="gas",
      p_nom=100, marginal_cost=100) # High operational cost

# 6. Add Battery Storage
n.add("StorageUnit", "Battery", bus="Main Grid",
      p_nom=50, max_hours=4,  # 50 MW / 200 MWh
      efficiency_store=0.95, efficiency_dispatch=0.95,
      marginal_cost=1)

# 7. Add a Global Constraint for CO2
# Limit total emissions for the 24h period to 50 tons
n.add("GlobalConstraint", "co2_limit",
      type="primary_energy",
      carrier_attribute="co2_emissions",
      sense="<=",
      constant=50.0)

# 8. Solve
n.optimize(solver_name='highs')

# 9. Analysis
print(f"Total CO2 Emissions: {n.generators_t.p['Gas Turbine'].sum() * 0.19:.2f} tons")
print(f"Wind share: {n.generators_t.p['Wind Park'].sum() / (n.loads.p_set['Town'] * len(n.snapshots)) * 100:.1f}%")

# How much did the battery actually help?
print()
print(n.storage_units_t.state_of_charge)

# What was the "market price" at each hour?
print()
print(n.buses_t.marginal_price)

# Did we hit the CO2 wall?
print()
print(n.global_constraints.loc["co2_limit", "mu"]) # Shadow price of CO2
