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
    # Create list of visualizations
    visualizations = [
        
    ]
    # Create list of silenced visualizations
    silenced_visualizations = args.silent if args.silent else []
    # Create valid visualizations
    valid_visualizations = [visualization for visualization in visualizations if visualization.__name__ not in silenced_visualizations]
    # Create output
    output = []

    # Execute visualizations
    output = [visualization(df) for visualization in valid_visualizations]

    # Create output
    if len(set(output)) != 1:
        print(output)
