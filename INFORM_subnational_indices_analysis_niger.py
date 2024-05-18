import pandas as pd
from src.utils import generate_plots, parse_data


# Load the data
data = parse_data('data/INFORM_NIGER_2018_v2.1.xlsx', 'INFORM Niger 2018')

# Define the columns for each type exclusing the index name
natural_columns = ['Food Insecurity Probability',	'Physical exposure to flood',	'Environmental degradation and drought']
human_columns = ['Conflict intensity',	'Political violence',	'Security level']
hazard_exposure = natural_columns + human_columns

 
socio_economic_vulnerability = ['Development & Deprivation']
vulnerable_groups = ['Uprooted people',	'Health Conditions',	'Children U5',	'Malnutrition',	'Recent Shocks',	'Food Insecurity',	'People in Need',	'Other Vulnerable Groups']
vulnerability_columns = socio_economic_vulnerability + vulnerable_groups

lack_capacity_infrastructure =['DRR Implementation']
institutional = ['Communication', 'Physical infrastructure',	'Access to health care']
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
        generate_plots(data, cols, title, n_components=2, out_folder="outputs_niger", risk_column_name='RISK')
    except Exception as e:
        print(f"Error generating plots for {title}")
        print(e)
        pass


