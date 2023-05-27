# Import packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import argparse


if __name__ == "__main__":
    # Define console parser
    parser = argparse.ArgumentParser(description="Create data visualizations for a Pre-Validated file")
    # Add file argument
    parser.add_argument("file", action="store", help="The file to validate.")
    # Add silent argument
    parser.add_argument('--silent', action='store', nargs='+', help='Name of visualizations to not generate')
    # Console arguments
    args = parser.parse_args()
    
    # Create dataframe
    df = pd.read_csv(args.file, encoding='unicode_escape')
    # Create a list of visualization functions
    graphing_functions = [

    ]
    # Create a list of text functions
    calculating_functions = [

    ]
    # Create list of silenced functions
    silenced_functions = args.silent if args.silent else []

    # Create valid visualizations functions
    valid_graphing_functions = [graph for graph in graphing_functions if graph.__name__ not in silenced_functions]
    # Create valid text functions
    valid_calculation_functions = [calculation for calculation in calculating_functions if calculation.__name__ not in silenced_functions]
    
    # Execute functions
    [graph(df) for graph in valid_graphing_functions]
    [print(calculation(df)) for calculation in valid_calculation_functions]
