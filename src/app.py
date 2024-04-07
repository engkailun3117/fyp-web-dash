from dash import Dash, dcc, Output, Input, State, html
import dash_bootstrap_components as dbc
from dash import dash_table
import pandas as pd


# Load Data
path = 'DNNresults.csv'
data = pd.read_csv(path)
df = pd.DataFrame(data)
df['Month'] = pd.to_datetime(df['Month'])  # Convert Month column to datetime
df['Month'] = df['Month'].dt.strftime('%Y/%m')  # Format Month column as 'YYYY/MM'
df2 = df[['Month','Date','Country','Gateway','Telco','Shortcode','Keyword','Offer ID','Affiliate ID',
          'Total Sales','ECPA','Day 1','Week 1','Month 3 (P)','Month 4 (P)','Month 5 (P)','Month 6 (P)']]

# Dash components
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
server = app.server

# Function to filter data based on user selections
def filter_data(df, month, date, country, gateway, telco, shortcode, keyword, offer_id, affiliate_id):
    filtered_df = df.copy()
    if month:
        filtered_df = filtered_df[filtered_df['Month'] == month]
    if date:
        filtered_df = filtered_df[filtered_df['Date'] == date]
    if country:
        filtered_df = filtered_df[filtered_df['Country'] == country]
    if gateway:
        filtered_df = filtered_df[filtered_df['Gateway'] == gateway]
    if telco:
        filtered_df = filtered_df[filtered_df['Telco'] == telco]
    if shortcode:
        filtered_df = filtered_df[filtered_df['Shortcode'] == shortcode]
    if keyword:
        filtered_df = filtered_df[filtered_df['Keyword'] == keyword]
    if offer_id:
        filtered_df = filtered_df[filtered_df['Offer ID'] == offer_id]
    if affiliate_id:
        filtered_df = filtered_df[filtered_df['Affiliate ID'] == affiliate_id]
    return filtered_df

# Dash layout
app.layout = html.Div(style={'backgroundColor': '#f8f9fa', 'color': '#212529', 'fontFamily': 'Arial, sans-serif'}, children=[
    html.Link(
        href='https://fonts.googleapis.com/css2?family=Forum&display=swap',
        rel='stylesheet'
    ),

    html.H1('ARPU Prediction Result', style={'widt': '50%','textAlign': 'center', 'fontWeight': '2000', 'fontFamily': 'Forum','marginBottom': '20px'}),

    dbc.Button(
        "Expand filters collapse",
        id="collapse-button",
        outline=True,
        className="me-1",
        color='info',
        style={'fontFamily': 'Forum', 'fontWeight': 'bold', 'fontSize': '12px'},
        size="sm",
        n_clicks=0,
    ),

    dbc.Collapse(id='collapse', is_open=False, children=[

        html.Div([
            dcc.Dropdown(id='month-dropdown', options=[{'label': month, 'value': month} for month in df2['Month'].unique()], placeholder='Select Month',
                         style={'width': '30%',  'margin': '2px','fontFamily': 'Forum'}),
            dcc.Dropdown(id='date-dropdown', placeholder='Select Date', style={'width': '30%','margin': '2px', 'fontFamily': 'Forum'}),
            dcc.Dropdown(id='country-dropdown', placeholder='Select Country', style={'width': '30%', 'margin': '2px', 'fontFamily': 'Forum'}),
            dcc.Dropdown(id='gateway-dropdown', placeholder='Select Gateway', style={'width': '30%', 'margin': '2px', 'fontFamily': 'Forum'}),
            dcc.Dropdown(id='telco-dropdown', placeholder='Select Telco', style={'width': '30%', 'margin': '2px','fontFamily': 'Forum'}),
            dcc.Dropdown(id='shortcode-dropdown', placeholder='Select Shortcode', style={'width': '30%','margin': '2px','fontFamily': 'Forum'}),
            dcc.Dropdown(id='keyword-dropdown', placeholder='Select Keyword', style={'width': '30%', 'margin': '2px','fontFamily': 'Forum'}),
            dcc.Dropdown(id='offer-id-dropdown', placeholder='Select Offer ID', style={'width': '30%', 'margin': '2px', 'fontFamily': 'Forum'}),
            dcc.Dropdown(id='affiliate-id-dropdown', placeholder='Select Affiliate ID', style={'width': '30%', 'margin': '2px','fontFamily': 'Forum'})
        ], style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'center', 'marginBottom': '10px'}),

        html.Div([html.Button('Clear Filters', id='clear-filters-button', n_clicks=0, className='me-1', style={'margin': '5px','fontFamily': 'Forum', 'color': 'secondary'})]
                  ,style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'right', 'marginBottom': '10px'}),

        
    ]),

    # Table displaying filtered data
    dash_table.DataTable(
        id='table',
        columns=[{'name': col, 'id': col} for col in df2.columns if col not in ['Month 3 ROI', 'Month 4 ROI', 'Month 5 ROI', 'Month 6 ROI']], 
        data=[],
        style_data={
            'textAlign': 'left',
            'color': '#212529',
            'backgroundColor': '#ffffff',
            'fontWeight': 'bold',
            'fontFamily': 'Forum',
        },
        style_header={
            'textAlign': 'center',
            'backgroundColor': '#007bff',  # Neon blue color for header
            'color': '#ffffff',
            'fontWeight': 'bold',
            'fontFamily': 'Forum'
        },
        style_table={'height': '500px', 'overflowY': 'auto'},
        page_size=200,
    ),

    html.P('ROI (Return on Investment) based on predictions', 
           style={'textAlign': 'center', 'fontWeight': 'bold', 'fontFamily': 'Forum', 'marginBottom': '5px','fontSize':'25px'}),

    html.Div(
    [

        html.Div(
            [
                dcc.Graph(
                    id='month3-donut-graph',
                    figure={
                        'layout': {
                            'title': 'Month 3 ROI',  # Replace with actual title
                            'margin': {'t': 20, 'r': 20, 'b': 20, 'l': 20},
                            'fontWeight': 'bold',
                            'fontFamily': 'Forum',
                            'legend': {'orientation': 'horizontal', 'yanchor': 'top', 'xanchor': 'center'}
                        }
                    },
                    style={'width': '50%', 'display': 'inline-block'}  # Set width to 50% for side-by-side display
                ),
                dcc.Graph(
                    id='month4-donut-graph',
                    figure={
                        'layout': {
                            'title': 'Month 4 ROI',  # Replace with actual title
                            'margin': {'t': 20, 'r': 20, 'b': 20, 'l': 20},
                            'fontWeight': 'bold',
                            'fontFamily': 'Forum',
                            'legend': {'orientation': 'horizontal', 'yanchor': 'top', 'xanchor': 'center'}
                        }
                    },
                    style={'width': '50%', 'display': 'inline-block'}  # Set width to 50% for side-by-side display
                )
            ],
            style={'backgroundColor': '#f0f0f0', 'padding': '20px'}  # Add background color and padding
        )
    ]),

    html.Div(
    [
        html.Div(
            [
                dcc.Graph(
                    id='month5-donut-graph',
                    figure={
                        'layout': {
                            'title': 'Month 5 ROI',  # Replace with actual title
                            'margin': {'t': 20, 'r': 20, 'b': 20, 'l': 20},
                            'fontWeight': 'bold',
                            'fontFamily': 'Forum',
                            'legend': {'orientation': 'horizontal', 'yanchor': 'top', 'xanchor': 'center'}
                        }
                    },
                    style={'width': '50%', 'display': 'inline-block'}  # Set width to 50% for side-by-side display
                ),
                dcc.Graph(
                    id='month6-donut-graph',
                    figure={
                        'layout': {
                            'title': 'Month 6 ROI',  # Replace with actual title
                            'margin': {'t': 20, 'r': 20, 'b': 20, 'l': 20},
                            'fontWeight': 'bold',
                            'fontFamily': 'Forum',
                            'legend': {'orientation': 'horizontal', 'yanchor': 'top', 'xanchor': 'center'}
                        }
                    },
                    style={'width': '50%', 'display': 'inline-block'}  # Set width to 50% for side-by-side display
                )
            ],
            style={'backgroundColor': '#f0f0f0', 'padding': '20px'}  # Add background color and padding
        )
    ])

])

# Collapse filter columns feature
@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# change the expand/collapse box word
@app.callback(
    Output('collapse-button', 'children'),
    [Input('collapse', 'is_open')]
)
def update_button_text(is_open):
    if is_open:
        return "Collapse filters"
    else:
        return "Expand filters"

# Callback to update date dropdown options based on month selection
@app.callback(
    Output('date-dropdown', 'options'),
    [Input('month-dropdown', 'value')]
)
def update_date_dropdown(month):
    if month:
        options = [{'label': date, 'value': date} for date in df2[df2['Month'] == month]['Date'].unique()]
    else:
        options = []
    return options

# Callback to update country dropdown options based on month and date selections
@app.callback(
    Output('country-dropdown', 'options'),
    [Input('month-dropdown', 'value'),
     Input('date-dropdown', 'value')]
)
def update_country_dropdown(month, date):
    if month and date:
        options = [{'label': country, 'value': country} for country in df2[(df2['Month'] == month) & (df2['Date'] == date)]['Country'].unique()]
    else:
        options = []
    return options

# Callback to update gateway dropdown options based on month, date and country selections
@app.callback(
    Output('gateway-dropdown', 'options'),
    [Input('month-dropdown', 'value'),
     Input('date-dropdown', 'value'),
     Input('country-dropdown','value')]
)
def update_gateway_dropdown(month, date, country):
    if month and date and country:
        options = [{'label':gateway, 'value': gateway} for gateway in df2[(df2['Month'] == month) & (df2['Date'] == date) & (df2['Country'] == country)]['Gateway'].unique()]
    else:
        options = []
    return options

# Callback to update telco dropdown options based on month, date, country, and gateway selections
@app.callback(
    Output('telco-dropdown', 'options'),
    [Input('month-dropdown', 'value'),
     Input('date-dropdown', 'value'),
     Input('country-dropdown', 'value'),
     Input('gateway-dropdown', 'value')]
)
def update_telco_dropdown(month, date, country, gateway):
    if month and date and country and gateway:
        options = [{'label': telco, 'value': telco} for telco in df2[(df2['Month'] == month) & (df2['Date'] == date) & (df2['Country'] == country) & (df2['Gateway'] == gateway)]['Telco'].unique()]
    else:
        options = []
    return options

# Callback to update shortcode dropdown options based on month, date, country, gateway, and telco selections
@app.callback(
    Output('shortcode-dropdown', 'options'),
    [Input('month-dropdown', 'value'),
     Input('date-dropdown', 'value'),
     Input('country-dropdown', 'value'),
     Input('gateway-dropdown', 'value'),
     Input('telco-dropdown', 'value')]
)
def update_shortcode_dropdown(month, date, country, gateway, telco):
    if month and date and country and gateway and telco:
        options = [{'label': shortcode, 'value': shortcode} for shortcode in df2[(df2['Month'] == month) & (df2['Date'] == date) & (df2['Country'] == country) & (df2['Gateway'] == gateway) & (df2['Telco'] == telco)]['Shortcode'].unique()]
    else:
        options = []
    return options


# Callback to update keyword dropdown options based on month, date, country, gateway, telco, and shortcode selections
@app.callback(
    Output('keyword-dropdown', 'options'),
    [Input('month-dropdown', 'value'),
     Input('date-dropdown', 'value'),
     Input('country-dropdown', 'value'),
     Input('gateway-dropdown', 'value'),
     Input('telco-dropdown', 'value'),
     Input('shortcode-dropdown', 'value')]
)
def update_keyword_dropdown(month, date, country, gateway, telco, shortcode):
    if month and date and country and gateway and telco and shortcode:
        options =[{'label': keyword, 'value': keyword} for keyword in df2[(df2['Month'] == month) & (df2['Date'] == date) & (df2['Country'] == country) & (df2['Gateway'] == gateway) & (df2['Telco'] == telco) & (df2['Shortcode'] == shortcode)]['Keyword'].unique()]
    else:
        options = []
    return options

# Callback to update offer ID dropdown options based on month, date, country, gateway, telco, shortcode, and keyword selections
@app.callback(
    Output('offer-id-dropdown', 'options'),
    [Input('month-dropdown', 'value'),
     Input('date-dropdown', 'value'),
     Input('country-dropdown', 'value'),
     Input('gateway-dropdown', 'value'),
     Input('telco-dropdown', 'value'),
     Input('shortcode-dropdown', 'value'),
     Input('keyword-dropdown', 'value')]
)
def update_offer_id_dropdown(month, date, country, gateway, telco, shortcode, keyword):
    if month and date and country and gateway and telco and shortcode and keyword:
        options = [{'label': offer_id, 'value': offer_id} for offer_id in df2[(df2['Month'] == month) & (df2['Date'] == date) & (df2['Country'] == country) & (df2['Gateway'] == gateway) & (df2['Telco'] == telco) & (df2['Shortcode'] == shortcode) & (df2['Keyword'] == keyword)]['Offer ID'].unique()]
    else:
        options = []
    return options

# Callback to update affiliate ID dropdown options based on all filter selections
@app.callback(
    Output('affiliate-id-dropdown', 'options'),
    [Input('month-dropdown', 'value'),
     Input('date-dropdown', 'value'),
     Input('country-dropdown', 'value'),
     Input('gateway-dropdown', 'value'),
     Input('telco-dropdown', 'value'),
     Input('shortcode-dropdown', 'value'),
     Input('keyword-dropdown', 'value'),
     Input('offer-id-dropdown', 'value')]
)
def update_affiliate_id_dropdown(month, date, country, gateway, telco, shortcode, keyword, offer_id):
    if month and date and country and gateway and telco and shortcode and keyword and offer_id:
        options = [{'label': affiliate_id, 'value': affiliate_id} for affiliate_id in df2[(df2['Month'] == month) & (df2['Date'] == date) & (df2['Country'] == country) & (df2['Gateway'] == gateway) & (df2['Telco'] == telco) & (df2['Shortcode'] == shortcode) & (df2['Keyword'] == keyword) & (df2['Offer ID'] == offer_id)]['Affiliate ID'].unique()]
    else:
        options = []
    return options

# Callback to update table data based on all filter selections
@app.callback(
    Output('table', 'data'),
    [Input('month-dropdown', 'value'),
     Input('date-dropdown', 'value'),
     Input('country-dropdown', 'value'),
     Input('gateway-dropdown', 'value'),
     Input('telco-dropdown', 'value'),
     Input('shortcode-dropdown', 'value'),
     Input('keyword-dropdown', 'value'),
     Input('offer-id-dropdown', 'value'),
     Input('affiliate-id-dropdown', 'value')]
)
def update_table_data(month, date, country, gateway, telco, shortcode, keyword, offer_id, affiliate_id):
    filtered_df = filter_data(df2, month, date, country, gateway, telco, shortcode, keyword, offer_id, affiliate_id)
    return filtered_df.to_dict('records')


# Month 3 donut graph callback
@app.callback(
    Output('month3-donut-graph', 'figure'),
    [Input('table', 'data'),
     Input('table', 'data_timestamp')]  # Input from table update callback
)
def update_month3_donut_graph(filtered_data, data_timestamp):
    if not filtered_data:  # Handle empty data case
        return {}

    # Extract filtered DataFrame from the callback context
    filtered_df = pd.DataFrame(filtered_data)

    # Calculate the percentage for the metric
    if len(filtered_df) > 0:
        metric_percentage = (filtered_df['Month 3 (P)'] / filtered_df['ECPA'] > 1).sum() / len(filtered_df) * 100
    else:
        metric_percentage = 0

    # Create donut chart figure
    return {
        'data': [
            {
                'values': [metric_percentage, 100 - metric_percentage],
                'labels': ['Hit ROI', 'Missed ROI'],
                'type': 'pie',
                'hole': 0.4,
                'textinfo': 'label+percent',
                'fontWeight': 'bold',
                'fontFamily': 'Forum',
                'textposition': 'inside',
                'marker': {
                    'colors': ['#fdae61', '#abcaf0']
                }
            }
        ],
        'layout': {
            'title': 'Month 3 ROI',  # Replace with actual title
            'margin': {'top': 20, 'right': 20, 'bottom': 20, 'left': 20},
            'fontWeight': 'bold',
            'fontFamily': 'Forum',
            'legend': {'orientation': 'horizontal', 'yanchor': 'top', 'xanchor': 'center'}
        }
    }


# Month 4 donut graph callback
@app.callback(
    Output('month4-donut-graph', 'figure'),
    [Input('table', 'data'),
     Input('table', 'data_timestamp')]  # Input from table update callback
)
def update_month4_donut_graph(filtered_data, data_timestamp):
    if not filtered_data:  # Handle empty data case
        return {}

    # Extract filtered DataFrame from the callback context
    filtered_df = pd.DataFrame(filtered_data)

    # Calculate the percentage for the metric
    if len(filtered_df) > 0:
        metric_percentage = (filtered_df['Month 4 (P)'] / filtered_df['ECPA'] > 1).sum() / len(filtered_df) * 100
    else:
        metric_percentage = 0

    # Create donut chart figure
    return {
        'data': [
            {
                'values': [metric_percentage, 100 - metric_percentage],
                'labels': ['Hit ROI', 'Missed ROI'],
                'type': 'pie',
                'hole': 0.4,
                'textinfo': 'label+percent',
                'fontWeight': 'bold',
                'fontFamily': 'Forum',
                'textposition': 'inside',
                'marker': {
                    'colors': ['#f0f5bc', '#d2b4ed']
                }
            }
        ],
        'layout': {
            'title': 'Month 4 ROI',  # Replace with actual title
            'margin': {'top': 20, 'right': 20, 'bottom': 20, 'left': 20},
            'fontWeight': 'bold',
            'fontFamily': 'Forum',
            'legend': {'orientation': 'horizontal', 'yanchor': 'top', 'xanchor': 'center'}
        }
    }

# Month 5 donut graph callback
@app.callback(
    Output('month5-donut-graph', 'figure'),
    [Input('table', 'data'),
     Input('table', 'data_timestamp')]  # Input from table update callback
)
def update_month5_donut_graph(filtered_data, data_timestamp):
    if not filtered_data:  # Handle empty data case
        return {}

    # Extract filtered DataFrame from the callback context
    filtered_df = pd.DataFrame(filtered_data)

    # Calculate the percentage for the metric
    if len(filtered_df) > 0:
        metric_percentage = (filtered_df['Month 5 (P)'] / filtered_df['ECPA'] > 1).sum() / len(filtered_df) * 100
    else:
        metric_percentage = 0

    # Create donut chart figure
    return {
        'data': [
            {
                'values': [metric_percentage, 100 - metric_percentage],
                'labels': ['Hit ROI', 'Missed ROI'],
                'type': 'pie',
                'hole': 0.4,
                'textinfo': 'label+percent',
                'fontWeight': 'bold',
                'fontFamily': 'Forum',
                'textposition': 'inside',
                'marker': {
                    'colors': ['#ebc0b0', '#b7ebe6']
                }
            }
        ],
        'layout': {
            'title': 'Month 5 ROI',  # Replace with actual title
            'margin': {'top': 20, 'right': 20, 'bottom': 20, 'left': 20},
            'fontWeight': 'bold',
            'fontFamily': 'Forum',
            'legend': {'orientation': 'horizontal', 'yanchor': 'top', 'xanchor': 'center'}
        }
    }

# Month 6 donut graph callback
@app.callback(
    Output('month6-donut-graph', 'figure'),
    [Input('table', 'data'),
     Input('table', 'data_timestamp')]  # Input from table update callback
)
def update_month6_donut_graph(filtered_data, data_timestamp):
    if not filtered_data:  # Handle empty data case
        return {}

    # Extract filtered DataFrame from the callback context
    filtered_df = pd.DataFrame(filtered_data)

    # Calculate the percentage for the metric
    if len(filtered_df) > 0:
        metric_percentage = (filtered_df['Month 6 (P)'] / filtered_df['ECPA'] > 1).sum() / len(filtered_df) * 100
    else:
        metric_percentage = 0

    # Create donut chart figure
    return {
        'data': [
            {
                'values': [metric_percentage, 100 - metric_percentage],
                'labels': ['Hit ROI', 'Missed ROI'],
                'type': 'pie',
                'hole': 0.4,
                'textinfo': 'label+percent',
                'fontWeight': 'bold',
                'fontFamily': 'Forum',
                'textposition': 'inside',
                'marker': {
                    'colors': ['#beebbe', '#ebbcbc']
                }
            }
        ],
        'layout': {
            'title': 'Month 6 ROI',  # Replace with actual title
            'margin': {'top': 20, 'right': 20, 'bottom': 20, 'left': 20},
            'fontWeight': 'bold',
            'fontFamily': 'Forum',
            'legend': {'orientation': 'horizontal', 'yanchor': 'top', 'xanchor': 'center'}
        }
    }

# Callback to clear all filter dropdowns
@app.callback(
    [Output('month-dropdown', 'value'),
     Output('date-dropdown', 'value'),
     Output('country-dropdown', 'value'),
     Output('gateway-dropdown', 'value'),
     Output('telco-dropdown', 'value'),
     Output('shortcode-dropdown', 'value'),
     Output('keyword-dropdown', 'value'),
     Output('offer-id-dropdown', 'value'),
     Output('affiliate-id-dropdown', 'value')],
    [Input('clear-filters-button', 'n_clicks')]
)
def clear_filters(n_clicks):
    if n_clicks:
        return '', '', '', '', '', '', '', '', ''
    return ('', '', '', '', '', '', '', '', '')

if __name__ == '__main__':
    app.run_server(debug=True)



