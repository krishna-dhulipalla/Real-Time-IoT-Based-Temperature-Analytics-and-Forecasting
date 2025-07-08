import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

app = Dash(__name__)

def load_data(path='sensor_data.csv'):
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        return pd.DataFrame(columns=['eventTime', 'temperature', 'state'])


def layout(df):
    fig = px.line(df, x='eventTime', y='temperature', color='state', title='Sensor Temperatures')
    return html.Div([dcc.Graph(figure=fig)])


def main():
    df = load_data()
    app.layout = layout(df)
    app.run_server(debug=True)


if __name__ == '__main__':
    main()
