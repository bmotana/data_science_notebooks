# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash import callback
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
sites = spacex_df["Launch Site"].unique().tolist()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',options=[
                                    {'label': 'All Sites', 'value': 'ALL'},
                                    *[{'label': site,'value': site } for site in sites],
                                ],
                                value='ALL',
                                placeholder="place holder here",
                                searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                min=0, max=10000, step=1000,
                                marks={0: '0',
                                    2_500: "2500",
                                    5_000: "5000",
                                    7_500: "7500",
                                    10_000: '10000'},
                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@callback(
    Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total success Launches by site')
        return fig
    else:
       selected_site_data = filtered_df[filtered_df["Launch Site"] == entered_site]
       selected_site_data =  selected_site_data.groupby(["class"]).count().reset_index()
       fig = px.pie(selected_site_data, values='Flight Number',
        names='class',  title=f'Total success launches for site {entered_site}')
       return fig

print("something works")
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
    Input(component_id="payload-slider", component_property="value")])

def get_scatterplot(entered_site, entered_payload_range):
    print(entered_site, entered_payload_range)
    low, high = entered_payload_range
    filtered_df = spacex_df
    mask = (filtered_df['Payload Mass (kg)'] > low) & (filtered_df['Payload Mass (kg)'] < high)
    filtered_df = filtered_df[mask]
    if entered_site == 'ALL':
        fig2 = px.scatter(filtered_df, x="Payload Mass (kg)",
         y="class", color="Booster Version Category",
         title="Correletion Between Payload and Success for all Sites")
        return fig2 
    else:
       selected_site_data = filtered_df[filtered_df["Launch Site"] == entered_site]
       fig2 = px.scatter(selected_site_data, x="Payload Mass (kg)", y="class", color="Booster Version Category")
       return fig2

# Run the app
if __name__ == '__main__':
    app.run()
    
"""
Which site has the largest successful launches?
- KSC LC-39A
Which site has the highest launch success rate?
- CCAFS SLC-40
Which payload range(s) has the highest launch success rate?
- 2000 - 4000 kgs
Which payload range(s) has the lowest launch success rate?
- 4000 - 7000 kgs
Which F9 Booster version (v1.0, v1.1, FT, B4, B5, etc.) has the highest
launch success rate?
- FT
"""