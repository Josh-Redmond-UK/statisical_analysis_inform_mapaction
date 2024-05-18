import pandas as pd
from src.utils import generate_plots, parse_data


# Load the data
data = parse_data()

# Define the columns for each type exclusing the index name
natural_columns = ['Earthquake',	'River Flood',	'Tsunami',	'Tropical Cyclone',	'Coastal flood',	'Drought',	'Epidemic']
human_columns = ['Projected Conflict Risk',	'Current Highly Violent Conflict Intensity']
hazard_exposure = natural_columns + human_columns

 
socio_economic_vulnerability = ['Development & Deprivation', 'Inequality', 'Economic Dependency']
vulnerable_groups = ['Uprooted people',	'Health Conditions',	'Children U5',	'Recent Shocks',	'Food Security',	'Other Vulnerable Groups']
vulnerability_columns = socio_economic_vulnerability + vulnerable_groups

lack_capacity_infrastructure =['Communication', 'Physical infrastructure', 'Access to health care']
institutional = ['Governance', 'DRR']
coping_capacity = lack_capacity_infrastructure + institutional

total = hazard_exposure + vulnerability_columns + coping_capacity

# Create dictionary of plot title and columns to plot
plots_dict = {
            "Hazard Exposure": hazard_exposure, 
            "Human":human_columns,
            "Natural":natural_columns,
            "Vulnerability": vulnerability_columns,
            "Socio-Economic Vulnerability": socio_economic_vulnerability,
            "Vulnerable Groups": vulnerable_groups,
            "Institutional": institutional,
            "Capacity Infrastructure": lack_capacity_infrastructure,
            "Coping Capacity": coping_capacity, 
            "All Variables":total}

# Draw the plots
for title, cols in plots_dict.items():
    try:
        generate_plots(data, cols, title, n_components=2, out_folder="outputs_national")
    except Exception as e:
        print(f"Error generating plots for {title}")
        print(e)
        pass

