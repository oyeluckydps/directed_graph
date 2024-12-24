from dash import register_page, html, dcc

register_page(__name__, path='/')

layout = html.Div([
    html.H1('Graph Visualization Tool', style={'textAlign': 'center', 'marginTop': '50px'}),
    html.Div([
        dcc.Link(
            html.Button('EXPLORE', style={'fontSize': '20px', 'padding': '10px 20px'}),
            href='/explore'
        ),
        dcc.Link(
            html.Button('MANUAL', style={'fontSize': '20px', 'padding': '10px 20px'}),
            href='/manual'
        )
    ], style={
        'display': 'flex',
        'justifyContent': 'center',
        'gap': '20px',
        'marginTop': '50px'
    })
])