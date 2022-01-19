# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

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


def generate_table(dataframe, max_rows=10):
    return html.Table(
        [
            html.Thead(html.Tr([html.Th(col) for col in dataframe.columns])),
            html.Tbody(
                [
                    html.Tr([html.Td(dataframe.iloc[i][col]) for col in dataframe.columns])
                    for i in range(min(len(dataframe), max_rows))
                ]
            ),
        ]
    )


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

# app.layout = html.Div(
#     children=[
#         html.H1(children="P4 Football", style={"textAlign": "center", "color": black}),
#         html.H4(children=f"Classement au {date.today().strftime('%d/%m/%Y')} "),
#         generate_table(df.reset_index()),
#         html.Div(
#             children="""
#         Classement
#     """,
#             style={"textAlign": "center", "color": "black"},
#         ),
#         dcc.Graph(id="example-graph", figure=fig),
#     ]
# )

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
    # When the table is first rendered, `derived_virtual_data` and
    # `derived_virtual_selected_rows` will be `None`. This is due to an
    # idiosyncrasy in Dash (unsupplied properties are always None and Dash
    # calls the dependent callbacks when the component is first rendered).
    # So, if `rows` is `None`, then the component was just rendered
    # and its value will be the same as the component's dataframe.
    # Instead of setting `None` in here, you could also set
    # `derived_virtual_data=df.to_rows('dict')` when you initialize
    # the component.
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
