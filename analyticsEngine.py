"""
"""


# PACKAGE IMPORTS
import pandas as pd                 # Pandas, used to represent CSVs and large data sets as a DataFrame.
import numpy as np                  # NumPy, adds Arrays to python and enables large arithmatic operations.
import matplotlib.pyplot as plt     # MatPlotLib's PyPlot, used to graph data sets and create data visualizations.
import argparse, os, shutil         # Argparse, OS, and Shutil, used for File Manipulation and the Command Line Interface

# LOCAL FILE IMPORTS
import keys                         # API Key File, used to store the API Keys for the project.
import text                         # Text, used to store the Text for the report in a Dictionary (JSON) format.




# GRAPHS
def save_graph(file_name: str, directory: str, dpi: int) -> None:
    """
    Saves the active PyPlot as a file.

    Args:
        `file_name` (str): The name for the file to be saved as.
        `directory` (str): The name of the directory for the file to be saved in.
        `dpi` (int): The DPI (resolution) to save the image in.

    Returns:
        None.

    Preconditions:
        - A PyPlot must be active.
        - The directory must be a local path.

    Raises:
        `OSError`: If the file cannot be moved to the specified directory.

    Example:
        >>> save_graph('plot.png', 'output/', dpi=300)

    Additional Information:
        - The file's extension is specified within the `file_name` argument.
        - The file's location is specified by the `directory` argument.
        - The file's size is specified by the `dpi` argument.
        - If the file cannot be moved to the specified directory, an `OSError` is raised.
    """
    plt.savefig(file_name, dpi=dpi)
    try:
        shutil.move(file_name, directory)
    except OSError:
        os.remove(directory + '/' + file_name)
        shutil.move(file_name, directory)
    plt.close()


def create_map(df: pd.DataFrame, directory: str) -> None:
    """
    """
    pass


def graph_profile_grade(df: pd.DataFrame, directory: str) -> None:
    """
    """
    pass


def graph_missing_organization_contact_info(df: pd.DataFrame, directory: str) -> None:
    """
    """
    pass


def graph_missing_location_contact_info(df: pd.DataFrame, directory: str) -> None:
    """
    """
    pass


def graph_missing_program_contact_info(df: pd.DataFrame, directory: str) -> None:
    """
    """
    pass


def graph_program_type(df: pd.DataFrame, directory: str) -> None:
    """
    """
    pass


def graph_food_program_breakdown(df: pd.DataFrame, directory: str) -> None:
    """
    """
    pass


def graph_program_filter_usage(df: pd.DataFrame, directory: str) -> None:
    """
    """
    pass


def graph_network_hours_overview(df: pd.DataFrame, directory: str) -> None:
    """
    """
    pass


def graph_sample_location_hours(df: pd.DataFrame, directory: str) -> None:
    """
    """
    pass


def graph_sample_program_hours(df: pd.DataFrame, directory: str) -> None:
    """
    """
    pass


def graph_program_qualifications(df: pd.DataFrame, directory: str) -> None:
    """
    """
    pass


def graph_program_service_areas(df: pd.DataFrame, directory: str) -> None:
    """
    """
    pass




# TABLES
def create_network_overview_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    """
    return


def create_highest_graded_profiles_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    """
    return


def create_lowest_graded_profiles_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    """
    return


def create_recommended_program_filters_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    """
    return


def create_hour_type_usage_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    """
    return


def create_organization_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    """
    return


def create_location_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    """
    return


def create_program_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    """
    return


def create_program_profile_completion_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    """
    return


def create_organization_contact_information_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    """
    return


def create_location_contact_information_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    """
    return


def create_program_contact_information_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    """
    return


def create_program_by_program_type_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    """
    return


def create_program_by_program_audience_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    """
    return


def create_program_by_program_languages_spoken_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    """
    return


def create_program_by_program_features_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    """
    return


def create_program_by_program_items_offered_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    """
    return


def create_program_by_program_dietary_options_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    """
    return


def create_location_hours_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    """
    return


def create_program_hours_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    """
    return


def create_program_by_program_qualifications_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    """
    return


def create_program_by_program_services_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    """
    return




# SUMMATIONS
def count_organizations(df: pd.DataFrame) -> int:
    """
    Counts the number of unique organizations in a DataFrame.

    Args:
        `df (pd.DataFrame)`: The Pandas DataFrame containing the data.

    Returns:
        `int`: The number of unique organizations.

    Preconditions:
        - The Pandas DataFrame must contain the column `Organization External ID`.

    Raises:
        - `KeyError`: If the `Organization External ID` column is not present in the DataFrame.

    Example:
        >>> data = pd.DataFrame({'Organization External ID': ['O1', 'O2', 'O2', 'O3', 'O1']})
        >>> count_organizations(data)
        3

    Additional Information:
        - A unique organization is determined by the `Organization External ID` column.
        - This function assumes that the provided DataFrame is properly formatted and contains the necessary columns.
        - Ensure that the DataFrame represents the relevant data and has no missing values in the required column.
    """
    return df['Organization External ID'].nunique()


def count_valid_organizations(df: pd.DataFrame) -> int:
    """
    Counts the number of unique organizations that are both active and approved.

    Args:
        `df (pd.DataFrame)`: The Pandas DataFrame containing the data.

    Returns:
        `int`: The number of unique organizations that are active and approved.

    Preconditions:
        - The Pandas DataFrame must contain the columns:
            - `Organization External ID`
            - `Organization Active Status`
            - `Organization Approved Status`

    Raises:
        - `KeyError`: If any of the required columns are not present in the DataFrame.

    Example:
        >>> data = pd.DataFrame({'Organization External ID': ['O1', 'O2', 'O2', 'O3', 'O1'],
                                'Organization Active Status': [True, False, True, True, True],
                                'Organization Approved Status': [True, True, False, True, True]})
        >>> count_valid_organizations(data)
        2

    Additional Information:
        - An active and approved organization is determined by the `Organization Active Status` and
          `Organization Approved Status` columns.
        - A unique organization is determined by the `Organization External ID` column.
        - This function assumes that the provided DataFrame is properly formatted and contains the necessary columns.
        - Ensure that the DataFrame represents the relevant data and has no missing values in the required columns.
    """
    df = df[(df['Organization Active Status'] == True) & (df['Organization Approved Status'] == True)]
    return df['Organization External ID'].nunique()


def count_locations(df: pd.DataFrame) -> int:
    """
    Counts the number of unique locations in a DataFrame.

    Args:
        `df (pd.DataFrame)`: The Pandas DataFrame containing the data.

    Returns:
        `int`: The number of unique locations.

    Preconditions:
        - The Pandas DataFrame must contain the column 'Location External ID'.

    Raises:
        - `KeyError`: If the column 'Location External ID' is not present in the DataFrame.

    Example:
        >>> data = pd.DataFrame({'Location External ID': ['L1', 'L2', 'L2', 'L3', 'L1']})
        >>> count_locations(data)
        3

    Additional Information:
        - A unique location is determined by the 'Location External ID' column.
        - This function assumes that the provided DataFrame is properly formatted and contains the necessary columns.
        - Ensure that the DataFrame represents the relevant data and has no missing values in the 'Location External ID' column.
    """
    return df['Location External ID'].nunique()


def count_valid_locations(df: pd.DataFrame) -> int:
    """
    Counts the number of unique locations that are both active and approved.

    Args:
        `df (pd.DataFrame)`: The Pandas DataFrame containing the data.

    Returns:
        `int`: The number of unique locations that are active and approved.

    Preconditions:
        - The Pandas DataFrame must contain the columns:
            - `Location External ID`
            - `Location Active Status`
            - `Location Approved Status`

    Raises:
        - `KeyError`: If any of the required columns (`Location External ID`, `Location Active Status`, `Location Approved Status`)
          are not present in the DataFrame.

    Example:
        >>> data = pd.DataFrame({
        ...     'Location External ID': ['L1', 'L2', 'L2', 'L3', 'L1'],
        ...     'Location Active Status': [True, False, True, True, True],
        ...     'Location Approved Status': [True, True, False, True, True]
        ... })
        >>> count_valid_locations(data)
        2

    Additional Information:
        - An active and approved location is determined by the 'Location Active Status' and 'Location Approved Status' columns.
        - A unique location is determined by the 'Location External ID' column.
        - This function assumes that the provided DataFrame is properly formatted and contains the necessary columns.
        - Ensure that the 'Location Active Status' and 'Location Approved Status' columns use boolean values (True/False).
        - For accurate results, make sure the DataFrame represents the relevant data and has no missing values.
    """
    df = df[(df['Location Active Status'] == True) & (df['Location Approved Status'] == True)]
    return df['Location External ID'].nunique()


def count_programs(df: pd.DataFrame) -> int:
    """
    Counts the number of unique programs in a DataFrame.

    Args:
        `df (pd.DataFrame)`: The Pandas DataFrame containing the data.

    Returns:
        `int`: The number of unique programs.

    Preconditions:
        - The Pandas DataFrame must contain the column `Program External ID`.

    Raises:
        - `KeyError`: If the `Program External ID` column is not present in the DataFrame.

    Examples:
        >>> data = pd.DataFrame({'Program External ID': ['P1', 'P2', 'P2', 'P3', 'P1']})
        >>> count_programs(data)
        3

    Additional Information:
        - A unique program is determined by the `Program External ID` column.
        - This function assumes that the provided DataFrame is properly formatted and contains the necessary column.
    """
    return df['Program External ID'].nunique()


def count_valid_programs(df: pd.DataFrame) -> int:
    """
    Counts the number of unique programs that are both active and approved.

    Args:
        `df (pd.DataFrame)`: The Pandas DataFrame containing the data.

    Returns:
        `int`: The number of unique programs that are active and approved.

    Preconditions:
        - The Pandas DataFrame must contain the columns:
            - `Program External ID`
            - `Program Active Status`
            - `Program Approved Status`

    Raises:
        - `KeyError`: If any of the required columns (`Program External ID`, `Program Active Status`, `Program Approved Status`)
          are not present in the DataFrame.

    Example:
        >>> data = pd.DataFrame({
        ...     'Program External ID': ['P1', 'P2', 'P2', 'P3', 'P1'],
        ...     'Program Active Status': [True, False, True, True, True],
        ...     'Program Approved Status': [True, True, False, True, True]
        ... })
        >>> count_valid_programs(data)
        2

    Additional Information:
        - An active and approved program is determined by the `Program Active Status` and `Program Approved Status` columns.
        - A unique program is determined by the `Program External ID` column.
        - This function assumes that the provided DataFrame is properly formatted and contains the necessary columns.
        - Ensure that the `Program Active Status` and `Program Approved Status` columns use boolean values (True/False).
        - For accurate results, make sure the DataFrame represents the relevant data and has no missing values.
    """
    df = df[(df['Program Active Status'] == True) & (df['Program Approved Status'] == True)]
    return df['Program External ID'].nunique()




# MAIN
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
    # Create a list of graphing functions
    graphing_functions = [
        create_map,
        graph_profile_grade,
        graph_missing_organization_contact_info,
        graph_missing_location_contact_info,
        graph_missing_program_contact_info,
        graph_program_type,
        graph_food_program_breakdown,
        graph_program_filter_usage,
        graph_network_hours_overview,
        graph_sample_location_hours,
        graph_sample_program_hours,
        graph_program_qualifications
    ]
    # Create a list of DataFrame functions
    dataframe_functions = [
        create_network_overview_table,
        create_highest_graded_profiles_table,
        create_lowest_graded_profiles_table,
        create_recommended_program_filters_table,
        create_organization_table,
        create_location_table,
        create_program_table,
        create_organization_contact_information_table,
        create_location_contact_information_table,
        create_program_contact_information_table,
        create_program_by_program_type_table,
        create_program_by_program_audience_table,
        create_program_by_program_languages_spoken_table,
        create_program_by_program_features_table,
        create_program_by_program_items_offered_table,
        create_program_by_program_dietary_options_table,
        create_location_hours_table,
        create_program_hours_table,
        create_program_by_program_qualifications_table,
        create_program_by_program_services_table
    ]
    # Create a list of summation functions
    summation_functions = [
        count_organizations,
        count_valid_organizations,
        count_locations,
        count_valid_locations,
        count_programs,
        count_valid_programs
    ]

    # Create directory within project folder
    if not os.path.isdir(directory):
        os.mkdir(directory)
    # Move file to directory
    if args.file.split("\\")[0] != directory:
        shutil.move(args.file, directory)

    # Create list of silenced functions
    silenced_functions = args.silent if args.silent else []

    # Create valid graphing functions
    valid_graphing_functions = [graph for graph in graphing_functions if graph.__name__ not in silenced_functions]
    # Create valid DataFrame functions
    valid_dataframe_functions = [dataframe for dataframe in dataframe_functions if dataframe.__name__ not in silenced_functions]
    # Create valid summation functions
    valid_summation_functions = [summation for summation in summation_functions if summation.__name__ not in silenced_functions]

    # Execute functions
    [graph(df, directory) for graph in valid_graphing_functions]
    [print(dataframe.__name__ + ": " + dataframe(df)) for dataframe in valid_dataframe_functions]
    [print(summation.__name__ + ": " + str(summation(df))) for summation in valid_summation_functions]
