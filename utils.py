import networkx as nx
import pathlib
import ast
import pprint
import time
from contextlib import contextmanager

def read_data(filename):
    text_on_file = pathlib.Path(filename).read_text()
    return ast.literal_eval(text_on_file)

def save_data(data, filename, mode = 'w'):
    with open(pathlib.Path(filename), mode=mode) as f:
        pprint.pprint(data, f)


@contextmanager
def time_block(label):
    """Context manager to time a specific block of code."""
    start_time = time.time()
    yield
    end_time = time.time()
    time_taken = end_time - start_time
    if label not in time_block.timings:
        time_block.timings[label] = []
    time_block.timings[label].append(time_taken)

time_block.timings = {}

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