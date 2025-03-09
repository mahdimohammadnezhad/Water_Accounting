import dash
from dash import html, dcc, dash_table, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Initialize the Dash app with a better styling theme
app = dash.Dash(__name__, external_stylesheets=[dcc.themes.BOOTSTRAP])

# Read the data
df = pd.read_excel("dataset_acc.xlsx", sheet_name="Sheet1")

# Calculate summary statistics
summary_stats = df.describe()

# App layout with improved styling and organization
app.layout = html.Div([
    # Header
    html.Div([
        html.H1('Water Resources Dashboard', 
                style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '30px'})
    ], style={'padding': '20px', 'backgroundColor': '#f8f9fa'}),
    
    # Filters Section
    html.Div([
        html.H3('Filters', style={'marginBottom': '20px'}),
        html.Div([
            html.Div([
                html.Label('Select Column:'),
                dcc.Dropdown(
                    id='column-selector',
                    options=[{'label': col, 'value': col} for col in df.columns],
                    value=df.columns[1],  # Default to second column
                    style={'direction': 'rtl'}
                )
            ], style={'width': '48%', 'display': 'inline-block', 'marginRight': '2%'}),
            html.Div([
                html.Label('Select Range:'),
                dcc.RangeSlider(
                    id='range-slider',
                    min=0,
                    max=100,
                    step=1,
                    marks={0: '0%', 25: '25%', 50: '50%', 75: '75%', 100: '100%'},
                    value=[0, 100]
                )
            ], style={'width': '48%', 'display': 'inline-block'})
        ], style={'marginBottom': '20px'})
    ], style={'padding': '20px'}),
    
    # Visualization Section
    html.Div([
        html.Div([
            # Bar Chart
            dcc.Graph(id='bar-chart'),
        ], style={'width': '33%', 'display': 'inline-block'}),
        
        html.Div([
            # Pie Chart
            dcc.Graph(id='pie-chart'),
        ], style={'width': '33%', 'display': 'inline-block'}),

        html.Div([
            # Line Chart
            dcc.Graph(id='line-chart'),
        ], style={'width': '33%', 'display': 'inline-block'})
    ]),

    # Summary Statistics Section
    html.Div([
        html.H3('Summary Statistics', style={'marginTop': '30px', 'marginBottom': '20px'}),
        dash_table.DataTable(
            id='summary-table',
            columns=[{"name": i, "id": i} for i in summary_stats.columns],
            data=summary_stats.round(2).reset_index().rename(columns={"index": "Statistic"}).to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_cell={
                'textAlign': 'right',
                'padding': '10px',
                'whiteSpace': 'normal',
                'height': 'auto',
            },
            style_header={
                'backgroundColor': '#f8f9fa',
                'fontWeight': 'bold',
                'border': '1px solid black'
            },
            style_data={
                'backgroundColor': 'white',
                'border': '1px solid #ddd'
            }
        )
    ], style={'padding': '20px'}),
    
    # Data Table Section
    html.Div([
        html.H3('Data Table', style={'marginTop': '30px', 'marginBottom': '20px'}),
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_cell={
                'textAlign': 'right',
                'direction': 'rtl',
                'padding': '10px',
                'whiteSpace': 'normal',
                'height': 'auto',
            },
            style_header={
                'backgroundColor': '#f8f9fa',
                'fontWeight': 'bold',
                'border': '1px solid black'
            },
            style_data={
                'backgroundColor': 'white',
                'border': '1px solid #ddd'
            },
            page_size=10,  # Enable pagination
            filter_action="native",  # Enable filtering
            sort_action="native",  # Enable sorting
        )
    ], style={'padding': '20px'})
], style={'fontFamily': 'Arial, sans-serif'})

# Callback for updating the bar chart
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('column-selector', 'value')]
)
def update_bar_chart(selected_column):
    fig = px.bar(
        df,
        x='عنوان',
        y=selected_column,
        title=f'Distribution of {selected_column}',
        template='plotly_white'
    )
    fig.update_layout(
        xaxis_title='Title',
        yaxis_title=selected_column,
        plot_bgcolor='white'
    )
    return fig

# Callback for updating the pie chart
@app.callback(
    Output('pie-chart', 'figure'),
    [Input('column-selector', 'value'),
     Input('range-slider', 'value')]
)
def update_pie_chart(selected_column, range_value):
    # Filter data based on range slider
    min_val = df[selected_column].min() + (df[selected_column].max() - df[selected_column].min()) * range_value[0] / 100
    max_val = df[selected_column].min() + (df[selected_column].max() - df[selected_column].min()) * range_value[1] / 100
    filtered_df = df[(df[selected_column] >= min_val) & (df[selected_column] <= max_val)]
    
    fig = px.pie(
        filtered_df,
        values=selected_column,
        names='عنوان',
        title=f'Distribution of {selected_column} by Category'
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

# Callback for updating the line chart
@app.callback(
    Output('line-chart', 'figure'),
    [Input('column-selector', 'value'),
     Input('range-slider', 'value')]
)
def update_line_chart(selected_column, range_value):
    # Filter data based on range slider
    min_val = df[selected_column].min() + (df[selected_column].max() - df[selected_column].min()) * range_value[0] / 100
    max_val = df[selected_column].min() + (df[selected_column].max() - df[selected_column].min()) * range_value[1] / 100
    filtered_df = df[(df[selected_column] >= min_val) & (df[selected_column] <= max_val)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=filtered_df['عنوان'],
        y=filtered_df[selected_column],
        mode='lines+markers',
        name=selected_column
    ))
    fig.update_layout(
        title=f'Trend of {selected_column}',
        xaxis_title='Title',
        yaxis_title=selected_column,
        template='plotly_white'
    )
    return fig

# Callback for updating range slider
@app.callback(
    Output('range-slider', 'min'),
    Output('range-slider', 'max'),
    Output('range-slider', 'marks'),
    Output('range-slider', 'value'),
    [Input('column-selector', 'value')]
)
def update_range_slider(selected_column):
    min_val = 0
    max_val = 100
    marks = {0: '0%', 25: '25%', 50: '50%', 75: '75%', 100: '100%'}
    value = [0, 100]
    return min_val, max_val, marks, value

if __name__ == '__main__':
    app.run_server(debug=True)