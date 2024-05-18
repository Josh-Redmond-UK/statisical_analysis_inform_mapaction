import pandas as pd
from src.utils import generate_plots, parse_data


# Load the data
data = parse_data('data/INFORM_LAC_2020_v007_Eng.xlsx', 'LAC INFORM 2020')

# Define the columns for each type exclusing the index name
natural_columns = ['Earthquake and Tsunami',	'Flood',	'Tropical Cyclone',	'Environmental degradation and drought',	'Epidemics']
human_columns = ['Conflict', 'Violence', 'Asylum seekers ' ]
hazard_exposure = natural_columns + human_columns

 
socio_economic_vulnerability = ['Development & Deprivation',	'Inequality', 'Dependency']
vulnerable_groups = ['Uprooted people',	'Health Conditions',	'Nutrtion and health conditions of children U5',	'Unprotected youth',	'Recent Shocks', 'Food Security', 'Other Vulnerable Groups']
vulnerability_columns = socio_economic_vulnerability + vulnerable_groups

lack_capacity_infrastructure =['DRR implementation',	'Governance', 'Social protection',	'Security and violence containment']
institutional = ['Communication', 'Physical connectivity',	'Access to health care'	,'Access to education']
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
        generate_plots(data, cols, title, n_components=2, out_folder="outputs_latam")
    except Exception as e:
        print(f"Error generating plots for {title}")
        print(e)
        pass

