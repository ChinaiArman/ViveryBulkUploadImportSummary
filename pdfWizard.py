"""
"""


# PACKAGE IMPORTS
from fpdf import FPDF
import pandas as pd                 # Pandas, used to represent CSVs and large data sets as a DataFrame.
import numpy as np                  # NumPy, adds Arrays to python and enables large arithmatic operations.
import matplotlib.pyplot as plt     # MatPlotLib's PyPlot, used to graph data sets and create data visualizations.
import argparse, os, shutil         # Argparse, OS, and Shutil, used for File Manipulation and the Command Line Interface
import json                         # JSON, used to parse JSON files and convert to Dictionary data types.

# LOCAL FILE IMPORTS
import analyticsEngine as ae        # AnalyticsWizard, used as an API to parse and process the Bulk Upload Data File into small chunks of information.

# CONSTANTS
TEXT_SAVE_NAME = "resources/text.json"                                                  # Path to TEXT save file (JSON).
with open(TEXT_SAVE_NAME) as file: TEXT = json.load(file)                               # TEXT, used for all of the text in the PDF report; stored in the file, 'resources/text.json'.




# PDFCONSTRUCTOR CLASS
class pdfConstructor:
    """
    """
    def __init__(
            self, 
            new_df: pd.DataFrame(), 
            new_directory: str,
            new_filename: str,
            new_network_name: str
            ) -> None:
        """
        """
        self.df = new_df
        self.directory = new_directory
        self.filename = new_filename
        self.network_name = new_network_name
        self.pdf = FPDF()
        return




# MAIN
if __name__ == "__main__":
    # Define console parser
    parser = argparse.ArgumentParser(description="Create data visualizations for a Pre-Validated file")
    # Add file argument
    parser.add_argument("file", action="store", help="The file to validate.")
    # Add network name argument
    parser.add_argument("network_name", action="store", help="To name the PDF and customize to the specific Network")
    # Console arguments
    args = parser.parse_args()
    
    # Create directory name
    directory = "data_" + args.file.split("\\")[-1].replace(".csv", "")
    # Create network name
    network_name = args.network_name
    # Create DataFrame
    df = pd.read_csv(args.file)

    # Create directory within project folder
    if not os.path.isdir(directory):
        os.mkdir(directory)
    if not os.path.isdir(directory + "/resources"):
        os.mkdir(directory + "/resources")
    if not os.path.isdir(directory + "/csvs"):
        os.mkdir(directory + "/csvs")
    if not os.path.isdir(directory + "/images"):
        os.mkdir(directory + "/images")
    # Move file to directory
    if args.file.split("\\")[0] != directory:
        shutil.move(args.file, directory)

    # Create pdfConstructor instance
    constructor = pdfConstructor(df, directory, network_name.replace(" ", "_").lower() + "_analytical_report.pdf", network_name)

    # Create PDF
    constructor.show_data()
