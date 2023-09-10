from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import pandas as pd
import plotly.graph_objects as go
from scipy.stats import percentileofscore
from utils import custom_data, get_custom_data_index, labs, var_names, units, get_data
from assets.bootstrap import selectors_size


df = get_data()

# stylesheet with the .dbc class
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.CYBORG, dbc_css
    ],
    title='Romania Housing'
)
server = app.server
app.layout = dbc.Container(
    children=[
        html.Link(rel="stylesheet",
                  href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"),
        dbc.Row(
            html.H1("Romania Housing App",
                    style={
                        'display': 'flex',
                        'justify-content': 'center',
                        'text-align': 'center'
                    }
                    )
        ),
        dbc.Container(
            children=[
                dbc.Row(
                    id='selectors',
                    className='my-0 mx-2',
                    style={'display': 'flex', 'justify-content': 'center'},
                    children=[
                        dbc.Col(
                            children=[
                                html.H6("Property Type", style={
                                    'text-align': 'center'}),
                                dcc.RadioItems(
                                    options=list(df.property_type.unique()),
                                    value='apartment',
                                    inputStyle={"margin-right": "10px"},
                                    inline=False,
                                    id='property_type'
                                )
                            ],
                            **selectors_size
                        ),
                        dbc.Col(
                            children=[
                                html.H6("County", style={
                                    'text-align': 'center'}),
                                dcc.Dropdown(
                                    options=sorted(list(df.county.unique())),
                                    style={'min-width': '200px'},
                                    id='county',
                                    clearable=True,
                                    multi=True
                                )],
                            **selectors_size
                        )],
                ),
                dbc.Row(
                    id='selectors_2',
                    className='my-0 mx-2',
                    style={'display': 'flex', 'justify-content': 'center'},
                    children=[
                        dbc.Col(
                            children=[
                                html.H6("Variable", style={
                                    'text-align': 'center'}),
                                dcc.Dropdown(
                                    id='variable',
                                    options=[
                                        {'label': 'Net Area (m\u00b2)',
                                         'value': 'suprafata_utila'},
                                        {'label': 'Price (\N{euro sign})',
                                         'value': 'price'},
                                        {'label': 'Price (\N{euro sign}) per m\u00b2',
                                         'value': 'price_per_sqmeter'}
                                    ],
                                    value='price_per_sqmeter',

                                    clearable=False
                                )
                            ],
                            **selectors_size
                        ),
                        dbc.Col(
                            style={
                                'display': 'inline-block',
                                'justify-content': 'center',
                                'text-align': 'center'
                            },
                            className='my-3',
                            children=[
                                dbc.Col(children=[
                                    html.Div(
                                        id='slider_value'
                                    ),
                                    dcc.Input(
                                        type='range',
                                        min=0,
                                        max=20,
                                        step=1,
                                        id='variable_slider',
                                        className='my-0 mx-2',
                                        style={'width': '100%'},
                                    )
                                ],
                                ),
                            ],
                            **selectors_size
                        )
                    ]
                ),
                dbc.Row(
                    html.Div(
                        "Each point on the map is a property for sale. Click on a point to compare it with the selected data.",
                        style={'display': 'flex', 'justify-content': 'center'}
                    ),
                    className='my-0'
                ),
                dbc.Row(
                    style={'display': 'flex', 'justify-content': 'center',
                           'align-text': 'center'},
                    children=html.Div(
                        style={
                            'display': 'flex', 'justify-content': 'center', 'align-text': 'center'},
                        children=[
                            html.Div(children="No. of Properties",
                                     className='mx-2'),
                            html.Span(
                                id="property_count",
                                className="badge bg-info rounded-pill mx-2"
                            )
                        ]
                    ),
                    className='my-0'
                ),
                dbc.Container(  # plots
                    style={'display': 'flex', 'justify-content': 'center'},
                    children=[
                        dbc.Row(
                            id='plots',
                            style={'display': 'flex',
                                   'justify-content': 'center'},
                            className='vw-100',
                            children=[
                                dbc.Col(
                                    dcc.Graph(
                                        id='map',
                                    ),
                                    style={'display': 'flex',
                                           'justify-content': 'center'},
                                    xs=10,
                                    md=6,
                                ),
                                dbc.Col(
                                    dcc.Graph(
                                        id='ecdf',
                                        style={'display': 'flex',
                                               'justify-content': 'center'}
                                    ),
                                    xs=12,
                                    sm=12,
                                    md=6
                                )
                            ]
                        )
                    ]
                ),
                dbc.Row(
                    html.Table(
                        [html.Thead(
                            html.Tr(
                                [
                                    html.Th(children="Type", scope='col'),
                                    html.Th(children="County", scope='col'),
                                    html.Th(
                                        children="Price (\N{euro sign})", scope='col'),
                                    html.Th(
                                        children="Net Area (m\u00b2)", scope='col'),
                                    html.Th(
                                        children="Price per Sq. Meter (\N{euro sign}/m\u00b2)", scope='col'),
                                    html.Th(children="URL", scope='col')
                                ]
                            )
                        ),
                            html.Tbody(
                                html.Tr(id='table_row')
                            )
                        ],
                        className='table table-hover'
                    ),
                    className='my-3'
                ),
                html.Footer(
                    children=[
                        html.A(
                            [html.I(className='fa fa-linkedin')],
                            className="btn btn-link btn-floating btn-lg text-dark m-1",
                            href="https://www.linkedin.com/in/esdras-santos-a06444b8/",
                            role="button"
                        ),
                        html.A(
                            [html.I(className='fa fa-github')],
                            className="btn btn-link btn-floating btn-lg text-dark m-1",
                            href="https://github.com/EChristo23",
                            role="button"
                        )
                    ], style={'display': 'flex', 'justify-content': 'center'},
                    className='my-3'
                ),
                dcc.Store(id='intermediate-value')
            ]
        )
    ],
    fluid=True,
    className="dbc"
)


@callback(
    Output('slider_value', 'children'),
    Input('variable', 'value'),
    Input('variable_slider', 'value'),
)
def slider_value_update(input_variable, value):
    return str(value) + ' ' + units.get(input_variable)


@callback(
    Output('variable_slider', 'min'),
    Output('variable_slider', 'max'),
    Output('variable_slider', 'step'),
    Output('variable_slider', 'value'),
    Input('variable', 'value')
)
def slider_pars_update(input_variable):
    steps = {
        'price': 5000,
        'suprafata_utila': 10,
        'price_per_sqmeter': 100,
    }
    pars = [df[input_variable].min(), df[input_variable].max()]
    return pars[0], pars[1], steps.get(input_variable), pars[1]


@app.callback(
    Output('property_count', 'children'),
    Input('intermediate-value', 'data'),
    Input('map', 'selectedData')

)
def update_count(input_df, selection
                 ):
    input_df = pd.DataFrame.from_dict(input_df)
    if selection:
        ids = [i.get('customdata')[get_custom_data_index('id')]
               for i in selection.get('points')]
        input_df = input_df.loc[input_df.id.isin(ids)]
    return str(input_df.shape[0])


@app.callback(
    Output('intermediate-value', 'data'),
    [Input('county', 'value')],
    [Input('property_type', 'value')],
    Input('variable', 'value'),
    Input('variable_slider', 'value')
)
def property_count(county, property_type, input_variable, slider_value):
    input_df = df.copy(deep=True)
    if county:
        input_df = input_df[input_df['county'].isin(county)]

    if property_type:
        input_df = input_df[input_df['property_type'].isin([property_type])]

    if input_variable:
        if slider_value:
            input_df = input_df[input_df[input_variable]
                                <= float(slider_value)]

    return input_df.to_dict()


@callback(
    Output('map', 'figure'),
    Input('variable', 'value'),
    Input('intermediate-value', 'data')
)
def update_map(input_variable, input_df):
    #input_df = pd.DataFrame.from_dict(input_df)

    map_graph = px.scatter_mapbox(
        # title='''Romania's Map''',
        data_frame=input_df,
        lat="latitude",
        lon="longitude",
        hover_data={
            "property_type": True,
            "county": True,
            "city": True,
            "price_per_sqmeter": ':.2f',
            "price": True,
            "suprafata_utila": True,
            "latitude": False,
            "longitude": False
        },
        custom_data=custom_data,
        color=input_variable,
        color_continuous_scale=px.colors.sequential.Plasma_r,
        opacity=0.3,
        zoom=5,
        height=550,
        width=750,
        mapbox_style='carto-positron',
        template=load_figure_template('cyborg'),
        labels=labs,
        center={'lat': 46.0442, 'lon': 25.0094}
    ).update_traces(
        marker_colorbar_orientation="h",
        selector=dict(type='scattermapbox'),
        marker={
            'size': 12,
            'colorscale': 'Plasma'
        },
        hovertemplate='<b>' + labs.get('property_type') + ' </b>: %{customdata[1]}<br>' +
                      '<b>' + labs.get('county') + ' </b>: %{customdata[2]}<br>' +
                      '<b>' + labs.get('city') + ' </b>: %{customdata[7]}<br>' +
                      '<b>' + labs.get('price_per_sqmeter') + ' </b>: %{customdata[3]:.2f}<br>' +
                      '<b>' + labs.get('price') + ' </b>: %{customdata[4]:.2f}<br>' +
                      '<b>' + labs.get('suprafata_utila') + ' </b>: %{customdata[5]:.2f}<br>'
    ).update_layout(
        # coloraxis_showscale=False,
        legend=dict(yanchor="top", y=0.9, xanchor="left", x=0.4),
        transition_duration=500,
        paper_bgcolor='rgba(0,0,0,0)',
        # margin={'l': 25, 'r': 0, 'b': 0, 't': 25},
        title_x=0.5,
        title=dict(
            text="Romania's Map",
            x=0.5,
            y=0.925,
            xanchor='center',
            yanchor='top',
            # pad = dict(
            #            t = 0
            #           ),
            font=dict(

                # family='Courier New, monospace',
                # size=40,
                # color='#000000'
            )
        )
    )
    return map_graph


@callback(
    Output('ecdf', 'figure'),
    Input('variable', 'value'),
    Input('intermediate-value', 'data'),
    Input('map', 'clickData')
    #Input('map', 'selectedData')
)
def update_ecdf(input_variable, input_df, point#, selection
                ):
    filtered_df = pd.DataFrame.from_dict(input_df)
    # filtered_df = input_df
    # if selection:
    #     ids = [i.get('customdata')[get_custom_data_index('id')]
    #            for i in selection.get('points')]
    #     filtered_df = filtered_df.loc[filtered_df.id.isin(ids)]

    fig = px.ecdf(
        filtered_df,
        x=input_variable,
        template=load_figure_template('cyborg'),
        markers=True,
        lines=True,
        title="Cumulative Proportion by {variable}".format(
            variable=labs.get(input_variable)),
        hover_data=custom_data,
        height=550,
        width=750,
    ).update_layout(
        yaxis={'title': 'Cumulative Proportion (%)'},
        xaxis={'title': labs.get(input_variable)},
        yaxis_tickformat='.1%',
        # transition_duration=0,
        paper_bgcolor='rgba(0,0,0,0)',
        title_x=0.5
    )

    fig.update_traces(
        line_color='#7201a8',
        line={'width': 5},
        marker={
            'color': filtered_df[input_variable].sort_values(),
            'colorscale': 'Plasma_r',
            'size': 10
        },
        hovertemplate='A ' + var_names.get(input_variable) + ' of <b>%{x} ' + units.get(input_variable) +
                      '</b><br> is higher than <b>%{y}</b> of the properties selected.'
    )

    if point:  # check if there is a hover point
        point_id = point.get('points')[0].get('customdata')[
            get_custom_data_index('id')]
        if point_id in filtered_df.id.values:
            data = point.get('points')[0].get('customdata')[get_custom_data_index(input_variable)]
            x_coordinate = data
            y_coordinate = percentileofscore(filtered_df[input_variable], data) / 100
            if y_coordinate > 0.5:
                fig.add_trace(
                    go.Scatter(
                        x=[x_coordinate],
                        y=[y_coordinate],
                        # mode="markers",
                        marker=dict(
                            color='#d382fa',
                            size=20,
                        ),
                        mode="markers+text",
                        text=['A ' + var_names.get(input_variable) + ' of <b> ' + str(round(x_coordinate, 1)) + ' ' +
                              units.get(input_variable) + ' </b> <br> is <b>higher</b> than <b>' + str(
                            round(100 * y_coordinate, 1)) + '%</b> of the properties selected.'],
                        hoverinfo='text',
                        textposition="bottom right",
                        hovertext='A ' + var_names.get(input_variable) + ' of <b> ' + str(
                            round(x_coordinate, 1)) + ' ' + units.get(input_variable)
                                  + ' </b> <br> is higher than <b>' + str(
                            round(100 * y_coordinate, 1)) + '%</b> of the properties selected.',
                        showlegend=False
                    )
                )
            else:
                fig.add_trace(
                    go.Scatter(
                        x=[x_coordinate],
                        y=[y_coordinate],
                        # mode="markers",
                        marker=dict(
                            color='#d382fa',
                            size=20,
                        ),
                        mode="markers+text",
                        text=['A ' + var_names.get(input_variable) + ' of <b> ' + str(round(x_coordinate, 1)) + ' ' +
                              units.get(input_variable) + ' </b> <br> is <b>lower</b> than <b>' + str(
                            round(100 - (100 * y_coordinate), 1)) + '%</b> of the properties selected.'],
                        hoverinfo='text',
                        textposition="bottom right",
                        hovertext='A ' + var_names.get(input_variable) + ' of <b> ' + str(
                            round(x_coordinate, 1)) + ' ' +
                                  units.get(input_variable) + ' </b> <br> is <b>lower</b> than <b>' + str(
                            round(100 - (100 * y_coordinate), 1)) + '%</b> of the properties selected.',
                        showlegend=False
                    )
                )
    return fig


@app.callback(
    Output('table_row', 'children'),
    Input('map', 'clickData')
)
def table_row(clickdata):
    if clickdata:
        clickdata.get('points')[0].get('customdata')
        cols = ['property_type', 'county', 'price',
                'suprafata_utila', 'price_per_sqmeter']
        data = [clickdata.get('points')[0].get('customdata')[
                    get_custom_data_index(i)] for i in cols]
        row = [html.Td(children=cell) for cell in data]

        # URL
        row.append(
            html.Td(
                children=html.A(
                    'source',
                    href=clickdata.get('points')[0].get('customdata')[
                        get_custom_data_index('url')],
                    target='_blank'
                )
            )
        )
        return row


if __name__ == '__main__':
    app.run(debug=True)
