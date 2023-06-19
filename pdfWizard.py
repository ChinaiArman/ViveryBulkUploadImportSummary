"""
"""


# PACKAGE IMPORTS
from fpdf import FPDF
import pandas as pd                 # Pandas, used to represent CSVs and large data sets as a DataFrame.
import numpy as np                  # NumPy, adds Arrays to python and enables large arithmatic operations.
import matplotlib.pyplot as plt     # MatPlotLib's PyPlot, used to graph data sets and create data visualizations.
import argparse, os, shutil         # Argparse, OS, and Shutil, used for File Manipulation and the Command Line Interface

# LOCAL FILE IMPORTS
import analyticsEngine as ae        # AnalyticsWizard, used as an API to parse and process the Bulk Upload Data File into small chunks of information.
import text as txt                  # Text, used to store the Text for the report in a Dictionary (JSON) format.

# CONSTANTS




# PDFCONSTRUCTOR CLASS
class pdfConstructor:
    """
    """
    def __init__(self, 
                 new_df: pd.DataFrame(), 
                 new_directory: str,
                 new_filepath: str,
                 new_filename: str
                ):
        """
        """
        self.df = new_df
        self.directory = new_directory
        self.filepath = new_filepath
        self.filename = new_filename




# MAIN
if __name__ == "__main__":
    # Define console parser
    parser = argparse.ArgumentParser(description="Create data visualizations for a Pre-Validated file")
    # Add file argument
    parser.add_argument("file", action="store", help="The file to validate.")
    # Console arguments
    args = parser.parse_args()
    
    # Create filename
    filename = args.file.split("\\")[-1]
    # Create directory name
    directory = "data_" + filename.replace(".csv", "")
    # Create path to file
    path = directory + "\\" + filename
    # Create DataFrame
    df = pd.read_csv(args.file)

    # Create directory within project folder
    if not os.path.isdir(directory):
        os.mkdir(directory)
    # Move file to directory
    if args.file.split("\\")[0] != directory:
        shutil.move(args.file, directory)

    # Create pdfConstructor instance
    constructor = pdfConstructor(df, directory, path, filename)

    # Create PDF
