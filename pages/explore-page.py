from dash import register_page, html, dcc, callback, Output, Input, State, ctx
import dash_cytoscape as cyto
import pickle
from pathlib import Path
import pandas as pd
import networkx as nx
from utils import graph_stylesheet, generate_elements_from_graph

register_page(__name__, path='/explore')

# Load DataFrame
filename = 'optimized_isomorphic_hash'
with open(Path(filename + 'CDG._pickle'), 'rb') as inp:
    cdg = pickle.load(inp)
df = pd.DataFrame(cdg.df)

current_index = 0

layout = html.Div([
    dcc.Link(
        html.Button('HOME', style={'position': 'absolute', 'top': '10px', 'left': '10px'}),
        href='/'
    ),
    html.Div(id='graph-info', style={'textAlign': 'center', 'margin': '10px'}),
    cyto.Cytoscape(
        id='cytoscape-graph-explore',
        layout={'name': 'preset'},
        style={'width': '100%', 'height': '600px'},
        stylesheet=graph_stylesheet
    ),
    html.Div([
        html.Button('Left', id='left-button', n_clicks=0),
        html.Button('Right', id='right-button', n_clicks=0),
        dcc.Input(id='row-input', type='number', min=1, max=len(df), value=1, style={'margin-left': '20px'}),
        html.Button('Submit', id='submit-button', n_clicks=0)
    ], style={'display': 'flex', 'justifyContent': 'center', 'margin': '20px'})
])

@callback(
    [Output('cytoscape-graph-explore', 'elements'),
     Output('graph-info', 'children')],
    [Input('left-button', 'n_clicks'),
     Input('right-button', 'n_clicks'),
     Input('submit-button', 'n_clicks')],
    State('row-input', 'value')
)
def update_graph(left_clicks, right_clicks, submit_clicks, row_input):
    global current_index, df

    if not ctx.triggered:
        button_id = 'initial'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'left-button' and current_index > 0:
        current_index -= 1
    elif button_id == 'right-button' and current_index < len(df) - 1:
        current_index += 1
    elif button_id == 'submit-button':
        if row_input is not None and 1 <= row_input <= len(df):
            current_index = row_input - 1

    row = df.iloc[current_index]
    elements = generate_elements_from_graph(nx.DiGraph(row['adj_']))
    info_text = f"Row {current_index + 1}/{len(df)} - Nodes: {row['number_of_nodes']} Edges: {row['number_of_edges']}"

    return elements, info_text