from flask import Flask
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
import yfinance as yf
import plotly.graph_objs as go
from dash.dependencies import Input, Output

server = Flask(__name__)


app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout of the app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Label("Choose a stock:", style={'margin-right': '10px'}),
            dcc.Dropdown(
                id='stock-selector',
                options=[
                    {'label': 'Bitcoin (USD)', 'value': 'BTC-USD'},
                    {'label': 'Apple', 'value': 'AAPL'},
                    {'label': 'Google', 'value': 'GOOGL'},
                    {'label': 'Euro', 'value': 'EURUSD=X'},
                    {'label': 'TCS', 'value': 'TCS.NS'},
                    {'label': 'Asian Paints', 'value': 'ASIANPAINT.NS'},
                    {'label': 'Nifty Bank', 'value': '^NSEBANK'}
                ],
                value='BTC-USD',
                style={'width': '150px', 'display': 'inline-block', 'margin-right': '10px'}
            ),
            html.Label("Graph type:", style={'margin-right': '10px'}),
            dcc.Dropdown(
                id='graph-type-selector',
                options=[
                    {'label': 'Line', 'value': 'lines'},
                    {'label': 'Candlestick', 'value': 'candle'},
                    {'label': 'Step', 'value': 'step'}
                ],
                value='lines',
                style={'width': '150px', 'display': 'inline-block', 'margin-right': '10px'}
            ),
            html.Label("Period:", style={'margin-right': '10px'}),
            dcc.Dropdown(
                id='period-selector',
                options=[
                    {'label': '1 Day', 'value': '1d'},
                    {'label': '5 Days', 'value': '5d'},
                    {'label': '1 Month', 'value': '1mo'},
                    {'label': '3 Months', 'value': '3mo'},
                    {'label': '6 Months', 'value': '6mo'},
                    {'label': '1 Year', 'value': '1y'},
                ],
                value='1d',
                style={'width': '150px', 'display': 'inline-block', 'margin-right': '10px'}
            ),
            html.Label("Interval:", style={'margin-right': '10px'}),
            dcc.Dropdown(
                id='interval-selector',
                options=[
                    {'label': '1 Minute', 'value': '1m'},
                    {'label': '5 Minutes', 'value': '5m'},
                    {'label': '15 Minutes', 'value': '15m'},
                    {'label': '30 Minutes', 'value': '30m'},
                    {'label': '60 Minutes', 'value': '60m'},
                    {'label': '90 Minutes', 'value': '90m'},
                    {'label': '1 Hour', 'value': '1h'},
                    {'label': '1 Day', 'value': '1d'},
                ],
                value='1m',
                style={'width': '150px', 'display': 'inline-block'}
            ),
        ], width=10,style={'margin-top':'30px','margin-left':'200px'})
    ], className='mb-4'),
    dbc.Row(dbc.Col(dcc.Graph(id='stock-chart'), width=12)),
    dcc.Interval(
        id='interval-component',
        interval=10*1000,  
        n_intervals=0
    )
], fluid=True)

@app.callback(
    Output('stock-chart', 'figure'),
    [
        Input('stock-selector', 'value'),
        Input('graph-type-selector', 'value'),
        Input('period-selector', 'value'),
        Input('interval-selector', 'value'),
        Input('interval-component', 'n_intervals')
    ]
)
def update_chart(symbol, graph_type, period, interval, n_intervals):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period=period, interval=interval)
    data.reset_index(inplace=True)

    if graph_type == 'lines':
        trace = go.Scatter(x=data['Datetime'], y=data['Close'], mode='lines', name='Stock Price')
    elif graph_type == 'candle':
        trace = go.Candlestick(x=data['Datetime'], open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name='Stock Price')
    elif graph_type == 'step':
        trace = go.Scatter(x=data['Datetime'], y=data['Close'], mode='lines', line_shape='hv', name='Stock Price')
    
    layout = go.Layout(
        margin=dict(l=40, r=20, t=40, b=40)
    )

    return {'data': [trace], 'layout': layout}


if __name__ == '__main__':
    app.run_server(debug=True)
