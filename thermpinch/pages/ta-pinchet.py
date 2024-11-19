import os
import dash
import pandas as pd
from dash import Dash, Input, Output, State, dcc, html, dash_table
from dash.exceptions import PreventUpdate
from dash_ag_grid.AgGrid import AgGrid
from collections import namedtuple
from typing import Final
from PyPinch import PyPinch
from io import BytesIO
import matplotlib.pyplot as plt
import base64

import traceback
import math

from agility.components import (
    ButtonCustom,
    InputCustom,
    MessageCustom,
    DropdownCustom,
    CheckboxCustom,
    DisplayField,
    ContainerCustom,
)

from thermpinch.config.main import STORE_ID
from thermpinch.project import page2
from thermpinch.schemas.page2 import Page2Input, generate_table_record

from typing import Final

dash.register_page(__name__)
app: Dash = dash.get_app()


PAGE_TITLE = "Pinch Temperature"


class PageIDs:
    def __init__(self) -> None:
        # Get the base name of the file where this instance is created
        filename = os.path.basename(__file__)
        # Remove the file extension to use only the file name as the prefix
        prefix: Final[str] = filename.replace(".py", "")
        self.prefix: Final[str] = prefix
        self.status: Final[str] = f"{prefix}_status"
        self.output_datanii: Final[str] = f"{prefix}_output_datanii"
        self.run_pinch_csv: Final[str] = f"{prefix}_run_pinch_csv"


ids = PageIDs()


layout = html.Div(
    [
        # html.Div(id="pinch_results", style={"margin-top": "20px"}),
        html.H1("pinch", className="app-title"),
        html.H2(PAGE_TITLE, className="page-title"),
        html.Hr(),
        html.Div(
            'The pinch point is the temperature level where the process is most constrained thermally, meaning no further heat exchange can occur without violating \u0394Tₘᵢₙ. The pinch point is critical for targeting maximum heat recovery. It divides the process into distinct "above pinch" and "below pinch" regions, guiding the placement of heat exchangers for optimal energy recovery.'
        ),
        html.Br(),
        ButtonCustom(label="Pinch Point", id="run_pinch_csv").layout,
        dcc.Loading(
            id="loading", children=[html.Div(id="output_datanii")], type="default"
        ),
    ]
)


@app.callback(
    Output("output_datanii", "children"), [Input("run_pinch_csv", "n_clicks")]
)
def run_csv_pinch_analysis(n_clicks):
    csv_file_path = os.path.join(os.getcwd(), "pinch_analysis_data.csv")

    if n_clicks and os.path.exists(csv_file_path):
        try:
            # Run the PyPinch analysis with CSV option
            # Run the PyPinch analysis
            options = {"dataframe"}
            pinchen = PyPinch(csv_file_path, options)
            pinchen.solve(options)

            # Get the DataFrame with pinch results
            pinch_df = pinchen.printpinchdf()

            # Display the DataFrame as a Dash DataTable
            return html.Div(
                [
                    html.H3("Pinch Analysis Results"),
                    dash_table.DataTable(
                        data=pinch_df.to_dict("records"),
                        columns=[{"name": col, "id": col} for col in pinch_df.columns],
                        style_table={"width": "50%", "margin": "auto"},
                        style_header={
                            "backgroundColor": "rgb(230, 230, 230)",
                            "fontWeight": "bold",
                        },
                        style_cell={"textAlign": "center", "padding": "5px"},
                    ),
                ]
            )

        except Exception as e:
            return html.Div(
                [
                    html.H3("An error occurred while running the CSV Pinch analysis:"),
                    html.P(str(e)),
                ]
            )

    return html.Div()
