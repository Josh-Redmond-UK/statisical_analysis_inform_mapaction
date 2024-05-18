import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import os


    

def parse_data(path='data/INFORM_Risk_2024_v067.xlsx', sheet_name='INFORM Risk 2024 (a-z)'):

    data = pd.read_excel(path, sheet_name=sheet_name, header=1)

    data = data.iloc[1:]

    #Replace missing values with 0
    data.replace({'x': 0}, regex=True, inplace=True)
    
    return data


                

def create_pca_plots(data, cols, title, n_components=2, out_folder="outputs", risk_column_name='INFORM RISK'):
    to_keep = cols + [risk_column_name]
    data = data[to_keep]

    data.dropna(how='any', axis=0, inplace=True)

    inform_risk = data[risk_column_name]
    data = data[cols]
    pca = PCA(n_components=min(n_components, len(data.columns)))
    pca.fit(data)
    evr = pca.explained_variance_ratio_[:2]
    top_1 = np.argmax(evr)
    top_comp_explains = round(evr[top_1], 2)
    comps = pca.components_[0:2]

    arrow_d = np.transpose(comps)



    top_1_comp = abs(comps)[top_1]
    feat_importance_frame = pd.DataFrame(top_1_comp, index=cols, columns=['Importance'])
    feat_importance_frame.to_csv(f'{out_folder}/'+title +  " top 1 component explains " f'{top_comp_explains} variance feature importance.csv')

    components = np.array(pca.transform(data))
    components[:,0] *= 1.0/(components[:,0].max() - components[:,0].min())
    components[:,1] *= 1.0/(components[:,1].max() - components[:,1].min())

    fig = plt.figure(figsize = (12,12))
    plt.xlabel('Principal Component 1', fontsize = 15)
    plt.ylabel('Principal Component 2', fontsize = 15)
    plt.title(f'Top 2 components of {n_components} component PCA', fontsize = 20)
    sc = plt.scatter(components[:,0], components[:,1], c=inform_risk)
    cbar = plt.colorbar(sc)
    cbar.set_label("INFORM RISK", fontsize = 15)

    for i in range(len(cols)):
        plt.arrow(0, 0, arrow_d[i,0], arrow_d[i,1], color = 'r', alpha = 0.5, head_width = 0.025, head_length = 0.01)
        plt.text(arrow_d[i,0], arrow_d[i,1], cols[i], color = 'black', ha = 'center', va = 'center')

    plt.savefig(f'{out_folder}/'+title + 'PCA.png')


def create_correlation_plots(data, cols, title, out_folder="outputs"):
    data = data[cols]
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
    plt.savefig(f'{out_folder}/'+title + '.png')
    correlations_frame.to_csv(f'{out_folder}/'+title + '.csv')

def generate_plots(data, cols, title, n_components=2, out_folder="outputs", risk_column_name="INFORM RISK"):
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
       
    create_correlation_plots(data, cols, title, out_folder)
    create_pca_plots(data, cols, title, n_components, out_folder, risk_column_name)

