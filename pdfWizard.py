# Import packages
from fpdf import FPDF
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import argparse

# Import local files
import analyticsWizard as aw

# Constants
FILENAME = "" # UPDATE


class pdfConstructor:
    def __init__(self, 
                 new_df: pd.DataFrame(), 
                 new_root: str
                ):
        self.df = new_df
        self.root = new_root
        self.path = new_root + FILENAME # UPDATE
        
    def print(self):
        print(self.df)


if __name__ == "__main__":
    # Define console parser
    parser = argparse.ArgumentParser(description="Create data visualizations for a Pre-Validated file")
    # Add file argument
    parser.add_argument("file", action="store", help="The file to validate.")
    # Console arguments
    args = parser.parse_args()
    
    # Create dataframe
    df = pd.read_csv(args.file, encoding='unicode_escape')
    
    # Create pdfConstructor instance
    constructor = pdfConstructor(df, args.file)

    # Create PDF
