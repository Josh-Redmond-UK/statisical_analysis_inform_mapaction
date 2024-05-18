import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# Load the data

def parse_data(path):

    data = pd.read_excel('data/INFORM_Risk_2024_v067.xlsx', sheet_name='INFORM Risk 2024 (a-z)', header=1)

    data = data.iloc[1:]

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
    
def create_pca_plots(correlations, cols, title):
    pca = PCA(n_components=2)
    pca.fit(correlations)
    evr = pca.explained_variance_ratio_
    top_1 = np.argmax(evr)
    top_comp_explains = round(evr[top_1], 2)
    comps = (abs( pca.components_ ))
    top_1_comp = comps[top_1]
    feat_importance_frame = pd.DataFrame(top_1_comp, index=cols, columns=['Importance'])
    feat_importance_frame.to_csv('outputs/'+title +  " top 1 component explains " f'{top_comp_explains} variance feature importance.csv')

    components = np.array(pca.transform(correlations))
    fig = plt.figure(figsize = (12,12))


    plt.xlabel('Principal Component 1', fontsize = 15)
    plt.ylabel('Principal Component 2', fontsize = 15)
    plt.title('2 component PCA', fontsize = 20)
    sc = plt.scatter(components[:,0], components[:,1], c=data['INFORM RISK'])
    cbar = plt.colorbar(sc)
    cbar.set_label("INFORM RISK", fontsize = 15)
    plt.savefig('outputs/'+title + 'PCA.png')






def plot_correlation_df(df, cols, title):
    data = df[cols]
    data.replace({'x': 0}, regex=True, inplace=True)
    correlations_frame = data.corr()
    correlations = np.array(correlations_frame)
    fig, ax = plt.subplots(figsize=(12, 12))
    im = ax.imshow(correlations)
    ax.set_xticks(np.arange(len(cols)), labels=cols)
    ax.set_yticks(np.arange(len(cols)), labels=cols)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")
    # Loop over data dimensions and create text annotations.
    for i in range(len(cols)):
        for j in range(len(cols)):
            text = ax.text(j, i, round(correlations[i, j], 2),
                        ha="center", va="center", color="w")

    ax.set_title(title)
    plt.colorbar(im)
    fig.tight_layout()
    plt.savefig('outputs/'+title + '.png')
    correlations_frame.to_csv('outputs/'+title + '.csv')

    # PCA Analysis
    create_pca_plots(data, cols, title)


plots_dict = {"Hazard Exposure": hazard_exposure, "Vulnerability": vulnerability_columns, "Coping Capacity": coping_capacity, "All Variables":total}

for title, cols in plots_dict.items():
    plot_correlation_df(data, cols, title)

