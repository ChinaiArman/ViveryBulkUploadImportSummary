# Import packages
from fpdf import FPDF
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import argparse
import shutil

# Import local files
import analyticsWizard as aw

# Constants


class pdfConstructor:
    def __init__(self, 
                 new_df: pd.DataFrame(), 
                 new_directory: str,
                 new_filepath: str,
                 new_filename: str
                ):
        self.df = new_df
        self.directory = new_directory
        self.filepath = new_filepath
        self.filename = new_filename


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
    df = pd.read_csv(path)

    # Create directory within project folder
    if not os.path.isdir(directory):
        os.mkdir(directory)
    # Move file to directory
    if args.file.split("\\")[0] != directory:
        shutil.move(args.file, directory)

    # Create pdfConstructor instance
    constructor = pdfConstructor(df, directory, path, filename)

    # Create PDF
