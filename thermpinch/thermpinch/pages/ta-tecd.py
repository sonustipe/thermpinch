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


PAGE_TITLE = "Temperature-Enthalpy Composite Diagram"


class PageIDs:
    def __init__(self) -> None:
        # Get the base name of the file where this instance is created
        filename = os.path.basename(__file__)
        # Remove the file extension to use only the file name as the prefix
        prefix: Final[str] = filename.replace(".py", "")
        self.prefix: Final[str] = prefix
        self.status: Final[str] = f"{prefix}_status"
        self.outputdata_tecd: Final[str] = f"{prefix}_outputdata_tecd"
        self.runpinch_tecd: Final[str] = f"{prefix}_runpinch_tecd"
        self.runpinch: Final[str] = f"{prefix}_runpinch"


ids = PageIDs()


layout = html.Div(
    [
        html.H1("pinch", className="app-title"),
        html.H2(PAGE_TITLE, className="page-title"),
        html.Hr(),
        html.Div(
            "Based on the Shifted Composite diagram, the Actual Temperature-Enthalpy Composite Diagram can be constructed: the hot streams have their temperatures shifted up by \u0394Tₘᵢₙ/2 and the cold streams have their temperatures shifted down by \u0394Tₘᵢₙ/2. "
        ),
        # html.Div(id="pinch_results", style={"margin-top": "20px"}),
        html.Br(),
        # html.Div(id="pinch_results", style={"margin-top": "20px"}),
        ButtonCustom(label="Run PyPinch Analysis", id="runpinch_tecd").layout,
        dcc.Loading(
            id="loading", children=[html.Div(id="outputdata_tecd")], type="default"
        ),
    ]
)


@app.callback(Output("outputdata_tecd", "children"), [Input("runpinch_tecd", "n_clicks")])
def run_pinch_analysis(n_clicks):
    csv_file_path = os.path.join(os.getcwd(), "pinch_analysis_data.csv")

    if n_clicks and os.path.exists(csv_file_path):
        try:
            # Run the PyPinch analysis
            options = {"draw"}
            pinch = PyPinch(csv_file_path, options)
            pinch.showCompositeDiagram()
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
