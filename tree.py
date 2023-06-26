import json
import matplotlib.pyplot as plt
import networkx as nx

# Load the JSON file
with open('structures.json', 'r') as f:
    data = json.load(f)

# Create a directed graph
G = nx.DiGraph()

# Add nodes to the graph
for item in data:
    G.add_node(item['id'], color=tuple(item['rgb_triplet']), label=item['name'])

# Add edges to the graph
for item in data:cd
    for i in range(len(item['structure_id_path']) - 1):
        G.add_edge(item['structure_id_path'][i], item['structure_id_path'][i+1])

# Draw the graph
plt.figure(figsize=(10, 10))
pos = nx.spring_layout(G)
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_nodes(G, pos, node_color=[G.nodes[n]['color'] for n in G.nodes])
plt.show()
