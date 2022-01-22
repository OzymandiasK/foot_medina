import dash
from dash import dcc
from dash import html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import date
from dash.dependencies import Input, Output
from dash import dash_table
from preproc_matches import melt_ranking_timeline

ranking_df = pd.read_csv("ranking.csv", sep=";", index_col="EQUIPE")
ranking_timeline = pd.read_csv("ranking_timeline.csv", sep=";")
melted_ranking_timeline = melt_ranking_timeline(ranking_timeline)

app = dash.Dash(__name__)
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.title = "Medina Forest"
app._favicon = "football.ico"

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

colors = {"background": "#111111", "text": "#FFFFFF"}

# fig = px.bar(
#     ranking_df.sort_values("PTS"),
#     x=ranking_df.index,
#     y="PTS",
#     color="J",
#     barmode="stack",
#     color_continuous_scale=px.colors.sequential.Sunsetdark,
# )

ranking_plot_line = px.line(
    melted_ranking_timeline,
    x=melted_ranking_timeline["Journée"],
    y=melted_ranking_timeline["PTS"],
    color=melted_ranking_timeline["Equipe"],
    title="Evolution du Classement",
)
ranking_plot_line.update_traces(line=dict(width=4))
# fig.update_layout(
#     plot_bgcolor=colors["background"],
#     paper_bgcolor=colors["background"],
#     font_color=colors["text"],
# )
app.layout = html.Div(
    [
        html.H1(
            "Medina Forest",
            style={"textAlign": "center", "color": "#000000", "fontFamily": "lato"},
        ),
        dash_table.DataTable(
            id="datatable-interactivity",
            columns=[
                {"name": i, "id": i, "deletable": False, "selectable": True}
                for i in ranking_df.reset_index().columns
            ],
            data=ranking_df.reset_index().to_dict("records"),
            editable=True,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            column_selectable="single",
            row_selectable="multi",
            row_deletable=False,
            selected_columns=[],
            selected_rows=[],
            page_action="native",
            page_current=0,
            page_size=12,
        ),
        html.Div(id="datatable-interactivity-container"),
        html.Div(
            [
                dcc.Checklist(
                    id="checklist",
                    options=[
                        {"label": x, "value": x}
                        for x in melted_ranking_timeline["Equipe"].unique()
                    ],
                    labelStyle={"display": "inline-block"},
                ),
                dcc.Graph(figure=ranking_plot_line, id="line-chart"),
            ]
        ),
    ]
)


@app.callback(
    Output("datatable-interactivity", "style_data_conditional"),
    Input("datatable-interactivity", "selected_columns"),
)
def update_styles(selected_columns):
    return [{"if": {"column_id": i}, "background_color": "#D2F3FF"} for i in selected_columns]


@app.callback(
    Output("datatable-interactivity-container", "children"),
    Input("datatable-interactivity", "derived_virtual_data"),
    Input("datatable-interactivity", "derived_virtual_selected_rows"),
)
def update_graphs(rows, derived_virtual_selected_rows):

    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    ranking_dff = ranking_df.reset_index() if rows is None else pd.DataFrame(rows)

    colors = [
        "#7FDBFF" if i in derived_virtual_selected_rows else "#0074D9"
        for i in range(len(ranking_dff))
    ]
    ranking_dff_sorted = ranking_dff.sort_values(by="PTS", ascending=True)
    return [
        dcc.Graph(
            id="column",
            figure={
                "data": [
                    {
                        "title": "Classement et nombre de matches joués",
                        "x": ranking_dff_sorted["EQUIPE"],
                        "y": ranking_dff_sorted["PTS"],
                        "type": "bar",
                        "text": ranking_dff_sorted["J"],
                        "textposition": "auto",
                        "marker": {"color": colors},
                    }
                ],
                "layout": {
                    "xaxis": {"automargin": True},
                    "yaxis": {
                        "automargin": True,
                        "title": {"text": ranking_dff_sorted.columns},
                    },
                    "height": 250,
                    "margin": {"t": 10, "l": 10, "r": 10},
                },
            },
        )
    ]


@app.callback(Output("line-chart", "figure"), [Input("checklist", "value")])
def update_line_chart(value):
    mask = ranking_timeline.index.isin(value)
    fig = px.line(ranking_timeline[mask], x="year", y="lifeExp", color="country")
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
