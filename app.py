import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px


#-------------------------------------------------Importing Data-------------------------------------------------------------


#------Movements------------------------------------------------
mov = pd.read_csv("mov.csv")

#-------------Demographic--------------------------------#
demo = pd.read_excel("demo2.xlsx", engine='openpyxl')
clean_demo = pd.read_csv("clean_demo.csv")

demo_sex =pd.read_csv("demo_sex.csv")
demo_age =pd.read_csv("demo_age.csv")

#--------Top Countries --------------------
top_movements=pd.read_csv("top_movements.csv")


#----------------------------------------------Dropdowns, Slicer and Radio  -----------------------------------------------------------------

country_options = [dict(label="Country: "+str(country), value=country) for country in ["Total"]+demo['Country'].unique()]

year_options = [dict(label=year, value=year) for year in demo["Year"].unique()]

top_options = [dict(label="Top "+str(top)+" Countries", value=top) for top in np.arange(2,16)]

segment_options=[dict(label=str(seg)+" Countries", value=seg) for seg in ["Origin", "Asylum"]]

segment_options2=[dict(label=seg, value=seg) for seg in ["Origin", "Asylum"]]

sex_group_options=[dict(label=group, value=group) for group in ["By Gender", "By Age Group"]]

top_options_flows= [dict(label="Top "+str(top)+" Movements", value=top) for top in np.arange(1,11)]


all_options = {
    'Continent': [i for i in mov["Asylum Continent"].unique() if i!= "Unknown"],
    'Region': [i for i in mov["Asylum Region"].unique() if i!= "Unknown"]
}

choice1= dcc.RadioItems(
        id='choice1',
        options=[{'label': k, 'value': k} for k in all_options.keys()],
        value='Continent'
    )

choice2= dcc.Dropdown(id='choice2', multi=True)


dropdown_country = dcc.Dropdown(
        id='country_drop',
        options=country_options,
        value='Afghanistan',
        multi=False
    )

dropdown_sex_group= dcc.Dropdown(
        id ="sex_group_drop",
        options=sex_group_options,
        value="By Gender",
        multi=False
)

dropdown_segment = dcc.Dropdown(
    id="segment_drop",
    options= segment_options,
    value="Origin",
    multi=False
)


dropdown_segment_2 = dcc.Dropdown(
    id="segment_drop_2",
    options= segment_options2,
    value="Origin",
    multi=False
)

dropdown_top = dcc.Dropdown(
        id='top_drop',
        options=top_options,
        value=5,
        multi=False
    )

dropdown_top_2 = dcc.Dropdown(
        id='top_drop_2',
        options=top_options_flows,
        value=5,
        multi=False
    )

slider_year = dcc.Slider(
        id='year_slider',
        min=2001,
        max=2019,
        marks={str(i): '{}'.format(str(i)) for i in demo["Year"].unique()},
        step=1,
        value=2001,
        included=False
    )

slider_year_2 = dcc.Slider(
        id='year_slider_2',
        min=2001,
        max=2019,
        marks={str(i): '{}'.format(str(i)) for i in demo["Year"].unique()},
        step=1,
        value=2001,
        included=False
    )


slider_year_3 = dcc.Slider(
        id='year_slider_3',
        min=2001,
        max=2019,
        marks={str(i): '{}'.format(str(i)) for i in demo["Year"].unique()},
        step=1,
        value=2001,
        included=False
    )

slider_year_4 = dcc.Slider(
        id='year_slider_4',
        min=2001,
        max=2019,
        marks={str(i): '{}'.format(str(i)) for i in demo["Year"].unique()},
        step=1,
        value=2001,
        included=False
    )



slider_range_year = dcc.RangeSlider(
        id='year_range_slider',
        min=demo['Year'].min(),
        max=demo['Year'].max(),
        marks={str(i): '{}'.format(str(i)) for i in demo["Year"].unique()},
        value=[demo['Year'].min(), demo["Year"].max()],
        step=1
    )


#---------------------------------------------------------APP----------------------------------------------------------

app = dash.Dash(__name__, external_stylesheets='')

server = app.server

app.layout = html.Div([html.Div([html.H2("Refugees in the 21st Century: The Tale of a Never-Ending Journey")], style={ "text-align": "center"}, className="box"),
                        dcc.Tabs(id='tabs', value='tab-1', children=[
                                                                    dcc.Tab(label='Refugees, from where and to where?', value='tab-1'),
                                                                    dcc.Tab(label='What routes do Refugees take?', value='tab-2'),
                                                                    dcc.Tab(label="Who are the Refugees?", value='tab-3')

                                                                        ]),
                        html.Div(id='tabs_content'),

])
#------------------------------------------------- -------------------------------------------------------------------
@app.callback(
    [Output("choropleth", "figure"),
        Output("bar_top", "figure")
        ],
        [Input("year_slider", "value"),
         Input("top_drop","value"),
         Input ("segment_drop", "value")
    ]

)

def plots_1 (year, top, segment):

    #Origin/Asylum Map  top_movements
    df_movs= top_movements[top_movements["Year_"+str(segment)]==year]
    log_values= np.log(df_movs["Refugees_"+str(segment)])

    data_choropleth= dict(type="choropleth",
                                  locations=df_movs["Country of "+(str(segment).lower())+" (ISO)"],
                                  z=log_values,
                                  locationmode="ISO-3",
                                  text= df_movs[['Country of '+(str(segment).lower()), "Refugees_"+str(segment)]] ,
                                  colorscale='teal',
                                  hovertemplate='Country: %{text[0]} <br>'+ "Non-scaled value: %{text[1]} <br>"+'Log-scaled Value: %{z}',
                                  name='',
                                colorbar={'title': '(Log Scale)'}
                                  )
    layout_choropleth = dict(geo=dict(scope='world',
                                             projection=dict(type='equirectangular'),
                                             lakecolor='white',
                                             landcolor='white',
                                             showocean=True,  # default = False
                                             oceancolor='azure',
                                             bgcolor='#f9f9f9'
                                             ),
                                    margin=dict(t=0, b=0, l=0, r=0),
                                    hovermode="x",
                                    paper_bgcolor='#f9f9f9'
                                    )


    #Top Bar Plots

    top_movs= df_movs[df_movs["Year_"+str(segment)]==year].sort_values(by="Refugees_"+str(segment), ascending=False).head(top)
    top_movs["Country of "+(str(segment).lower())]=top_movs["Country of "+(str(segment).lower())].apply(lambda x: x+"  ")
    countries=top_movs["Country of "+(str(segment).lower())].values.tolist()
    values=top_movs["Refugees_"+str(segment)].values.tolist()

    data_top= dict(type="bar", x=values[::-1], y=countries[::-1], orientation="h", marker = { "color" : "steelblue"}
                         )
    layout_top = dict(xaxis=dict(title='Number of Refugees'),
                      paper_bgcolor='#f9f9f9',
                      plot_bgcolor='#f9f9f9'
                     )


    return go.Figure(data=data_choropleth, layout=layout_choropleth), \
           go.Figure(data=data_top, layout=layout_top)



@app.callback(
    Output('choice2', 'options'),
    Input('choice1', 'value'))

def set_sub_choice_options(selected_country):
    return [{'label': i, 'value': i} for i in all_options[selected_country]]

@app.callback(
    Output('choice2', 'value'),
    Input('choice2', 'options'))

def set_sub_choice_value(available_options):
    return available_options[0]['value']


@app.callback(
    Output("sankey", "figure"),
    [Input("segment_drop_2", "value"),
    Input('choice1', 'value'),
    Input('choice2', 'value'),
    Input("year_slider_3", "value")])

def plots_2 (segment, choice1, choice2, year):

    if segment == "Origin":
    #Sankey Graph Origin
        if choice1 == "Continent":
            df_flows = mov[(mov["Year"] == year) & (
                (mov["Origin Continent"] != 'Unknown') & (mov["Asylum Continent"] != 'Unknown'))].groupby(
            ["Origin Continent", "Asylum Continent"])["Refugees"].sum().sort_values(ascending=False).to_dict()

        elif choice1 == "Region":
            df_flows = mov[(mov["Year"] == year) & (
                (mov["Origin Region"] != 'Unknown') & (mov["Asylum Region"] != 'Unknown'))].groupby(
            ["Origin Region", "Asylum Region"])["Refugees"].sum().sort_values(ascending=False).to_dict()


        origin=[]
        destiny=[]
        values=[]
        for i, v in enumerate(df_flows.keys()):
            if v[0] in choice2:
                origin.append(v[0])
                destiny.append(v[1])
                values.append(df_flows[(v[0], v[1])])

        indices_origin = {}
        for index, value in enumerate(origin):
            if value not in indices_origin.keys():
                indices_origin[value] = index

        indices_destiny = {}
        for index, value in enumerate(destiny):
            if value not in indices_destiny.keys():
                indices_destiny[value] = index

        data=[go.Sankey(
        node = dict(
         pad = 30,
         thickness = 20,
         line = dict(color = "silver", width = 0.5),
         label = origin+destiny,
         color="lightgrey"
        ),
        link = dict(
         source = [indices_origin[i] for i in origin],
         target = [indices_destiny[i]+len(origin) for i in destiny],
         value = values,
          color=['steelblue', "dodgerblue", "silver", "skyblue", "lightsteelblue", "dodgerblue", "lightpink", "plum",
              "silver", "thistle", "lightgrey", "salmon"]
    ))]

        return go.Figure(data, layout={"paper_bgcolor":'#f9f9f9'})


    # Sankey Graph Asylum
    if segment=="Asylum":

        if choice1 == "Continent":
            df_flows= mov[(mov["Year"] == year) & (
                (mov["Origin Continent"] != 'Unknown') & (mov["Asylum Continent"] != 'Unknown'))].groupby(
            ["Origin Continent", "Asylum Continent"])["Refugees"].sum().sort_values(ascending=False).to_dict()


        elif choice1 == "Region":
            df_flows = mov[(mov["Year"] == year) & (
                (mov["Origin Region"] != 'Unknown') & (mov["Asylum Region"] != 'Unknown'))].groupby(
            ["Origin Region", "Asylum Region"])["Refugees"].sum().sort_values(ascending=False).to_dict()

        origin = []
        destiny = []
        values = []

        for i, v in enumerate(df_flows.keys()):
            if v[1] in choice2:
                origin.append(v[0])
                destiny.append(v[1])
                values.append(df_flows[(v[0], v[1])])

        indices_origin = {}
        for index, value in enumerate(origin ):
            if value not in indices_origin .keys():
                indices_origin [value] = index

        indices_destiny  = {}
        for index, value in enumerate(destiny ):
            if value not in indices_destiny.keys():
                indices_destiny [value] = index

        data= [go.Sankey(
            node=dict(
                pad=30,
                thickness=20,
                line=dict(color="silver", width=0.5),
                label=origin + destiny ,
                color="lightgrey"
            ),
            link=dict(
                source=[indices_origin[i] for i in origin ],
                target=[indices_destiny[i] + len(origin ) for i in destiny ],
                value=values,

                 color=['steelblue', "dodgerblue", "silver", "skyblue", "lightsteelblue", "dodgerblue", "lightpink", "plum",
                    "silver", "thistle", "lightgrey", "salmon"]
            ))]

        return go.Figure(data, layout={"paper_bgcolor":'#f9f9f9'})




@app.callback(
        [Output("sunburst_demo", "figure"),
         Output("time_series_demo", "figure")]
        ,

        [Input("year_slider_2", "value"),
         Input("country_drop", "value"),
         Input("year_range_slider", "value"),
         Input("sex_group_drop", "value")
    ]

)

def plots_3 (year, country, years, sex_group):
    # Sunburst_Demographic
    fig_sun=px.sunburst(data_frame=clean_demo[(clean_demo["Year"] == year) & (clean_demo["Country"] == country)],
                path=['Children/Adults', "Sex"],
                values='Population',
                hover_data={"Population": True, "Children/Adults": False, "Sex": False},
               color_discrete_sequence=["steelblue", "lightblue"]
             )

    fig_sun.update_traces(textinfo="label+percent entry", hoverinfo='none')
    fig_sun.update_layout(paper_bgcolor='#f9f9f9')

    #Time Series Demographic

    if sex_group=="By Gender":
        fig_line = px.line(x="Year",
                  y=demo_sex[(demo_sex["Country"] == country) &(demo_sex['Year']>=years[0]) & (demo_sex["Year"]<=years[1])]["Population"],
                  data_frame=demo_sex[(demo_sex["Country"] == country) &(demo_sex['Year']>=years[0]) & (demo_sex["Year"]<=years[1])],
                  color="Sex",
                  labels={"y": "Number of Refugees"
                          },
                 color_discrete_sequence=px.colors.qualitative.Set1
                  )
        fig_line.update_layout(plot_bgcolor='#f9f9f9',
                           paper_bgcolor='#f9f9f9')

    elif sex_group == "By Age Group":
        fig_line = px.line(x="Year",
                           y=demo_age[(demo_age["Country"] == country) & (demo_age['Year'] >= years[0]) & (
                                       demo_age["Year"] <= years[1])]["Population"],
                           color="Adults/Children",
                           data_frame=demo_age[(demo_age["Country"] == country) & (demo_age['Year'] >= years[0]) & (
                                       demo_age["Year"] <= years[1])],
                           labels={"y": "Number of Refugees",
                                   },
                           color_discrete_sequence=px.colors.qualitative.Set1
                           )
        fig_line.update_layout(plot_bgcolor='#f9f9f9',
                               paper_bgcolor='#f9f9f9')

    return go.Figure(fig_sun), \
            go.Figure(fig_line)


@app.callback (Output('tabs_content', 'children'),
              [Input('tabs', 'value')])

def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
                         html.Div([html.Div([html.H4("Do you want to analyse the countries of origin or asylum?")], className="smallbox"),
                                    html.Div([
                                            html.Div([""],style={"width":"33%"}),
                                            html.Div([dropdown_segment], style= {'width': '33%',"text-align": "center"}),
                                            html.Div([""], style={"width":"33%"})],
                                                                                    style={"display":"flex"}
                                            )
                                    ], style={"margin-bottom":"2%"}),

                         html.Div([html.Div([html.H4("Which year do you wish to analyse?")], className="smallbox"),
                                    html.Div([slider_year])], style={"margin-bottom":"3%"}
                                 ),
                        html.Div([html.Div([html.H4("Here, you can understand better the global distribution of the Refugees."),
                                            dcc.Graph(id="choropleth")
                                            ], style={"width":"47%"}, className="box"),
                                  html.Div(" ", style={"width":"6%"}),
                                  html.Div([html.Div([html.H4("Select how many top countries you want to visualize.")]),
                                            html.Div([html.Div([""], style={"width":"33%"}),
                                                      html.Div([dropdown_top], style={"width": "33%", "text-align": "center"}),
                                                      html.Div([""], style={"width": "33%"})],
                                                                                            style={"display":"flex"}),

                                            html.Div([dcc.Graph(id="bar_top")])
                                            ], style={"width":"47%"}, className="box")
                                    ],
                                   style={"display" : "flex"}
                                 )
                        ])

    elif tab == 'tab-3':
        return html.Div([html.Div([html.H4("Please choose which country you wish to analyse.")], className="smallbox"),
                         html.Div([html.Div([" "], style={"width":"33%"}),
                                   html.Div([dropdown_country], style={"width":"33%", "text-align": "center"}),
                                   html.Div([" "], style={"width":"33%"})
                                  ], style={"display":"flex"}),
                         html.Div([html.Div([html.H4(["Select the year for which you want to see the distribution of gender and age groups."], style={"text-align": "center" }),
                                            html.Div([html.Div([""], style={"width":"5%"}),
                                                      slider_year_2,
                                                      html.Div([""], style={"width": "5%"})
                                                         ]),
                                             dcc.Graph(id="sunburst_demo")], className="box", style={"width":"50%"}),
                                   html.Div([html.Div([html.H4(["Select the range of years you want to see the evolution of the number of Refugees, and if you want to see it by gender or age group."], style={"text-align": "center" }),
                                                      html.Div([""], style={"width":"5%"}),
                                                      slider_range_year,
                                                      html.Div([""], style={"width": "5%"})
                                                        ]),
                                             html.Div([html.Div([" "], style={"width": "33%"}),
                                                      html.Div([dropdown_sex_group],
                                                      style={"width": "33%", "text-align": "center"}),
                                             html.Div([" "], style={"width": "33%"}) ], style={"display":"flex"}),

                                             dcc.Graph(id="time_series_demo")], style={"width":"50%"}, className="box"

                                            )

                                  ], style={"display":"flex"})
                       ])


    elif tab == 'tab-2':
        return html.Div([html.Div([html.H4(["Select if you want to analyse by origin or asylum location and for which year."])], className = "smallbox"),
                        html.Div([html.Div([" "], style={"width": "33%"}),
                                 html.Div([dropdown_segment_2], style={"width": "33%", "text-align": "center"}),
                                 html.Div([" "], style={"width": "33%"})], style={"display":"flex"}),
                         html.Div([html.Div([" "], style={"width": "15%"}),
                                 html.Div([slider_year_3], style={"width": "70%"}),
                                 html.Div([" "], style={"width": "15%"})], style={"display":"flex"}),
                        html.Div([html.H4(["Select if you want to visualize the routes between continents or regions, and which ones you intend to visualize."])], className="smallbox"),
                         html.Div([html.Div([" "], style={"width": "33%"}),
                                    html.Div([choice1], style={"width": "33%", "text-align": "center"}),
                                     html.Div([" "], style={"width": "33%"})], style={"display": "flex"}),
                         html.Div([html.Div([" "], style={"width": "33%"}),
                                   html.Div([choice2], style={"width": "33%", "text-align": "center"}),
                                   html.Div([" "], style={"width": "33%"})], style={"display": "flex"}),
                         html.Div([html.Div([" "], style={"width": "5%"}),
                                   html.Div([dcc.Graph(id="sankey")], style={"width": "90%"}, className="box"),
                                   html.Div([" "], style={"width": "5%"})], style={"display": "flex"})


                         ])


if __name__ == '__main__':
    app.run_server(debug=True)
