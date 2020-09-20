from dash import Dash
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.express as px
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from plotly.subplots import make_subplots


timespan = np.linspace(0, 10, 50)

def gen_noise(lower_limit=-0.1, upper_limit=0.1) -> float:
    return np.abs(np.random.normal(lower_limit,upper_limit,1)[0])

investments = [gen_noise(0.0, 10000.0) for t in timespan]
# investments = [0.0, 0.0, 0.0, 500.0, 250.0, 100.0, 0.0, 0.0, 1000.0, 750.0, 200.0, 0.0, 0.0, 0.0]
purchases = [
    investments[t] * np.abs(np.random.normal(1.0, 1.2, 1)[0])
    for t in range(len(timespan))
]
# purchases_shifted = [gen_noise(0.0, 10000.0) for _ in range(10)]
# purchases_shifted.extend(purchases[10:])

def cross_correlation_dashboard(server):
    """Create a Plotly Dash dashboard."""

    fig = make_subplots(rows=1, cols=2, start_cell="bottom-left")

    fig.add_trace(go.Scatter(x=timespan[10:40], y=investments[10:40],
                             line_color="#23b2ea"),
                  row=1, col=1)

    fig.add_trace(go.Scatter(x=timespan[10:40], y=purchases[0:30],
                             line_color="#f77d20"),
                  row=1, col=1)

    fig.update_yaxes(range=[-1000.0,int(np.max(purchases) * 1.1)], row=1, col=1)

    fig.add_trace(go.Scatter(x=timespan[10:40], y=investments[10:40],
                             line_color="#23b2ea"),
                  row=1, col=2)

    fig.add_trace(go.Scatter(x=timespan[10:40], y=purchases[10:40],
                             line_color="#f77d20"),
                  row=1, col=2)

    fig.update_yaxes(range=[-1000.0,int(np.max(purchases) * 1.1)], row=1, col=2)

    fig.update_layout(showlegend=False,
                      xaxis_title="",
                      yaxis_title="",
                      margin=dict(l=0, r=0, t=35, b=35))

    dash_app = Dash(
        server=server,
        routes_pathname_prefix='/dashapp_corr/'
        # external_stylesheets=['../static/css/dash_table.css']
    )

    # Create Dash Layout
    dash_app.layout = html.Div([
        html.Div([
            dcc.Graph(id='conv_plot', figure=fig)
        ]),
    ],
    style={'backgroundColor': '#ffffff'},
    )

    return dash_app.server
