import dash
from dash import dcc
from dash import html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import date
from dash.dependencies import Input, Output
from dash import dash_table

df = pd.read_csv("ranking.csv", sep=";", index_col="EQUIPE")
# df = df.drop(labels="PARKING BRUSSELS")

app = dash.Dash(__name__)
app.title = "Medina Forest"
app._favicon = "football.ico"

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

colors = {"background": "#111111", "text": "#FFFFFF"}

fig = px.bar(
    df.sort_values("PTS"),
    x=df.index,
    y="PTS",
    color="J",
    barmode="stack",
    color_continuous_scale=px.colors.sequential.Sunsetdark,
)
# fig.update_layout(
#     plot_bgcolor=colors["background"],
#     paper_bgcolor=colors["background"],
#     font_color=colors["text"],
# )
black = "#000000"

app.layout = html.Div(
    [
        html.H1(
            "Medina Forest",
            style={"textAlign": "center", "color": black, "fontFamily": "lato"},
        ),
        dash_table.DataTable(
            id="datatable-interactivity",
            columns=[
                {"name": i, "id": i, "deletable": False, "selectable": True}
                for i in df.reset_index().columns
            ],
            data=df.reset_index().to_dict("records"),
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

    dff = df.reset_index() if rows is None else pd.DataFrame(rows)

    colors = [
        "#7FDBFF" if i in derived_virtual_selected_rows else "#0074D9" for i in range(len(dff))
    ]

    return [
        dcc.Graph(
            id="column",
            figure={
                "data": [
                    {
                        "x": dff["EQUIPE"],
                        "y": dff["J"],
                        "type": "bar",
                        "marker": {"color": colors},
                    }
                ],
                "layout": {
                    "xaxis": {"automargin": True},
                    "yaxis": {"automargin": True, "title": {"text": dff.columns}},
                    "height": 250,
                    "margin": {"t": 10, "l": 10, "r": 10},
                },
            },
        )
    ]


if __name__ == "__main__":
    app.run_server(debug=True)
