from dash import Dash
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.express as px
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from plotly.subplots import make_subplots


timespan = np.linspace(0, 8, 100)

def f(x: float) -> float:
    if x >= 1.0 and x < 1.5:
        return 2 * x - 2
    elif x >= 1.5 and x < 4.5:
        return 1
    elif x >= 4.5 and x < 5.0:
        return -2 * x + 10.0
    return 0.0

def gen_noise(lower_limit=-0.1, upper_limit=0.1) -> float:
    return np.random.normal(lower_limit,upper_limit,1)[0]

def hamming_window(x,window_len=10):
    s = np.r_[x[window_len-1:0:-1],x,x[-2:-window_len-1:-1]]
    w = np.hamming(window_len)
    y = np.convolve(w/w.sum(),s,mode='valid')
    return y[:len(timespan)]


signal = [f(t) for t in timespan]
noise = [gen_noise() for t in timespan]
noisy_signal = [s + n for s,n in zip(signal, noise)]
conv_window = hamming_window(noisy_signal, window_len=15)
hamming_filter = np.hamming(len(timespan))


def hamming_convolution_dashboard(server):
    """Create a Plotly Dash dashboard."""

    fig = make_subplots(rows=1, cols=2, start_cell="bottom-left")

    fig.add_trace(go.Scatter(x=timespan, y=hamming_filter),
                  row=1, col=1)

    fig.add_trace(go.Scatter(x=timespan, y=conv_window),
                  row=1, col=2)
                  
    fig.add_trace(go.Scatter(x=timespan, y=noisy_signal),
                  row=1, col=2)

    fig.update_layout(showlegend=False,
                      xaxis_title="",
                      yaxis_title="",
                      margin=dict(l=0, r=0, t=35, b=35))

    dash_app = Dash(
        server=server,
        routes_pathname_prefix='/dashapp_conv/'
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

def signal_noise_dashboard(server):
    """Create a Plotly Dash dashboard."""

    fig = make_subplots(rows=1, cols=3, start_cell="bottom-left")

    fig.add_trace(go.Scatter(x=timespan, y=signal),
                  row=1, col=1)

    fig.add_trace(go.Scatter(x=timespan, y=noise),
                  row=1, col=2)

    fig.add_trace(go.Scatter(x=timespan, y=noisy_signal),
                  row=1, col=3)

    fig.update_layout(showlegend=False,
                      xaxis_title="",
                      yaxis_title="",
                      margin=dict(l=0, r=0, t=35, b=35))

    dash_app = Dash(
        server=server,
        routes_pathname_prefix='/dashapp_noise/'
        # external_stylesheets=['../static/css/dash_table.css']
    )

    # Create Dash Layout
    dash_app.layout = html.Div([
        html.Div([
            dcc.Graph(id='signal_plot', figure=fig)
        ]),
    ],
    style={'backgroundColor': '#ffffff'},
    )

    return dash_app.server
