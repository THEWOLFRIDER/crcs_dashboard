import dash
from dash import dcc
from dash import html
import pandas as pd

# Read the dataset1.csv
df = pd.read_csv("dataset1.csv")

# Create the Dash app
app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div(
    children=[
        html.H1('CRCS Portal Dashboard'),
        
        # Data visualization components
        dcc.Graph(
            id='registered-mscs',
            figure={
                'data': [
                    {'x': df['State'], 'y': df['Number of Registered MSCS'], 'type': 'bar', 'name': 'Registered MSCS'},
                ],
                'layout': {
                    'title': 'Number of Registered MSCS by State',
                    'xaxis': {'title': 'State'},
                    'yaxis': {'title': 'Number of Registered MSCS'}
                }
            }
        ),
        
        dcc.Graph(
            id='sector-distribution',
            figure={
                'data': [
                    {'labels': df['Sector Type'], 'values': df['Number of MSCS'], 'type': 'pie', 'name': 'Sector Distribution'},
                ],
                'layout': {
                    'title': 'MSCS Sector Distribution',
                }
            }
        ),
        
        # Filters and interactivity
        dcc.Dropdown(
            id='state-dropdown',
            options=[{'label': state, 'value': state} for state in df['State'].unique()],
            value=None,
            placeholder='Select a state'
        ),
        
        dcc.Dropdown(
            id='district-dropdown',
            options=[{'label': district, 'value': district} for district in df['District'].unique()],
            value=None,
            placeholder='Select a district'
        ),
        
        # Additional components and features
        html.Div(id='selected-mscs-details'),
        
        # Add more components and features as needed
        
    ]
)

# Callbacks for interactivity and drill-down capabilities
@app.callback(
    dash.dependencies.Output('selected-mscs-details', 'children'),
    [dash.dependencies.Input('state-dropdown', 'value'),
     dash.dependencies.Input('district-dropdown', 'value')]
)
def display_selected_mscs_details(selected_state, selected_district):
    if selected_state is not None and selected_district is not None:
        selected_mscs = df[(df['State'] == selected_state) & (df['District'] == selected_district)]
        return html.Table(
            children=[
                html.Thead(
                    html.Tr(
                        children=[
                            html.Th('Society Name'),
                            html.Th('Address'),
                            html.Th('Date of Registration'),
                            html.Th('Area of Operation'),
                            html.Th('Sector Type')
                        ]
                    )
                ),
                html.Tbody(
                    [html.Tr(
                        children=[
                            html.Td(selected_msc['Society Name']),
                            html.Td(selected_msc['Society Address']),
                            html.Td(selected_msc['Date of Registration']),
                            html.Td(selected_msc['Area of Operation']),
                            html.Td(selected_msc['Sector Type'])
                        ]
                    ) for _, selected_msc in selected_mscs.iterrows()]
                )
            ]
        )

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
import dash
from dash import dcc
from dash import html
import pandas as pd

# Read the dataset1.csv
df = pd.read_csv("dataset1.csv")

# Create the Dash app
app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div(
    children=[
        html.H1('CRCS Portal Dashboard'),
        
     
        
        # Filters and interactivity
        dcc.Dropdown(
            id='state-dropdown',
            options=[{'label': state, 'value': state} for state in df['State'].unique()],
            value=None,
            placeholder='Select a state'
        ),
        
        dcc.Dropdown(
            id='district-dropdown',
            options=[{'label': district, 'value': district} for district in df['District'].unique()],
            value=None,
            placeholder='Select a district'
        ),
        
        # Additional components and features
        html.Div(id='selected-mscs-details'),
        
        dcc.Markdown('''
            #### Additional Features:
            
            - **Search by Society Name**: Enter a society name to search and display its details.
            
            - **Yearly Registration Trend**: Show the trend of registrations over the years using a line chart.
            
            - **Responsive Design**: Ensure the dashboard is responsive and compatible with different screen sizes and devices.
        '''),
        
        dcc.Input(
            id='society-search',
            type='text',
            placeholder='Enter society name'
        ),
        
        dcc.Graph(
            id='yearly-registration-trend',
        ),
        
    ]
)

# Callbacks for interactivity and drill-down capabilities
@app.callback(
    dash.dependencies.Output('selected-mscs-details', 'children'),
    [dash.dependencies.Input('state-dropdown', 'value'),
     dash.dependencies.Input('district-dropdown', 'value'),
     dash.dependencies.Input('society-search', 'value')]
)
def display_selected_mscs_details(selected_state, selected_district, society_name):
    if society_name:
        selected_mscs = df[df['Society Name'].str.contains(society_name, case=False)]
    elif selected_state is not None and selected_district is not None:
        selected_mscs = df[(df['State'] == selected_state) & (df['District'] == selected_district)]
    else:
        return ''
    
    return html.Table(
        children=[
            html.Thead(
                html.Tr(
                    children=[
                        html.Th('Society Name'),
                        html.Th('Address'),
                        html.Th('Date of Registration'),
                        html.Th('Area of Operation'),
                        html.Th('Sector Type')
                    ]
                )
            ),
            html.Tbody(
                [
                    html.Tr(
                        children=[
                            html.Td(selected_msc['Society Name']),
                            html.Td(selected_msc['Society Address']),
                            html.Td(selected_msc['Date of Registration']),
                            html.Td(selected_msc['Area of Operation']),
                            html.Td(selected_msc['Sector Type'])
                        ]
                    )
                    for _, selected_msc in selected_mscs.iterrows()
                ]
            )
        ]
    )

@app.callback(
    dash.dependencies.Output('yearly-registration-trend', 'figure'),
    [dash.dependencies.Input('state-dropdown', 'value'),
     dash.dependencies.Input('district-dropdown', 'value')]
)
def display_yearly_registration_trend(selected_state, selected_district):
    if selected_state is not None and selected_district is not None:
        selected_mscs = df[(df['State'] == selected_state) & (df['District'] == selected_district)]
    else:
        selected_mscs = df
    
    yearly_registration_count = (
        selected_mscs.groupby('Year')['Number of Registered MSCS']
        .sum()
        .reset_index()
    )
    
    return {
        'data': [
            {'x': yearly_registration_count['Year'], 'y': yearly_registration_count['Number of Registered MSCS'], 'type': 'line', 'name': 'Yearly Registration Trend'},
        ],
        'layout': {
            'title': 'Yearly Registration Trend',
            'xaxis': {'title': 'Year'},
            'yaxis': {'title': 'Number of Registered MSCS'}
        }
    }

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

# Callbacks for interactivity and drill-down capabilities
@app.callback(
    dash.dependencies.Output('selected-mscs-details', 'children'),
    [dash.dependencies.Input('state-dropdown', 'value'),
     dash.dependencies.Input('district-dropdown', 'value'),
     dash.dependencies.Input('society-search', 'value')]
)
def display_selected_mscs_details(selected_state, selected_district, society_name):
    if society_name:
        selected_mscs = df[df['Society Name'].str.contains(society_name, case=False)]
    elif selected_state is not None and selected_district is not None:
        selected_mscs = df[(df['State'] == selected_state) & (df['District'] == selected_district)]
    else:
        return ''
    
    return html.Table(
        children=[
            html.Thead(
                html.Tr(
                    children=[
                        html.Th('Society Name'),
                        html.Th('Address'),
                        html.Th('Date of Registration'),
                        html.Th('Area of Operation'),
                        html.Th('Sector Type')
                    ]
                )
            ),
            html.Tbody(
                [
                    html.Tr(
                        children=[
                            html.Td(selected_msc['Society Name']),
                            html.Td(selected_msc['Society Address']),
                            html.Td(selected_msc['Date of Registration']),
                            html.Td(selected_msc['Area of Operation']),
                            html.Td(selected_msc['Sector Type'])
                        ]
                    )
                    for _, selected_msc in selected_mscs.iterrows()
                ]
            )
        ]
    )

@app.callback(
    dash.dependencies.Output('yearly-registration-trend', 'figure'),
    [dash.dependencies.Input('state-dropdown', 'value'),
     dash.dependencies.Input('district-dropdown', 'value')]
)
def display_yearly_registration_trend(selected_state, selected_district):
    if selected_state is not None and selected_district is not None:
        selected_mscs = df[(df['State'] == selected_state) & (df['District'] == selected_district)]
    else:
        selected_mscs = df
    
    yearly_registration_count = (
        selected_mscs.groupby('Year')['Number of Registered MSCS']
        .sum()
        .reset_index()
    )
    
    return {
        'data': [
            {'x': yearly_registration_count['Year'], 'y': yearly_registration_count['Number of Registered MSCS'], 'type': 'line', 'name': 'Yearly Registration Trend'},
        ],
        'layout': {
            'title': 'Yearly Registration Trend',
            'xaxis': {'title': 'Year'},
            'yaxis': {'title': 'Number of Registered MSCS'}
        }
    }

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
# Callback for filtering the dataset1.csv based on the selected state and district
@app.callback(
    dash.dependencies.Output('filtered-data', 'data'),
    [dash.dependencies.Input('state-dropdown', 'value'),
     dash.dependencies.Input('district-dropdown', 'value')]
)
def filter_data(selected_state, selected_district):
    if selected_state is not None and selected_district is not None:
        filtered_data = df[(df['State'] == selected_state) & (df['District'] == selected_district)]
    else:
        filtered_data = df
    
    return filtered_data.to_dict('records')

# Callback for updating the dropdown options for districts based on the selected state
@app.callback(
    dash.dependencies.Output('district-dropdown', 'options'),
    [dash.dependencies.Input('state-dropdown', 'value')]
)
def update_district_dropdown(selected_state):
    if selected_state is not None:
        districts = df[df['State'] == selected_state]['District'].unique()
        district_options = [{'label': district, 'value': district} for district in districts]
        return district_options
    
    return []

# Callback for updating the dropdown options for societies based on the selected state and district
@app.callback(
    dash.dependencies.Output('society-dropdown', 'options'),
    [dash.dependencies.Input('state-dropdown', 'value'),
     dash.dependencies.Input('district-dropdown', 'value')]
)
def update_society_dropdown(selected_state, selected_district):
    if selected_state is not None and selected_district is not None:
        societies = df[(df['State'] == selected_state) & (df['District'] == selected_district)]['Society Name'].unique()
        society_options = [{'label': society, 'value': society} for society in societies]
        return society_options
    
    return []

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
# Callback for updating the data table based on the selected society
@app.callback(
    dash.dependencies.Output('data-table', 'data'),
    [dash.dependencies.Input('society-dropdown', 'value')],
    [dash.dependencies.State('filtered-data', 'data')]
)
def update_data_table(selected_society, filtered_data):
    if selected_society is not None:
        selected_data = filtered_data[filtered_data['Society Name'] == selected_society]
    else:
        selected_data = filtered_data
    
    return selected_data.to_dict('records')


# Add additional components, layouts, and callbacks as per your project's needs
# ...


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
# Add additional components, layouts, and callbacks as per your project's needs
# ...

# Define the layout of the dashboard
app.layout = html.Div(
    [
        # Header section
        html.Header(
            [
                html.H1('CRCS Portal Dashboard'),
                html.H3('Multistate Cooperative Societies Registration and Management'),
            ]
        ),
        
        # Filter section
        html.Div(
            [
                html.Label('Select State:'),
                dcc.Dropdown(
                    id='state-dropdown',
                    options=[
                        {'label': state, 'value': state} for state in df['State'].unique()
                    ],
                    multi=True,
                    placeholder='Select State'
                ),
                
                html.Label('Select District:'),
                dcc.Dropdown(
                    id='district-dropdown',
                    options=[
                        {'label': district, 'value': district} for district in df['District'].unique()
                    ],
                    multi=True,
                    placeholder='Select District'
                ),
                
                html.Label('Select Sector:'),
                dcc.Dropdown(
                    id='sector-dropdown',
                    options=[
                        {'label': sector, 'value': sector} for sector in df['Sector Type'].unique()
                    ],
                    multi=True,
                    placeholder='Select Sector'
                ),
            ],
            className='filter-section'
        ),
        
        # Main content section
        html.Div(
            [
                # Data table section
                html.Div(
                    id='data-table-section',
                    children=[
                        html.H3('Registered Societies'),
                        dash_table.DataTable(
                            id='data-table',
                            columns=[
                                {'name': col, 'id': col} for col in df.columns
                            ],
                            data=df.to_dict('records'),
                            style_table={'overflowX': 'scroll'},
                            style_cell={
                                'minWidth': '100px', 'width': '150px', 'maxWidth': '300px',
                                'whiteSpace': 'normal', 'textAlign': 'left'
                            }
                        ),
                    ]
                ),
                
                # Society details section
                html.Div(
                    id='society-details-section',
                    children=[
                        html.H3('Society Details'),
                        dcc.Markdown(
                            id='society-details-text',
                            className='society-details-text'
                        ),
                    ]
                ),
            ],
            className='content-section'
        ),
    ]
)

# Callback for updating the data table based on the selected filters
@app.callback(
    dash.dependencies.Output('data-table', 'data'),
    [dash.dependencies.Input('state-dropdown', 'value'),
     dash.dependencies.Input('district-dropdown', 'value'),
     dash.dependencies.Input('sector-dropdown', 'value')]
)
def update_data_table(selected_states, selected_districts, selected_sectors):
    filtered_data = df[
        df['State'].isin(selected_states) &
        df['District'].isin(selected_districts) &
        df['Sector Type'].isin(selected_sectors)
    ]
    return filtered_data.to_dict('records')


# Callback for updating the society details text based on the selected row
@app.callback(
    dash.dependencies.Output('society-details-text', 'children'),
    [dash.dependencies.Input('data-table', 'active_cell')],
    [dash.dependencies.State('data-table', 'data')]
)
def update_society_details(active_cell, data):
    if active_cell is not None:
        row_index = active_cell['row']
        selected_society = data[row_index]['Society Name']
        society_details = get_society_details(selected_society)  # Custom function to get society details
        return society_details
    else:
        return ''


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
# Define additional components, layouts, and callbacks as per your project's needs
# ...

# Define the layout of the dashboard
app.layout = html.Div(
    [
        # Header section
        html.Header(
            [
                html.H1('CRCS Portal Dashboard'),
                html.H3('Multistate Cooperative Societies Registration and Management'),
            ]
        ),
        
        # Filter section
        html.Div(
            [
                html.Label('Select State:'),
                dcc.Dropdown(
                    id='state-dropdown',
                    options=[
                        {'label': state, 'value': state} for state in df['State'].unique()
                    ],
                    multi=True,
                    placeholder='Select State'
                ),
                
                html.Label('Select District:'),
                dcc.Dropdown(
                    id='district-dropdown',
                    options=[
                        {'label': district, 'value': district} for district in df['District'].unique()
                    ],
                    multi=True,
                    placeholder='Select District'
                ),
                
                html.Label('Select Sector:'),
                dcc.Dropdown(
                    id='sector-dropdown',
                    options=[
                        {'label': sector, 'value': sector} for sector in df['Sector Type'].unique()
                    ],
                    multi=True,
                    placeholder='Select Sector'
                ),
            ],
            className='filter-section'
        ),
        
        # Main content section
        html.Div(
            [
                # Data table section
                html.Div(
                    id='data-table-section',
                    children=[
                        html.H3('Registered Societies'),
                        dash_table.DataTable(
                            id='data-table',
                            columns=[
                                {'name': col, 'id': col} for col in df.columns
                            ],
                            data=df.to_dict('records'),
                            style_table={'overflowX': 'scroll'},
                            style_cell={
                                'minWidth': '100px', 'width': '150px', 'maxWidth': '300px',
                                'whiteSpace': 'normal', 'textAlign': 'left'
                            }
                        ),
                    ]
                ),
                
                # Society details section
                html.Div(
                    id='society-details-section',
                    children=[
                        html.H3('Society Details'),
                        dcc.Markdown(
                            id='society-details-text',
                            className='society-details-text'
                        ),
                    ]
                ),
            ],
            className='content-section'
        ),
        
        # Additional components and sections
        # ...

    ]
)

# Callbacks for updating the data table and society details based on the selected filters and rows
# ...


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
# Define additional components, layouts, and callbacks as per your project's needs
# ...

# Define the layout of the dashboard
app.layout = html.Div(
    [
        # Header section
        html.Header(
            [
                html.H1('CRCS Portal Dashboard'),
                html.H3('Multistate Cooperative Societies Registration and Management'),
            ]
        ),
        
        # Filter section
        html.Div(
            [
                html.Label('Select State:'),
                dcc.Dropdown(
                    id='state-dropdown',
                    options=[
                        {'label': state, 'value': state} for state in df['State'].unique()
                    ],
                    multi=True,
                    placeholder='Select State'
                ),
                
                html.Label('Select District:'),
                dcc.Dropdown(
                    id='district-dropdown',
                    options=[
                        {'label': district, 'value': district} for district in df['District'].unique()
                    ],
                    multi=True,
                    placeholder='Select District'
                ),
                
                html.Label('Select Sector:'),
                dcc.Dropdown(
                    id='sector-dropdown',
                    options=[
                        {'label': sector, 'value': sector} for sector in df['Sector Type'].unique()
                    ],
                    multi=True,
                    placeholder='Select Sector'
                ),
            ],
            className='filter-section'
        ),
        
        # Main content section
        html.Div(
            [
                # Data table section
                html.Div(
                    id='data-table-section',
                    children=[
                        html.H3('Registered Societies'),
                        dash_table.DataTable(
                            id='data-table',
                            columns=[
                                {'name': col, 'id': col} for col in df.columns
                            ],
                            data=df.to_dict('records'),
                            style_table={'overflowX': 'scroll'},
                            style_cell={
                                'minWidth': '100px', 'width': '150px', 'maxWidth': '300px',
                                'whiteSpace': 'normal', 'textAlign': 'left'
                            }
                        ),
                    ]
                ),
                
                # Society details section
                html.Div(
                    id='society-details-section',
                    children=[
                        html.H3('Society Details'),
                        dcc.Markdown(
                            id='society-details-text',
                            className='society-details-text'
                        ),
                    ]
                ),
            ],
            className='content-section'
        ),
        
        # Additional components and sections
        # ...

    ]
)

# Callbacks for updating the data table and society details based on the selected filters and rows
@app.callback(
    Output('data-table', 'data'),
    Output('data-table', 'columns'),
    Input('state-dropdown', 'value'),
    Input('district-dropdown', 'value'),
    Input('sector-dropdown', 'value')
)
def update_data_table(state, district, sector):
    filtered_df = df.copy()
    
    if state:
        filtered_df = filtered_df[filtered_df['State'].isin(state)]
    
    if district:
        filtered_df = filtered_df[filtered_df['District'].isin(district)]
    
    if sector:
        filtered_df = filtered_df[filtered_df['Sector Type'].isin(sector)]
    
    columns = [{'name': col, 'id': col} for col in filtered_df.columns]
    data = filtered_df.to_dict('records')
    
    return data, columns

@app.callback(
    Output('society-details-text', 'children'),
    Input('data-table', 'selected_rows')
)
def update_society_details(selected_rows):
    if selected_rows:
        society = df.iloc[selected_rows[0]]
        details = f"""
        **Society Name**: {society['Society Name']}
        **Society Address**: {society['Society Address']}
        **Date of Registration**: {society['Date of Registration']}
        **Area of Operation**: {society['Area of Operation']}
        **Sector Type**: {society['Sector Type']}
        """
    else:
        details = "No society selected"
    
    return details

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
# Define additional components, layouts, and callbacks as per your project's needs
# ...

# Define the layout of the dashboard
app.layout = html.Div(
    [
        # Header section
        html.Header(
            [
                html.H1('CRCS Portal Dashboard'),
                html.H3('Multistate Cooperative Societies Registration and Management'),
            ]
        ),
        
        # Filter section
        html.Div(
            [
                html.Label('Select State:'),
                dcc.Dropdown(
                    id='state-dropdown',
                    options=[
                        {'label': state, 'value': state} for state in df['State'].unique()
                    ],
                    multi=True,
                    placeholder='Select State'
                ),
                
                html.Label('Select District:'),
                dcc.Dropdown(
                    id='district-dropdown',
                    options=[
                        {'label': district, 'value': district} for district in df['District'].unique()
                    ],
                    multi=True,
                    placeholder='Select District'
                ),
                
                html.Label('Select Sector:'),
                dcc.Dropdown(
                    id='sector-dropdown',
                    options=[
                        {'label': sector, 'value': sector} for sector in df['Sector Type'].unique()
                    ],
                    multi=True,
                    placeholder='Select Sector'
                ),
            ],
            className='filter-section'
        ),
        
        # Main content section
        html.Div(
            [
                # Data table section
                html.Div(
                    id='data-table-section',
                    children=[
                        html.H3('Registered Societies'),
                        dash_table.DataTable(
                            id='data-table',
                            columns=[
                                {'name': col, 'id': col} for col in df.columns
                            ],
                            data=df.to_dict('records'),
                            style_table={'overflowX': 'scroll'},
                            style_cell={
                                'minWidth': '100px', 'width': '150px', 'maxWidth': '300px',
                                'whiteSpace': 'normal', 'textAlign': 'left'
                            }
                        ),
                    ]
                ),
                
                # Society details section
                html.Div(
                    id='society-details-section',
                    children=[
                        html.H3('Society Details'),
                        dcc.Markdown(
                            id='society-details-text',
                            className='society-details-text'
                        ),
                    ]
                ),
            ],
            className='content-section'
        ),
        
        # Additional components and sections
        # ...

    ]
)

# Callbacks for updating the data table and society details based on the selected filters and rows
@app.callback(
    Output('data-table', 'data'),
    Output('data-table', 'columns'),
    Input('state-dropdown', 'value'),
    Input('district-dropdown', 'value'),
    Input('sector-dropdown', 'value')
)
def update_data_table(state, district, sector):
    filtered_df = df.copy()
    
    if state:
        filtered_df = filtered_df[filtered_df['State'].isin(state)]
    
    if district:
        filtered_df = filtered_df[filtered_df['District'].isin(district)]
    
    if sector:
        filtered_df = filtered_df[filtered_df['Sector Type'].isin(sector)]
    
    columns = [{'name': col, 'id': col} for col in filtered_df.columns]
    data = filtered_df.to_dict('records')
    
    return data, columns

@app.callback(
    Output('society-details-text', 'children'),
    Input('data-table', 'selected_rows')
)
def update_society_details(selected_rows):
    if selected_rows:
        society = df.iloc[selected_rows[0]]
        details = f"""
        **Society Name**: {society['Society Name']}
        **Society Address**: {society['Society Address']}
        **Date of Registration**: {society['Date of Registration']}
        **Area of Operation**: {society['Area of Operation']}
        **Sector Type**: {society['Sector Type']}
        """
    else:
        details = "No society selected"
    
    return details

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
# Define additional components, layouts, and callbacks as per your project's needs
# ...

# Define the layout of the dashboard
app.layout = html.Div(
    [
        # Header section
        html.Header(
            [
                html.H1('CRCS Portal Dashboard'),
                html.H3('Multistate Cooperative Societies Registration and Management'),
            ]
        ),
        
        # Filter section
        html.Div(
            [
                html.Label('Select State:'),
                dcc.Dropdown(
                    id='state-dropdown',
                    options=[
                        {'label': state, 'value': state} for state in df['State'].unique()
                    ],
                    multi=True,
                    placeholder='Select State'
                ),
                
                html.Label('Select District:'),
                dcc.Dropdown(
                    id='district-dropdown',
                    options=[
                        {'label': district, 'value': district} for district in df['District'].unique()
                    ],
                    multi=True,
                    placeholder='Select District'
                ),
                
                html.Label('Select Sector:'),
                dcc.Dropdown(
                    id='sector-dropdown',
                    options=[
                        {'label': sector, 'value': sector} for sector in df['Sector Type'].unique()
                    ],
                    multi=True,
                    placeholder='Select Sector'
                ),
            ],
            className='filter-section'
        ),
        
        # Main content section
        html.Div(
            [
                # Data table section
                html.Div(
                    id='data-table-section',
                    children=[
                        html.H3('Registered Societies'),
                        dash_table.DataTable(
                            id='data-table',
                            columns=[
                                {'name': col, 'id': col} for col in df.columns
                            ],
                            data=df.to_dict('records'),
                            style_table={'overflowX': 'scroll'},
                            style_cell={
                                'minWidth': '100px', 'width': '150px', 'maxWidth': '300px',
                                'whiteSpace': 'normal', 'textAlign': 'left'
                            }
                        ),
                    ]
                ),
                
                # Society details section
                html.Div(
                    id='society-details-section',
                    children=[
                        html.H3('Society Details'),
                        dcc.Markdown(
                            id='society-details-text',
                            className='society-details-text'
                        ),
                    ]
                ),
            ],
            className='content-section'
        ),
        
        # Additional components and sections
        # ...

    ]
)

# Callbacks for updating the data table and society details based on the selected filters and rows
@app.callback(
    Output('data-table', 'data'),
    Output('data-table', 'columns'),
    Input('state-dropdown', 'value'),
    Input('district-dropdown', 'value'),
    Input('sector-dropdown', 'value')
)
def update_data_table(state, district, sector):
    filtered_df = df.copy()
    
    if state:
        filtered_df = filtered_df[filtered_df['State'].isin(state)]
    
    if district:
        filtered_df = filtered_df[filtered_df['District'].isin(district)]
    
    if sector:
        filtered_df = filtered_df[filtered_df['Sector Type'].isin(sector)]
    
    columns = [{'name': col, 'id': col} for col in filtered_df.columns]
    data = filtered_df.to_dict('records')
    
    return data, columns

@app.callback(
    Output('society-details-text', 'children'),
    Input('data-table', 'selected_rows')
)
def update_society_details(selected_rows):
    if selected_rows:
        society = df.iloc[selected_rows[0]]
        details = f"""
        **Society Name**: {society['Society Name']}
        **Society Address**: {society['Society Address']}
        **State**: {society['State']}
        **District**: {society['District']}
        **Date of Registration**: {society['Date of Registration']}
        **Area of Operation**: {society['Area of Operation']}
        **Sector Type**: {society['Sector Type']}
        """
    else:
        details = "No society selected."
    
    return details

# Additional callbacks and functionalities
# ...

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
# Import necessary libraries
import dash
from dash import dcc
from dash import html
import pandas as pd

# Load the dataset1.csv
df = pd.read_csv("dataset1.csv")

# Create the app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div(
    children=[
        html.H1("CRCS Dashboard"),
        html.Div(
            className="container",
            children=[
                html.Div(
                    className="sidebar",
                    children=[
                        html.H2("Filters"),
                        dcc.Dropdown(
                            id="state-dropdown",
                            options=[
                                {"label": state, "value": state}
                                for state in df["State"].unique()
                            ],
                            placeholder="Select a state",
                        ),
                        dcc.Dropdown(
                            id="district-dropdown",
                            placeholder="Select a district",
                        ),
                        dcc.Dropdown(
                            id="sector-dropdown",
                            options=[
                                {"label": sector, "value": sector}
                                for sector in df["Sector Type"].unique()
                            ],
                            placeholder="Select a sector",
                        ),
                    ],
                ),
                html.Div(
                    className="content",
                    children=[
                        html.Div(
                            className="summary",
                            children=[
                                html.H2("Summary"),
                                html.Div(id="summary-content"),
                            ],
                        ),
                        html.Div(
                            className="details",
                            children=[
                                html.H2("Details"),
                                html.Div(id="details-content"),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ]
)

# Define the callbacks
@app.callback(
    dash.dependencies.Output("district-dropdown", "options"),
    [dash.dependencies.Input("state-dropdown", "value")],
)
def update_district_dropdown(state):
    if state:
        districts = df[df["State"] == state]["District"].unique()
        options = [{"label": district, "value": district} for district in districts]
        return options
    else:
        return []

@app.callback(
    dash.dependencies.Output("summary-content", "children"),
    [
        dash.dependencies.Input("state-dropdown", "value"),
        dash.dependencies.Input("district-dropdown", "value"),
        dash.dependencies.Input("sector-dropdown", "value"),
    ],
)
def update_summary(state, district, sector):
    filtered_df = df
    if state:
        filtered_df = filtered_df[filtered_df["State"] == state]
    if district:
        filtered_df = filtered_df[filtered_df["District"] == district]
    if sector:
        filtered_df = filtered_df[filtered_df["Sector Type"] == sector]

    total_societies = len(filtered_df)
    summary = f"Total societies: {total_societies}"
    return summary

@app.callback(
    dash.dependencies.Output("details-content", "children"),
    [
        dash.dependencies.Input("state-dropdown", "value"),
        dash.dependencies.Input("district-dropdown", "value"),
        dash.dependencies.Input("sector-dropdown", "value"),
    ],
)
def update_details(state, district, sector):
    filtered_df = df
    if state:
        filtered_df = filtered_df[filtered_df["State"] == state]
    if district:
        filtered_df = filtered_df[filtered_df["District"] == district]
    if sector:
        filtered_df = filtered_df[filtered_df["Sector Type"] == sector]

    if len(filtered_df) > 0:
        details = []
        for _, society in filtered_df.iterrows():
            details.append(
                html.Div(
                    className="society-details",
                    children=[
                        html.H3(society["Society Name"]),
                        html.P(f"Society Address: {society['Society Address']}"),
                        html.P(f"Date of Registration: {society['Date of Registration']}"),
                        html.P(f"Area of Operation: {society['Area of Operation']}"),
                    ],
                )
            )
        return details
    else:
        return "No societies found."

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
# Import necessary libraries
import dash
from dash import dcc
from dash import html
import pandas as pd

# Load the dataset1.csv
df = pd.read_csv("dataset1.csv")

# Create the app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div(
    children=[
        html.H1("CRCS Dashboard"),
        html.Div(
            className="container",
            children=[
                html.Div(
                    className="sidebar",
                    children=[
                        html.H2("Filters"),
                        dcc.Dropdown(
                            id="state-dropdown",
                            options=[
                                {"label": state, "value": state}
                                for state in df["State"].unique()
                            ],
                            placeholder="Select a state",
                        ),
                        dcc.Dropdown(
                            id="district-dropdown",
                            placeholder="Select a district",
                        ),
                        dcc.Dropdown(
                            id="sector-dropdown",
                            options=[
                                {"label": sector, "value": sector}
                                for sector in df["Sector Type"].unique()
                            ],
                            placeholder="Select a sector",
                        ),
                    ],
                ),
                html.Div(
                    className="content",
                    children=[
                        html.Div(
                            className="summary",
                            children=[
                                html.H2("Summary"),
                                html.Div(id="summary-content"),
                            ],
                        ),
                        html.Div(
                            className="details",
                            children=[
                                html.H2("Details"),
                                html.Div(id="details-content"),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ]
)

# Define the callbacks
@app.callback(
    dash.dependencies.Output("district-dropdown", "options"),
    [dash.dependencies.Input("state-dropdown", "value")],
)
def update_district_dropdown(state):
    if state:
        districts = df[df["State"] == state]["District"].unique()
        options = [{"label": district, "value": district} for district in districts]
        return options
    else:
        return []

@app.callback(
    dash.dependencies.Output("summary-content", "children"),
    [
        dash.dependencies.Input("state-dropdown", "value"),
        dash.dependencies.Input("district-dropdown", "value"),
        dash.dependencies.Input("sector-dropdown", "value"),
    ],
)
def update_summary(state, district, sector):
    filtered_df = df
    if state:
        filtered_df = filtered_df[filtered_df["State"] == state]
    if district:
        filtered_df = filtered_df[filtered_df["District"] == district]
    if sector:
        filtered_df = filtered_df[filtered_df["Sector Type"] == sector]

    total_societies = len(filtered_df)
    summary = f"Total societies: {total_societies}"
    return summary

@app.callback(
    dash.dependencies.Output("details-content", "children"),
    [
        dash.dependencies.Input("state-dropdown", "value"),
        dash.dependencies.Input("district-dropdown", "value"),
        dash.dependencies.Input("sector-dropdown", "value"),
    ],
)
def update_details(state, district, sector):
    filtered_df = df
    if state:
        filtered_df = filtered_df[filtered_df["State"] == state]
    if district:
        filtered_df = filtered_df[filtered_df["District"] == district]
    if sector:
        filtered_df = filtered_df[filtered_df["Sector Type"] == sector]

    if len(filtered_df) > 0:
        details = []
        for _, society in filtered_df.iterrows():
            details.append(
                html.Div(
                    className="society-details",
                    children=[
                        html.H3(society["Society Name"]),
                        html.P(f"Society Address: {society['Society Address']}"),
                        html.P(f"Date of Registration: {society['Date of Registration']}"),
                        html.P(f"Area of Operation: {society['Area of Operation']}"),
                    ],
                )
            )
        return details
    else:
        return "No societies found."

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
