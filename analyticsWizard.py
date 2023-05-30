# Import packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import argparse
import os
import shutil


def count_number_of_orgs(df: pd.DataFrame) -> int:
    """
    Counts the number of unique organizations in a DataFrame.
    Unique organizations are determined by the 'Organization External ID' column.

    :param df: A Pandas DataFrame
    :return: The number of unique organizations, represented as an integer.
    """
    return df['Organization External ID'].nunique()


def count_number_of_orgs_approved(df: pd.DataFrame) -> int:
    """
    Counts the number of unique organizations that are both active and approved.
    Active and Approved organizations are determined by the 'Organization Active Status' and 'Organization Approved Status' columns.
    Unique organizations are determined by the 'Organization External ID' column.

    :param df: A Pandas DataFrame
    :return: The number of unique organizations that are both approved and active, represented as an integer. 
    """
    df = df[(df['Organization Active Status'] == True) & (df['Organization Approval Status'] == True)]
    return df['Organization External ID'].nunique()


def count_number_of_locs(df: pd.DataFrame) -> int:
    """
    Counts the number of unique locations in a DataFrame. Unique locations are determined by the 'Location External ID'.

    :param df: A Pandas DataFrame
    :return: The number of unique locations, represented as an integer.
    """
    return df['Location External ID'].nunique()


def count_number_of_locs_approved(df: pd.DataFrame) -> int:
    """
    Counts the number of unique locations that are both active and approved.
    Active and Approved locations are determined by the 'Location Active Status' and 'Location Approved Status' columns.
    Unique locations are determined by the 'Location External ID' column.

    :param df: A Pandas DataFrame
    :return: The number of unique locations that are both approved and active, represented as an integer. 
    """
    df = df[(df['Location Active Status'] == True) & (df['Location Approval Status'] == True)]
    return df['Location External ID'].nunique()


def count_number_of_progs(df: pd.DataFrame) -> int:
    """
    Counts the number of unique programs in a DataFrame. Unique programs are determined by the 'Program External ID'.

    :param df: A Pandas DataFrame
    :return: The number of unique programs, represented as an integer.
    """
    return df['Program External ID'].nunique()


def count_number_of_progs_approved(df: pd.DataFrame) -> int:
    """
    Counts the number of unique programs that are both active and approved.
    Active and Approved programs are determined by the 'Program Active Status' and 'Program Approved Status' columns.
    Unique programs are determined by the 'Program External ID' column.

    :param df: A Pandas DataFrame
    :return: The number of unique programs that are both approved and active, represented as an integer. 
    """
    df = df[(df['Program Active Status'] == True) & (df['Program Approval Status'] == True)]
    return df['Program External ID'].nunique()


if __name__ == "__main__":
    # Define console parser
    parser = argparse.ArgumentParser(description="Create data visualizations for a Pre-Validated file")
    # Add file argument
    parser.add_argument("file", action="store", help="The file to validate.")
    # Add silent argument
    parser.add_argument('--silent', action='store', nargs='+', help='Name of visualizations to not generate')
    # Console arguments
    args = parser.parse_args()
    
    # Create directory name
    directory = "data_" + args.file.split("\\")[-1].replace(".csv", "")
    # Create DataFrame
    df = pd.read_csv(args.file)
    # Create a list of visualization functions
    graphing_functions = [

    ]
    # Create a list of text functions
    calculating_functions = [
        count_number_of_orgs,
        count_number_of_orgs_approved,
        count_number_of_locs,
        count_number_of_locs_approved,
        count_number_of_progs,
        count_number_of_progs_approved
    ]

    # Create directory within project folder
    if not os.path.isdir(directory):
        os.mkdir(directory)
    # Move file to directory
    if args.file.split("\\")[0] != directory:
        shutil.move(args.file, directory)

    # Create list of silenced functions
    silenced_functions = args.silent if args.silent else []

    # Create valid visualizations functions
    valid_graphing_functions = [graph for graph in graphing_functions if graph.__name__ not in silenced_functions]
    # Create valid text functions
    valid_calculation_functions = [calculation for calculation in calculating_functions if calculation.__name__ not in silenced_functions]
    
    # Execute functions
    [graph(df, directory) for graph in valid_graphing_functions]
    [print(calculation(df)) for calculation in valid_calculation_functions]
