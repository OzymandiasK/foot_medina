import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

import pandas as pd

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?" "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

ranking_df = pd.read_csv("ranking.csv", sep=";")

available_indicators = ranking_df["EQUIPE"].unique()
# https://dash.plotly.com/basic-callbacks

app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        dcc.Dropdown(
                            id="xaxis-column",
                            options=[{"label": i, "value": i} for i in available_indicators],
                            value="Fertility rate, total (births per woman)",
                        ),
                        dcc.RadioItems(
                            id="xaxis-type",
                            options=[{"label": i, "value": i} for i in ["Linear", "Log"]],
                            value="Linear",
                            labelStyle={"display": "inline-block"},
                        ),
                    ],
                    style={"width": "48%", "display": "inline-block"},
                ),
                html.Div(
                    [
                        dcc.Dropdown(
                            id="yaxis-column",
                            options=[{"label": i, "value": i} for i in available_indicators],
                            value="Life expectancy at birth, total (years)",
                        ),
                        dcc.RadioItems(
                            id="yaxis-type",
                            options=[{"label": i, "value": i} for i in ["Linear", "Log"]],
                            value="Linear",
                            labelStyle={"display": "inline-block"},
                        ),
                    ],
                    style={"width": "48%", "float": "right", "display": "inline-block"},
                ),
            ]
        ),
        dcc.Graph(id="indicator-graphic"),
        dcc.Slider(
            id="year--slider",
            min=ranking_df["Year"].min(),
            max=ranking_df["Year"].max(),
            value=ranking_df["Year"].max(),
            marks={str(year): str(year) for year in ranking_df["Year"].unique()},
            step=None,
        ),
    ]
)


@app.callback(
    Output("indicator-graphic", "figure"),
    Input("xaxis-column", "value"),
    Input("yaxis-column", "value"),
    Input("xaxis-type", "value"),
    Input("yaxis-type", "value"),
    Input("year--slider", "value"),
)
def update_graph(xaxis_column_name, yaxis_column_name, xaxis_type, yaxis_type, year_value):
    ranking_dff = ranking_df[ranking_df["Year"] == year_value]

    fig = px.scatter(
        x=ranking_dff[ranking_dff["Indicator Name"] == xaxis_column_name]["Value"],
        y=ranking_dff[ranking_dff["Indicator Name"] == yaxis_column_name]["Value"],
        hover_name=ranking_dff[ranking_dff["Indicator Name"] == yaxis_column_name][
            "Country Name"
        ],
    )

    fig.update_layout(margin={"l": 40, "b": 40, "t": 10, "r": 0}, hovermode="closest")

    fig.update_xaxes(
        title=xaxis_column_name, type="linear" if xaxis_type == "Linear" else "log"
    )

    fig.update_yaxes(
        title=yaxis_column_name, type="linear" if yaxis_type == "Linear" else "log"
    )

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
