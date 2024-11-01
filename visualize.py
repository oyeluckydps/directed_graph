import dash
from dash import html, callback, Output, Input
import dash_cytoscape as cyto
import pandas as pd
import networkx as nx
import json

# Sample DataFrame
data = {
    'adj_': [
        json.dumps([(1, 2), (2, 3), (3, 1)]),  # Valid adjacency example
        json.dumps([(1, 2), (2, 3), (3, 4), (4, 1)]),  # Valid adjacency example
        json.dumps([(1, 2), (1, 3), (3, 4), (2, 4)])  # Valid adjacency example
    ],
    'number_of_nodes': [3, 4, 4],
    'number_of_edges': [3, 4, 4]
}

df = pd.DataFrame(data)

# Initialize Dash app
app = dash.Dash(__name__)

# Function to generate graph elements from a specific row
def generate_elements_from_row(row):
    try:
        adj_list = json.loads(row['adj_'])
        G = nx.DiGraph(adj_list)
        pos = nx.spring_layout(G, seed=42) if len(G.nodes) > 0 else {}
        elements = [
            {'data': {'id': str(node), 'label': str(node)}, 'position': {'x': pos[node][0] * 500, 'y': pos[node][1] * 500}}
            for node in G.nodes
        ] + [
            {'data': {'source': str(edge[0]), 'target': str(edge[1])}}
            for edge in G.edges
        ]
        return elements
    except Exception as e:
        print(f"Error constructing graph: {e}")
        return []

# Initialize elements to the first graph in the DataFrame
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
                'background-color': '#007bff',  # Strong blue for visibility
                'width': 60,  # Increased node size for emphasis
                'height': 60,
                'color': 'white',
                'font-size': 20,
                'text-valign': 'center',
                'text-halign': 'center'
            }},
            {'selector': 'edge', 'style': {
                'width': 4,  # Thicker edges for visibility
                'line-color': '#555',  # Darker gray for strong contrast
                'target-arrow-color': '#555',
                'target-arrow-shape': 'triangle',
                'arrow-scale': 3,  # Larger arrow size
                'curve-style': 'bezier'
            }}
        ]
    ),
    html.Div([
        html.Button('Left', id='left-button', n_clicks=0),
        html.Button('Right', id='right-button', n_clicks=0)
    ], style={'display': 'flex', 'justifyContent': 'center', 'margin': '20px'})
])

current_index = 0

@app.callback(
    [Output('cytoscape-graph', 'elements'),
     Output('graph-info', 'children')],
    [Input('left-button', 'n_clicks'),
     Input('right-button', 'n_clicks')]
)
def update_graph(left_clicks, right_clicks):
    global current_index
    ctx = dash.callback_context

    if not ctx.triggered:
        return dash.no_update, dash.no_update
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'left-button':
        current_index = max(0, current_index - 1)
    elif button_id == 'right-button':
        current_index = min(len(df) - 1, current_index + 1)

    row = df.iloc[current_index]
    elements = generate_elements_from_row(row)

    info_text = f"Row {current_index + 1}/{len(df)} - Nodes: {row['number_of_nodes']} Edges: {row['number_of_edges']}"

    return elements, info_text

if __name__ == '__main__':
    app.run_server(debug=True)