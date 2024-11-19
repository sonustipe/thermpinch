from PyPinch import PyPinch
import pandas as pd

def DrawPinch():
    # Draws Matplotlib-based plots
    return {"draw"}


def CSVPinch():
    # Writes calculated data as CSV files
    return {"csv"}


def DebugPinch():
    # Outputs raw calculated data in the terminal
    return {"debug"}
def dataframePinch():
    # Outputs raw calculated data in the terminal
    return {"dataframe"}

def FullPinch():
    # Multiple options can be supplied at once
    return {"draw", "csv", "debug"}


pinch = PyPinch("pinch_analysis_data.csv")
options = dataframePinch()
pinch.showdataframe()
