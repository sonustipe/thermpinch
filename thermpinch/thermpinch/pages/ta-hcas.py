########## diagrams$$$$$$$$$$$$

import os
import dash
import pandas as pd
from dash import Dash, Input, Output, State, dcc, html
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


PAGE_TITLE = "Heat cascade analysis"


class PageIDs:
    def __init__(self) -> None:
        # Get the base name of the file where this instance is created
        filename = os.path.basename(__file__)
        # Remove the file extension to use only the file name as the prefix
        prefix: Final[str] = filename.replace(".py", "")
        self.prefix: Final[str] = prefix
        self.status: Final[str] = f"{prefix}_status"
        self.outputdata_hcas: Final[str] = f"{prefix}_outputdata_hcas"
        self.runpinch_hcas: Final[str] = f"{prefix}_runpinch_hcas"
        self.runpinch: Final[str] = f"{prefix}_runpinch"


ids = PageIDs()


layout = html.Div(
    [
        html.H1("pinch", className="app-title"),
        html.H2(PAGE_TITLE, className="page-title"),
        html.Hr(),
        html.Div(
            "The heat cascade details the enthalpy balance at each interval, showing how heat is transferred from one temperature level to another."
        ),
        html.Br(),
        html.Div(
            "This is used to identify energy deficits or surpluses, helping to pinpoint where heating or cooling utilities are required. The cascade is crucial for finding the pinch point, which determines the maximum achievable heat recovery."
        ),
        html.Br(),
        html.Div(
            "Minimum Cold Utility (Q꜀ₘᵢₙ) and Minimum Hot Utility (Qₕₘᵢₙ):  These values represent the minimum amounts of external cooling (Q꜀ₘᵢₙ) and heating (Qₕₘᵢₙ) required to meet the process needs after maximizing heat recovery.They directly impact operational costs. By determining these minimum utility requirements, engineers can design processes that use energy more efficiently and reduce utility costs."
        ),
        # html.Div(id="pinch_results", style={"margin-top": "20px"}),
        ButtonCustom(label="Run PyPinch Analysis", id="runpinch_hcas").layout,
        dcc.Loading(
            id="loading", children=[html.Div(id="outputdata_hcas")], type="default"
        ),
    ]
)


@app.callback(Output("outputdata_hcas", "children"), [Input("runpinch_hcas", "n_clicks")])
def run_pinch_analysis(n_clicks):
    csv_file_path = os.path.join(os.getcwd(), "pinch_analysis_data.csv")

    if n_clicks and os.path.exists(csv_file_path):
        try:
            # Run the PyPinch analysis
            options = {"draw"}
            pinch = PyPinch(csv_file_path, options)
            pinch.showHeatCascade()
            # pinch.constructTemperatureInterval()

            # Save the plot as a base64 image
            buffer = BytesIO()
            plt.savefig(buffer, format="png")
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.read()).decode("utf-8")

            return html.Div(
                [
                    html.H3("PyPinch Analysis Complete"),
                    html.Img(
                        src="data:image/png;base64,{}".format(image_base64),
                        style={"width": "60%", "height": "auto"},
                    ),
                ]
            )
        except Exception as e:
            return html.Div(
                [html.H3("An error occurred while running PyPinch:"), html.P(str(e))]
            )

    return html.Div()
