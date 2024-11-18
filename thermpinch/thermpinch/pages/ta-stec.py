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


PAGE_TITLE = "Shifted Temperature-Enthalpy Composite Diagram"


class PageIDs:
    def __init__(self) -> None:
        # Get the base name of the file where this instance is created
        filename = os.path.basename(__file__)
        # Remove the file extension to use only the file name as the prefix
        prefix: Final[str] = filename.replace(".py", "")
        self.prefix: Final[str] = prefix
        self.status: Final[str] = f"{prefix}_status"
        self.outputdata_stec: Final[str] = f"{prefix}_outputdata_stec"
        self.runpinch_stec: Final[str] = f"{prefix}_runpinch_stec"
        self.runpinch: Final[str] = f"{prefix}_runpinch"


        ids = PageIDs()


layout = html.Div(
    [
        html.H1("pinch", className="app-title"),
        html.H2(PAGE_TITLE, className="page-title"),
        html.Hr(),
        # html.Div(id="pinch_results", style={"margin-top": "20px"}),
        html.Div(
            "The minimum cold utility Q꜀ₘᵢₙ (kW) is shaded in blue, while the minimum hot utility Qₕₘᵢₙ (kW) is shaded in red. These areas correspond to the regions in which no heat exchange can take place: where the graphs do not superimpose. The Pinch point is the point of closest approach between the two composite curves. It is shown with a dotted line. The Pinch point Temperature corresponds to the one found in the Heat Cascade."
        ),
        html.Br(),
        # html.Div(id="pinch_results", style={"margin-top": "20px"}),
        ButtonCustom(label="Run PyPinch Analysis", id="runpinch_stec").layout,
        dcc.Loading(
            id="loading", children=[html.Div(id="outputdata_stec")], type="default"
        ),
    ]
)


@app.callback(
    Output("outputdata_stec", "children"), [Input("runpinch_stec", "n_clicks")]
)
def run_pinch_analysis(n_clicks):
    csv_file_path = os.path.join(os.getcwd(), "pinch_analysis_data.csv")

    if n_clicks and os.path.exists(csv_file_path):
        try:
            # Run the PyPinch analysis
            options = {"draw"}
            pinch = PyPinch(csv_file_path, options)
            pinch.showShiftedCompositeDiagram()
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
