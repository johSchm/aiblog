from dash import Dash
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.express as px
import dash_core_components as dcc
from dash.dependencies import Input, Output, State


def f(x: float) -> float:
    if x >= 1.0 and x < 1.5:
        return 2 * x - 2
    elif x >= 1.5 and x < 4.5:
        return 1
    elif x >= 4.5 and x < 5.0:
        return -2 * x + 10.0
    return 0.0

def g(x: float) -> float:
    if x >= -5.0 and x < -4.5:
        return 2 * x + 10
    elif x >= -4.5 and x < -1.5:
        return 1
    elif x >= -1.5 and x < -1.0:
        return -2 * x - 2.0
    return 0.0

def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

center_f = 3
center_g = -3
timespan = np.linspace(-10, 10, 200)


def signal_kernel_dashboard(server):
    """Create a Plotly Dash dashboard."""

    df = pd.DataFrame(dict(t=timespan,
                           signal=[f(t) for t in timespan],
                           kernel=[gaussian(t, -3, 1.0) for t in timespan]))

    fig = px.line(df, x='t', y=['signal', 'kernel'])

    # app.run_server(mode='inline')

    dash_app = Dash(
        server=server,
        routes_pathname_prefix='/dashapp_signal_plot/'#,
        # external_stylesheets=[
        #     '/static/dist/css/styles.css',
        # ]
    )

    # Create Dash Layout
    dash_app.layout = html.Div([
        dcc.Graph(id = 'signal_kernel_plot', figure = fig),
    ])
    return dash_app.server


slider_smooth = 5
timespan_range_len = (abs(min(timespan)) + max(timespan))

c_total = np.convolve([f(t) for t in timespan],  # fixed
                      [g(t) for t in timespan])  # sliding
c_total /= sum([g(t) for t in timespan])
c_limit = int((abs(min(timespan)) + center_g) * (len(timespan) / timespan_range_len))
c_total = c_total[c_limit:c_limit+len(timespan)]


def convolution_dashboard(server):
    """Create a Plotly Dash dashboard."""

    timespan = np.linspace(-10, 10, 200)
    df = pd.DataFrame(dict(t=timespan,
                           signal=[f(t) for t in timespan],
                           kernel=[gaussian(t, -3, 1.0) for t in timespan]))

    fig = px.line(df, x='t', y=['signal', 'kernel'])

    # app.run_server(mode='inline')

    dash_app = Dash(
        server=server,
        routes_pathname_prefix='/dashapp_convolution/'#,
        # external_stylesheets=[
        #     '/static/dist/css/styles.css',
        # ]
    )

    # Create Dash Layout
    dash_app.layout = html.Div([

        dcc.Graph(id = 'conv_plot'),

        html.Div([
            html.Div([
                dcc.Slider(id = 'time_slider',
                           step = timespan_range_len / len(timespan),
                           min = min(timespan),
                           max = max(timespan),
                           value = center_g)],
                style={
                    'width': '80%',
                    'position': 'relative',
                    'padding': '0px 0px 0px 50px',
                    'top': '-35px',
                },
            ),
            html.Div([
                html.Button('PLAY',
                            id='play_btn',
                            n_clicks=0)],
                style={
                    'position': 'relative',
                    'top': '-80px',
                },
            )
        ]),

        dcc.Interval(id='interval_component',
                     interval=100, # in milliseconds
                     n_intervals=0)
    ],
    style={'backgroundColor': '#ffffff'},
    )

    def update_graphs(slider_value: float):
        f_arr = [f(t) for t in timespan]
        g_arr = [g(t-slider_value+center_g) for t in timespan]
        c_limit = int((abs(min(timespan)) + slider_value) * (len(timespan) / timespan_range_len))
        c_arr = np.copy(c_total)
        c_arr[int(c_limit):] = np.nan
        data = {
            't': timespan,
            'f': f_arr,
            'g': g_arr,
            'c': c_arr
        }
        return px.line(pd.DataFrame(data), x='t', y=['f', 'g', 'c'])

    @dash_app.callback(
        [
            Output(component_id='conv_plot', component_property='figure'),
            Output(component_id='time_slider', component_property='value'),
        ],
        [
            Input(component_id='play_btn', component_property='n_clicks'),
            Input(component_id='interval_component', component_property='n_intervals')
        ],
        [
            State(component_id='time_slider', component_property='value'),
        ]
    )
    def update_plot(n_clicks, n_intervals, slider_value):

        # play button pressed -> enter auto play mode
        if n_clicks != 0 and not n_clicks % 2:
            slider_value += 0.1
            return update_graphs(slider_value), slider_value

        # play button not pressed -> enter slider mode
        else:
            return update_graphs(slider_value), slider_value

    return dash_app.server
