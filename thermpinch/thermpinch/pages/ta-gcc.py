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


PAGE_TITLE = "Grand Composite Curve"


class PageIDs:
    def __init__(self) -> None:
        # Get the base name of the file where this instance is created
        filename = os.path.basename(__file__)
        # Remove the file extension to use only the file name as the prefix
        prefix: Final[str] = filename.replace(".py", "")
        self.prefix: Final[str] = prefix
        self.status: Final[str] = f"{prefix}_status"
        self.outputdata_gcc: Final[str] = f"{prefix}_outputdata_gcc"
        self.runpinch_gcc: Final[str] = f"{prefix}_runpinch_gcc"
        self.runpinch: Final[str] = f"{prefix}_runpinch"

ids = PageIDs()

layout = html.Div(
    [
        html.H1("pinch", className="app-title"),
        html.H2(PAGE_TITLE, className="page-title"),
        html.Hr(),
        # html.Div(id="pinch_results", style={"margin-top": "20px"}),
        html.Div(
            "Based on the Net Enthalpy Change in each interval (depicted in the Problem Table), the Grand Composite Curve can be constructed. Therefore, it can be seen as the graphical representation of the Problem Table. As before, the minimum cold utility Q꜀ₘᵢₙ(kW) is shaded in blue, while the minimum hot utility Qₕₘᵢₙ (kW) is shaded in red. The Pinch Point corresponds to the point of zero net enthalpy change between two adjacent intervals. It is shown with a dotted line at the Pinch Temperature ."
        ),
        html.Br(),
        # html.Div(id="pinch_results", style={"margin-top": "20px"}),
        ButtonCustom(label="Run PyPinch Analysis", id="runpinch_gcc").layout,
        dcc.Loading(
            id="loading",
            children=[html.Div(id="outputdata_gcc")],
            type="default",
        ),
    ]
)


@app.callback(Output("outputdata_gcc", "children"), [Input("runpinch_gcc", "n_clicks")])
def run_pinch_analysis(n_clicks):
    csv_file_path = os.path.join(os.getcwd(), "pinch_analysis_data.csv")

    if n_clicks and os.path.exists(csv_file_path):
        try:
            # Run the PyPinch analysis
            options = {"draw"}
            pinch = PyPinch(csv_file_path, options)
            pinch.showGrandCompositeCurve()
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
