from dash import register_page, html, dcc, callback, Output, Input, State
import dash_cytoscape as cyto
import networkx as nx
from ast import literal_eval
from utils import graph_stylesheet, generate_elements_from_graph

register_page(__name__, path='/manual')

layout = html.Div([
    dcc.Link(
        html.Button('HOME', style={'position': 'absolute', 'top': '10px', 'left': '10px'}),
        href='/'
    ),
    html.Div([
        html.H2('Enter Adjacent Graph', style={'textAlign': 'center'}),
        dcc.Textarea(
            id='graph-input',
            placeholder='Enter adjacent graph in format {0: [1, 2], 1: [2], 2: []}',
            style={'width': '100%', 'height': 100}
        ),
        html.Button('Submit', id='manual-submit', n_clicks=0, 
                   style={'marginTop': '10px', 'display': 'block', 'margin': '10px auto'})
    ], style={'width': '80%', 'margin': '20px auto'}),
    cyto.Cytoscape(
        id='cytoscape-graph-manual',
        layout={'name': 'preset'},
        style={'width': '100%', 'height': '600px'},
        stylesheet=graph_stylesheet
    )
])

@callback(
    Output('cytoscape-graph-manual', 'elements'),
    Input('manual-submit', 'n_clicks'),
    State('graph-input', 'value')
)
def update_manual_graph(n_clicks, input_value):
    if n_clicks == 0 or not input_value:
        return []
    
    try:
        # Convert string input to dictionary
        adj_list = literal_eval(input_value)
        G = nx.DiGraph(adj_list)
        return generate_elements_from_graph(G)
    except Exception as e:
        print(f"Error parsing graph input: {e}")
        return []
