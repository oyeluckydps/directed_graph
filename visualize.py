import pickle
from pathlib import Path

import dash
from dash import html, dcc, callback, Output, Input, State
import dash_cytoscape as cyto
import pandas as pd
import networkx as nx
import json

# Load DataFrame
filename = 'optimized_isomorphic_hash'
with open(Path(filename + 'CDG._pickle'), 'rb') as inp:
    cdg = pickle.load(inp)

df = pd.DataFrame(cdg.df)

# Initialize Dash app
app = dash.Dash(__name__)


# Function to generate graph elements
def generate_elements_from_row(row):
    try:
        adj_list = row['adj_']
        G = nx.DiGraph(adj_list)
        pos = nx.spring_layout(G, seed=42) if len(G.nodes) > 0 else {}
        elements = [
                       {'data': {'id': str(node), 'label': str(node)},
                        'position': {'x': pos[node][0] * 500, 'y': pos[node][1] * 500}}
                       for node in G.nodes
                   ] + [
                       {'data': {'source': str(edge[0]), 'target': str(edge[1])}}
                       for edge in G.edges
                   ]
        return elements
    except Exception as e:
        print(f"Error constructing graph: {e}")
        return []


# Initial elements for the first graph in the DataFrame
initial_elements = generate_elements_from_row(df.iloc[0])

app.layout = html.Div([
    html.Div(id='graph-info', style={'textAlign': 'center', 'margin': '10px'}),
    cyto.Cytoscape(
        id='cytoscape-graph',
        elements=initial_elements,  # Load first graph initially
        layout={'name': 'preset'},
        style={'width': '100%', 'height': '600px'},
        stylesheet=[
            {'selector': 'node', 'style': {
                'content': 'data(label)',
                'background-color': '#007bff',
                'width': 60,
                'height': 60,
                'color': 'white',
                'font-size': 20,
                'text-valign': 'center',
                'text-halign': 'center'
            }},
            {'selector': 'edge', 'style': {
                'width': 4,
                'line-color': '#555',
                'target-arrow-color': '#555',
                'target-arrow-shape': 'triangle',
                'arrow-scale': 3,
                'curve-style': 'bezier'
            }}
        ]
    ),
    html.Div([
        html.Button('Left', id='left-button', n_clicks=0),
        html.Button('Right', id='right-button', n_clicks=0),
        dcc.Input(id='row-input', type='number', min=1, max=len(df), value=1, style={'margin-left': '20px'}),
        html.Button('Submit', id='submit-button', n_clicks=0)
    ], style={'display': 'flex', 'justifyContent': 'center', 'margin': '20px'})
])

current_index = 0


@app.callback(
    [Output('cytoscape-graph', 'elements'),
     Output('graph-info', 'children')],
    [Input('left-button', 'n_clicks'),
     Input('right-button', 'n_clicks'),
     Input('submit-button', 'n_clicks')],
    State('row-input', 'value')
)
def update_graph(left_clicks, right_clicks, submit_clicks, row_input):
    global current_index
    ctx = dash.callback_context

    if not ctx.triggered:
        return dash.no_update, dash.no_update
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'left-button' and current_index > 0:
        current_index -= 1
    elif button_id == 'right-button' and current_index < len(df) - 1:
        current_index += 1
    elif button_id == 'submit-button':
        if row_input is not None and 1 <= row_input <= len(df):
            current_index = row_input - 1

    row = df.iloc[current_index]
    elements = generate_elements_from_row(row)

    info_text = f"Row {current_index + 1}/{len(df)} - Nodes: {row['number_of_nodes']} Edges: {row['number_of_edges']}"

    return elements, info_text


if __name__ == '__main__':
    app.run_server(debug=True)