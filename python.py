import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Load your dataset (replace with your data)
df = pd.read_csv("D:\\Project\\disaster_data.csv")

# Initialize the app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div([
    html.H1('Disaster Data Visualizer'),
    
    # Dropdown for filtering by disaster type
    dcc.Dropdown(
        id='disaster-type',
        options=[{'label': i, 'value': i} for i in df['Type'].unique()],
        value='All Disasters'
    ),
    
    # Graph component for visualizing data
    dcc.Graph(id='disaster-graph'),

    # Slider for year range
    dcc.RangeSlider(
        id='year-slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=[df['Year'].min(), df['Year'].max()],
        marks={str(year): str(year) for year in df['Year'].unique()}
    )
])

# Callbacks to update the graph based on dropdown and slider input
@app.callback(
    Output('disaster-graph', 'figure'),
    [Input('disaster-type', 'value'),
     Input('year-slider', 'value')]
)
def update_graph(selected_disaster, year_range):
    filtered_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]
    if selected_disaster != 'All Disasters':
        filtered_df = filtered_df[filtered_df['Type'] == selected_disaster]
    
    fig = px.line(filtered_df, x='Year', y='Frequency', color='Type', title='Disaster Frequency Over Time')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
