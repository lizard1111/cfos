import pandas as pd
import json
import numpy as np
import plotly.graph_objects as go

# Read both datasets
df1 = pd.read_csv('Fed.csv')
df2 = pd.read_csv('FastRefeed.csv')

# Rename the density column in both datasets for clarity
df1.rename(columns={'density (cells/mm^3)': 'density_Fed'}, inplace=True)
df2.rename(columns={'density (cells/mm^3)': 'density_FastRefeed'}, inplace=True)

# Merge the two datasets on 'acronym' column
df = pd.merge(df1, df2, on='acronym', how='outer')  # 'outer' ensures that all acronyms from both datasets are included

# Calculate the ratio
df['density_ratio'] = df['density_FastRefeed'] / df['density_Fed']

# Handle any potential division by zero or infinity
df['density_ratio'].replace([np.inf, -np.inf], np.nan, inplace=True)

# Load the JSON file
with open('structures.json', 'r') as f:
    data = json.load(f)

# Prepare data for the tree
labels = [item['acronym'] for item in data if item['acronym'] in df['acronym'].values]
parents = ['' if len(item['structure_id_path']) == 1 else next((i['acronym'] for i in data if i['id'] == item['structure_id_path'][-2])) for item in data if item['acronym'] in df['acronym'].values]

# Match acronyms with ratio values from the merged DataFrame
ratios = [df.loc[df['acronym'] == acronym, 'density_ratio'].iloc[0] for acronym in labels]

colors = ['rgb{}'.format(tuple(item['rgb_triplet'])) for item in data if item['acronym'] in df['acronym'].values]

# Create a Plotly figure
fig = go.Figure(go.Sunburst(
    labels=labels,
    parents=parents,
    values=ratios,
    marker=dict(colors=colors),
    hovertemplate='<b>%{label}</b><br>Density Ratio (FastRefeed/Fed): %{value}<extra></extra>',  # Customize hover text
))

fig.update_layout(
    margin=dict(t=0, l=0, r=0, b=0),  
    plot_bgcolor='black',
    paper_bgcolor='black'
)
fig.show()
