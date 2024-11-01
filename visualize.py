import pickle
from pathlib import Path

import dash
from dash import html
import dash_cytoscape as cyto
import networkx as nx

# Initialize Dash app
app = dash.Dash(__name__)

# Create directed graph
G = nx.DiGraph()
# G.add_edges_from([
#     (1, 2), (1, 3), (2, 4), (3, 4), (4, 5), (5, 6),
#     (5, 7), (6, 8), (7, 8), (8, 1), (3, 6), (2, 7)
# ])

# Load all primes
filename = 'optimized_isomorphic_hash'
with open(Path(filename + 'CDG._pickle'), 'rb') as inp:
    cdg = pickle.load(inp)

# Use NetworkX to compute a layout that reduces edge crossing
pos = nx.spring_layout(G, seed=42)  # Deterministic layout using seed

# Convert NetworkX graph to Cytoscape elements
elements = []
for node, p in pos.items():
    elements.append({'data': {'id': str(node), 'label': str(node)}, 'position': {'x': p[0]*500, 'y': p[1]*500}})
for edge in G.edges:
    elements.append({'data': {'source': str(edge[0]), 'target': str(edge[1])}})

app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape',
        layout={'name': 'preset'},  # Use 'preset' to allow dragging
        style={'width': '100%', 'height': '600px'},
        elements=elements,
        stylesheet=[
            # Styling for the nodes
            {
                'selector': 'node',
                'style': {
                    'width': '20px',
                    'height': '20px',
                    'content': 'data(label)',
                    'background-color': 'skyblue'
                }
            },
            # Styling for the edges
            {
                'selector': 'edge',
                'style': {
                    'line-color': 'gray',
                    'width': 2,
                    'target-arrow-color': 'gray',
                    'target-arrow-shape': 'triangle',  # Makes edges directed
                    'curve-style': 'bezier'  # Curved edges for better appearance
                }
            }
        ]
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)