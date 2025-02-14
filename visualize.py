import pickle
from pathlib import Path
import dash
from dash import html, dcc, callback, Output, Input, State, page_registry, page_container
import dash_cytoscape as cyto
import pandas as pd
import networkx as nx
import json
from ast import literal_eval

app = dash.Dash(__name__, use_pages=True)

# Shared stylesheet for consistent graph appearance
graph_stylesheet = [
    {
        'selector': 'node',
        'style': {
            'content': 'data(label)',
            'background-color': '#007bff',
            'width': 60,
            'height': 60,
            'color': 'white',
            'font-size': 20,
            'text-valign': 'center',
            'text-halign': 'center'
        }
    },
    {
        'selector': 'edge',
        'style': {
            'width': 4,
            'line-color': '#555',
            'target-arrow-color': '#555',
            'target-arrow-shape': 'triangle',
            'arrow-scale': 3,
            'curve-style': 'bezier'
        }
    }
]

# Home page (index.py)
app.layout = html.Div([
    page_container
])

# Function to generate graph elements (shared between pages)
def generate_elements_from_graph(G):
    try:
        pos = nx.spring_layout(G, seed=42) if len(G.nodes) > 0 else {}
        elements = [
            {
                'data': {'id': str(node), 'label': str(node)},
                'position': {'x': pos[node][0] * 500, 'y': pos[node][1] * 500}
            }
            for node in G.nodes
        ] + [
            {'data': {'source': str(edge[0]), 'target': str(edge[1])}}
            for edge in G.edges
        ]
        return elements
    except Exception as e:
        print(f"Error constructing graph: {e}")
        return []

# Pages directory
import pages

if __name__ == '__main__':
    app.run_server(debug=True)
