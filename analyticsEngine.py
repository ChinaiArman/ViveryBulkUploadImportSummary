"""
"""


# PACKAGE IMPORTS
import pandas as pd                 # Pandas, used to represent CSVs and large data sets as a DataFrame.
import numpy as np                  # NumPy, adds Arrays to python and enables large arithmatic operations.
import matplotlib.pyplot as plt     # MatPlotLib's PyPlot, used to graph data sets and create data visualizations.
import argparse, os, shutil         # Argparse, OS, and Shutil, used for File Manipulation and the Command Line Interface
import plotly.graph_objects as go   #
import json                         # JSON, used to parse JSON files and convert to Dictionary data types.
from PIL import Image               #

# LOCAL FILE IMPORTS


# CONSTANTS
from keys import PK, SK                                                                 # PK and SK, used for the MapBoxAPI; stored in the API Key File 'keys'.
TEXT_SAVE_NAME = "resources/text.json"                                                  # Path to TEXT save file (JSON).
with open(TEXT_SAVE_NAME) as file: TEXT = json.load(file)                               # TEXT, used for all of the text in the PDF report; stored in the file, 'resources/text.json'.
WEIGHTS_SAVE_NAME = "resources/weights.json"                                            # Path to WEIGHTS save file (JSON).
with open(WEIGHTS_SAVE_NAME) as file: WEIGHTS = json.load(file)                         # WEIGHTS, used for the weightage of each column in the profile completion grades; stored in the file, 'resources/weights.json'.
RECOMMENDED_FILTERS_SAVE_NAME = 'resources/recommended_filters.csv'                     # Path to Recommended Filters (CSV).
RECOMMENDED_FILTERS = pd.read_csv(RECOMMENDED_FILTERS_SAVE_NAME)                        # RECOMMENDED_FILTERS, used to store the recommended filters for locations and programs, stored in the file, 'resources/recommended_filters.csv'
PROFILE_COMPLETION_TIERS_SAVE_NAME = 'resources/profile_completion_tiers.csv'           # Path to Profile Completion Tiers (CSV).
PROFILE_COMPLETION_TIERS = pd.read_csv(PROFILE_COMPLETION_TIERS_SAVE_NAME)              # PROFILE_COMPLETION_TIERS, used to store the profile completion tiers for locations, stored in the file, 'resources/profile_completion_tiers.csv'

# COLOURS
VIVERY_GREEN = '#00483D'                                                                #
DARK_SAGE = '#00796B'                                                                   #
RED = '#D4A392'                                                                         #




# HELPERS
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
    return


def save_state(data: any, filename: str, directory: str) -> None:
    """
    Saves the current state of the data in a specified folder.

    Args:
        `data` (any): The data to be saved. It can be either a dictionary or a Pandas DataFrame.
        `filename` (str): The name for the file to be saved as.
        `directory` (str): The name of the directory for the file to be saved in.

    Returns:
        None.

    Preconditions:
        - The `data` parameter must be either a dictionary or a Pandas DataFrame.
        - The `filename` parameter should specify the desired name for the saved file.
        - The `directory` parameter should specify the target directory for saving the file.

    Raises:
        None.

    Example:
        >>> data_dict = {'name': 'John', 'age': 30}
        >>> save_state(data_dict, 'data.json', 'output/')
        >>> data_frame = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})
        >>> save_state(data_frame, 'data.csv', 'output/')

    Additional Information:
        - The function first checks the type of the `data` parameter to determine whether it is a dictionary or a Pandas DataFrame.
        - If `data` is a dictionary, it is saved as a JSON file with the specified `filename`.
        - If `data` is a Pandas DataFrame, it is saved as a CSV file with the specified `filename`.
        - The saved file is then moved to the specified `directory`.
        - If the file cannot be moved to the specified directory, an attempt is made to remove the existing file in the directory with the same name, and then move the new file to the directory.
        - Ensure that the `filename` includes the appropriate file extension based on the data type.
        - Ensure that the `directory` is a valid path for saving the file.
    """
    if type(data) == dict:
        file = open(filename,'w+')
        json.dump(data, file)
        file.close()
    elif type(data) == pd.DataFrame:
        data.to_csv(filename)
    try:
        shutil.move(filename, directory)
    except OSError:
        os.remove(directory + '/' + filename)
        shutil.move(filename, directory)
    return


def map_scope(int: int) -> None:
    """
    """
    if int > 60:
        return 2
    if int > 50:
        return 3
    if int > 30:
        return 4
    if int > 5:
        return 5
    if int > 2:
        return 6
    if int > 1:
        return 8
    return 12


def crop_image(width: int, height: int, filename: str, directory: str) -> None:
    """
    """
    im = Image.open(directory + "/" + filename)
    im = im.crop((height/2, width/2, height/2 + width, width/2 + height))
    im.save(directory + "/" + filename, "png")
    return




# GRAPHS
def create_map(df: pd.DataFrame, directory: str) -> None:
    """
    """
    df2 = df.copy()
    df2 = df2[['Location Latitude', 'Location Longitude', 'Organization Approval Status', 'Organization Active Status', 'Location Active Status', 'Location Approval Status']]
    df2['Color'] = np.where((df['Organization Approval Status'] == True) & (df['Organization Active Status'] == True) & (df['Location Approval Status'] == True) & (df['Location Active Status'] == True), DARK_SAGE, RED)

    fig = go.Figure(go.Scattermapbox(
            lat=df2['Location Latitude'],
            lon=df2['Location Longitude'],
            mode='markers',
            marker={'color': df2['Color'],
                    'size': 8}
        ))
    fig.update_layout(
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            accesstoken=PK,
            bearing=0,
            center=dict(
                lat=df2['Location Latitude'].mean(),
                lon=df2['Location Longitude'].mean(),
            ),
            pitch=0,
            zoom=max(map_scope((df2['Location Longitude'].max() - df2['Location Longitude'].min())), map_scope((df2['Location Latitude'].max() - df2['Location Latitude'].min())))
        ),
    )
    fig.write_image(directory + '/map.png', width=1000, height=1000)
    crop_image(624, 403, "map.png", directory)
    return


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
    Creates a network overview table based on the provided DataFrame.

    Args:
        `df` (pd.DataFrame): The Pandas DataFrame containing the network data.

    Returns:
        `pd.DataFrame`: A DataFrame containing the network overview information.

    Preconditions:
        - The Pandas DataFrame must contain the following columns:
            - `Organization External ID`
            - `Organization Approval Status`
            - `Organization Active Status`
            - `Location External ID`
            - `Location Approval Status`
            - `Location Active Status`
            - `Program External ID`
            - `Program Approval Status`
            - `Program Active Status`

    Raises:
        None.

    Example:
        >>> data = pd.DataFrame({
        ...     'Organization External ID': ['O1', 'O2', 'O2', 'O3', 'O1'],
        ...     'Organization Approval Status': [True, False, True, True, True],
        ...     'Organization Active Status': [True, True, False, True, True],
        ...     'Location External ID': ['L1', 'L2', 'L3', 'L1', 'L2'],
        ...     'Location Approval Status': [True, True, True, False, True],
        ...     'Location Active Status': [True, True, True, True, False],
        ...     'Program External ID': ['P1', 'P2', 'P2', 'P3', 'P1'],
        ...     'Program Approval Status': [True, True, True, True, True],
        ...     'Program Active Status': [True, True, True, False, True]
        ... })
        >>> create_network_overview_table(data)
            Level               Active  Inactive  Total
        0       Organizations       2         1      3
        1       Locations           3         2      3
        2       Programs            2         1      3

    Additional Information:
        - The network overview table provides a summary of the active, inactive, and total counts for organizations,
          locations, and programs within the network.
        - The active status of an organization, location, or program is determined by the `Organization Active Status`,
          `Location Active Status`, or `Program Active Status` columns, respectively.
        - The approval status of an organization, location, or program is determined by the `Organization Approval Status`,
          `Location Approval Status`, or `Program Approval Status` columns, respectively.
        - The count of unique entities is based on their respective external ID columns.
        - The table row headers and column headers are obtained from the `TEXT` dictionary under the key `NETWORK OVERVIEW`.
    """
    active = [
        df[['Organization External ID', 'Organization Approval Status', 'Organization Active Status']].loc[(df['Organization Approval Status'] == True) & (df['Organization Active Status'] == True)]['Organization External ID'].nunique(),
        df[['Location External ID', 'Location Approval Status', 'Location Active Status']].loc[(df['Location Approval Status'] == True) & (df['Location Active Status'] == True)]['Location External ID'].nunique(),
        df[['Program External ID', 'Program Approval Status', 'Program Active Status']].loc[(df['Program Approval Status'] == True) & (df['Program Active Status'] == True)]['Program External ID'].nunique()
        ]
    inactive = [
        df[['Organization External ID', 'Organization Approval Status', 'Organization Active Status']].loc[(df['Organization Approval Status'] != True) | (df['Organization Active Status'] != True)]['Organization External ID'].nunique(),
        df[['Location External ID', 'Location Approval Status', 'Location Active Status']].loc[(df['Location Approval Status'] != True) | (df['Location Active Status'] != True)]['Location External ID'].nunique(),
        df[['Program External ID', 'Program Approval Status', 'Program Active Status']].loc[(df['Program Approval Status'] != True) | (df['Program Active Status'] != True)]['Program External ID'].nunique()
        ]
    total = [
        df[['Organization External ID', 'Organization Approval Status', 'Organization Active Status']]['Organization External ID'].nunique(),
        df[['Organization External ID', 'Organization Approval Status', 'Organization Active Status']]['Organization External ID'].nunique(),
        df[['Program External ID', 'Program Approval Status', 'Program Active Status']]['Program External ID'].nunique()
        ]
    data = {
        'Level': TEXT["NETWORK OVERVIEW"]["rows"],
        'Active': active,
        'Inactive': inactive,
        'Total': total
        }
    return pd.DataFrame(data, columns=TEXT["NETWORK OVERVIEW"]["columns"])


def create_highest_graded_profiles_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a table of the highest graded program profiles based on the provided DataFrame.

    Args:
        `df` (pd.DataFrame): The Pandas DataFrame containing the data.

    Returns:
        `pd.DataFrame`: A DataFrame containing the highest graded program profiles.

    Preconditions:
        - The Pandas DataFrame must contain the necessary columns to calculate program profile completion, as required by the `create_program_profile_completion_table` function.
        - The `weights.py` file must be present in the working directory to access the completion weight for each column.

    Raises:
        None.

    Example:
        >>> data = pd.DataFrame({'Location External ID': ['L1', 'L2', 'L3'],
        ...                     'Location Name': [None, None, 'Good Food'],
        ...                     'Location ZIP': [715359, None, 136135],
        ...                     'Hours Entity Type': ['Program', 'Location', 'Location']})
        >>> create_program_profile_completion_table(data)
            Location ID     Profile Score   Tier Level
        0           L3              8           Basic
        1           L1              5           Basic
        2           L2              5           Basic

    Additional Information:
        - The function calls the `create_program_profile_completion_table` function to create a table of program profile completion based on the provided DataFrame.
        - It then sorts the resulting table in descending order of the profile scores.
        - The table displays the top 5 highest graded program profiles based on the `Profile Score` column.
        - The profile completion grades model after the internal scores Vivery uses to measure profile completeness.
        - Ensure that the provided DataFrame contains the necessary columns and represents the relevant data to calculate program profile completion.
        - For an accurate calculation, ensure all columns are present in the DataFrame.
        - The table column headers are obtained from the `TEXT` dictionary under the key `APPENDIX PROGRAM PROFILE COMPLETION LIST`.
    """ 
    return create_program_profile_completion_table(df).sort_values(by=TEXT["APPENDIX PROGRAM PROFILE COMPLETION LIST"]["columns"][1], ascending=False).head(5).reset_index(drop=True)


def create_lowest_graded_profiles_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a table of the lowest graded program profiles based on the provided DataFrame.

    Args:
        `df` (pd.DataFrame): The Pandas DataFrame containing the data.

    Returns:
        `pd.DataFrame`: A DataFrame containing the lowest graded program profiles.

    Preconditions:
        - The Pandas DataFrame must contain the necessary columns to calculate program profile completion, as required by the `create_program_profile_completion_table` function.
        - The `weights.py` file must be present in the working directory to access the completion weight for each column.

    Raises:
        None.

    Example:
        >>> data = pd.DataFrame({'Location External ID': ['L1', 'L2', 'L3'],
        ...                     'Location Name': [None, None, 'Good Food'],
        ...                     'Location ZIP': [715359, None, 136135],
        ...                     'Hours Entity Type': ['Program', 'Location', 'Location']})
        >>> create_program_profile_completion_table(data)
            Location ID     Profile Score   Tier Level
        0           L1              5           Basic
        1           L2              5           Basic
        2           L3              8           Basic

    Additional Information:
        - The function calls the `create_program_profile_completion_table` function to create a table of program profile completion based on the provided DataFrame.
        - It then sorts the resulting table in ascending order of the profile scores.
        - The table displays the 5 lowest graded program profiles based on the `Profile Score` column.
        - The profile completion grades model after the internal scores Vivery uses to measure profile completeness.
        - Ensure that the provided DataFrame contains the necessary columns and represents the relevant data to calculate program profile completion.
        - For an accurate calculation, ensure all columns are present in the DataFrame.
        - The table column headers are obtained from the `TEXT` dictionary under the key `APPENDIX PROGRAM PROFILE COMPLETION LIST`.
    """
    return create_program_profile_completion_table(df).sort_values(by=TEXT["APPENDIX PROGRAM PROFILE COMPLETION LIST"]["columns"][1], ascending=True).head(5).reset_index(drop=True)


def create_recommended_filters_slice(_: any) -> pd.DataFrame:
    """
    Creates a table of recommended program filters and returns the top 5 results.

    Args:
        `_` (any): Placeholder argument (ignored).

    Returns:
        `pd.DataFrame`: A DataFrame containing the recommended program filters.

    Preconditions:
        - The `recommended_filters.csv` file must exist in the `resources` directory.

    Raises:
        `pandas.errors.EmptyDataError`: If the CSV is empty.

    Example:
        >>> create_recommended_program_filters_table(None)
            #   Program Audience            Location Features            Program Features           Items Offered           Dietary Options
        0   1       Seniors                     Safe Space                  Reservations                Dairy                   Gluten Free
        1   2       Immigrants                  Wi-Fi Available             Indoor Service              Eggs                    Vegan
        2   3       Youth                                                   Prepared Food               Meat                    Vegetarian

    Additional Information:
        - The function reads the `recommended_filters.csv` file from the `resources` directory to create the table.
        - The table includes filter categories and their corresponding filter names.
        - The placeholder argument `_` is ignored and not used in the function.
        - This table only returns a slice of the recommended filters, specifically the top 5 results.
        - Table column headers are pulled from `text.json`.
    """
    df = RECOMMENDED_FILTERS.copy().head(5)
    df.columns = TEXT["RECOMMENDED FILTER OPTIONS"]["columns"]
    return df


def create_recommended_program_filters_table(_: any) -> pd.DataFrame:
    """
    Creates a table of recommended program filters.

    Args:
        `_` (any): Placeholder argument (ignored).

    Returns:
        `pd.DataFrame`: A DataFrame containing the recommended program filters.

    Preconditions:
        - The `recommended_filters.csv` file must exist in the `resources` directory.

    Raises:
        `pandas.errors.EmptyDataError`: If the CSV is empty.

    Example:
        >>> create_recommended_program_filters_table(None)
            #   Program Audience            Location Features            Program Features           Items Offered           Dietary Options
        0   1       Seniors                     Safe Space                  Reservations                Dairy                   Gluten Free
        1   2       Immigrants                  Wi-Fi Available             Indoor Service              Eggs                    Vegan
        2   3       Youth                                                   Prepared Food               Meat                    Vegetarian

    Additional Information:
        - The function reads the `recommended_filters.csv` file from the `resources` directory to create the table.
        - The table includes filter categories and their corresponding filter names.
        - The column headers are retrieved from the `text.json` file, which contains the necessary translations.
        - The placeholder argument `_` is ignored and not used in the function.
        - The function returns the full table of recommended program filters.
    """
    df = RECOMMENDED_FILTERS.copy()
    df.columns = TEXT["RECOMMENDED FILTER OPTIONS"]["columns"]
    return df.reset_index(drop=True)


def create_hour_type_usage_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a table of hour type usage based on the provided DataFrame.

    Args:
        `df` (pd.DataFrame): The Pandas DataFrame containing the data.

    Returns:
        `pd.DataFrame`: A DataFrame containing hour type usage information.

    Preconditions:
        - The Pandas DataFrame must contain the columns `Location External ID`, `Hours Entity Type`, `Frequency`,
          and `Program External ID`.

    Raises:
        None.

    Example:
        >>> data = pd.DataFrame({'Location External ID': ['L1', 'L2', 'L3', 'L4', 'L5'],
                                'Hours Entity Type': ['Location', 'Location', 'Location', 'Location', 'Location'],
                                'Frequency': ['Weekly', 'Every Other Week', 'Week of Month', 'Day of Month', 'Weekly'],
                                'Program External ID': ['P1', 'P2', 'P3', 'P4', 'P5']})
        >>> create_hour_type_usage_table(data)
            Hour Type           Location Usage      Program Usage
        0   Weekly                       1                  1
        1   Every Other Week             1                  1
        2   Week of Month                1                  1
        3   Day of Month                 1                  1

    Additional Information:
        - The function calculates the usage of hour types based on the `Hours Entity Type` and `Frequency` columns in the DataFrame.
        - The table displays the count of unique `Location External ID` and `Program External ID` for each hour type frequency.
        - The hour type frequencies are `Weekly`, `Every Other Week`, `Week of Month`, and `Day of Month`.
        - Ensure that the provided DataFrame contains the necessary columns and represents the relevant data.
        - Table row headers and column headers are pulled from `text.json`.
    """
    locations = [
        df[['Location External ID', 'Hours Entity Type', 'Frequency']].loc[(df['Hours Entity Type'] == 'Location') & (df['Frequency'] == 'Weekly')]['Location External ID'].nunique(),
        df[['Location External ID', 'Hours Entity Type', 'Frequency']].loc[(df['Hours Entity Type'] == 'Location') & (df['Frequency'] == 'Every Other Week')]['Location External ID'].nunique(),
        df[['Location External ID', 'Hours Entity Type', 'Frequency']].loc[(df['Hours Entity Type'] == 'Location') & (df['Frequency'] == 'Week of Month')]['Location External ID'].nunique(),
        df[['Location External ID', 'Hours Entity Type', 'Frequency']].loc[(df['Hours Entity Type'] == 'Location') & (df['Frequency'] == 'Day of Month')]['Location External ID'].nunique()
    ]
    programs = [
        df[['Program External ID', 'Hours Entity Type', 'Frequency']].loc[(df['Hours Entity Type'] == 'Program') & (df['Frequency'] == 'Weekly')]['Program External ID'].nunique(),
        df[['Program External ID', 'Hours Entity Type', 'Frequency']].loc[(df['Hours Entity Type'] == 'Program') & (df['Frequency'] == 'Every Other Week')]['Program External ID'].nunique(),
        df[['Program External ID', 'Hours Entity Type', 'Frequency']].loc[(df['Hours Entity Type'] == 'Program') & (df['Frequency'] == 'Week of Month')]['Program External ID'].nunique(),
        df[['Program External ID', 'Hours Entity Type', 'Frequency']].loc[(df['Hours Entity Type'] == 'Program') & (df['Frequency'] == 'Day of Month')]['Program External ID'].nunique()
    ]
    data = {
        'Hour Type': TEXT["NETWORK HOUR TYPE USAGE"]["rows"],
        'Location Usage': locations,
        'Program Usage': programs,
    }
    return pd.DataFrame(data, columns=TEXT["NETWORK HOUR TYPE USAGE"]["columns"])


def create_organization_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a new DataFrame containing selected columns related to organizations.

    Args:
        df (pd.DataFrame): The input DataFrame containing the data.

    Returns:
        pd.DataFrame: A new DataFrame with columns: `Organization External ID`, `Organization Name`,
        and `Organization Address 1`.

    Preconditions:
        - The input DataFrame `df` should contain the necessary columns:
            - `Organization External ID`
            - `Organization Name`
            - `Organization Address 1`

    Raises:
        None.

    Example:
        >>> data = pd.DataFrame({'Organization External ID': ['O1', 'O2', 'O3'],
                                'Organization Name': ['Org1', 'Org2', 'Org3'],
                                'Organization Address 1': ['Address1', 'Address2', 'Address3']})
        >>> create_organization_table(data)
           Organization ID      Organization Name   Organization Address
        0               O1                  Org1            Address1
        1               O2                  Org2            Address2
        2               O3                  Org3            Address3

    Additional Information:
        - The function extracts specific columns related to organizations from the input DataFrame.
        - The selected columns include:
            - `Organization External ID`: Represents the unique ID of the organization.
            - `Organization Name`: Represents the name of the organization.
            - `Organization Address 1`: Represents the first line of the organization's address.
        - The function creates a new DataFrame containing only the selected columns.
        - Ensure that the input DataFrame `df` represents the relevant data and contains the necessary columns.
        - The resulting DataFrame uses the column headers defined in `text.json` under the `APPENDIX ORGANIZATION LIST` section.
        - The resulting DataFrame is sorted by `Organization External ID` in ascending order.
        - Duplicate values are dropped to ensure unique organizations.
    """
    df = df[['Organization External ID', 'Organization Name', 'Organization Address 1']]
    df.columns = TEXT["APPENDIX ORGANIZATION LIST"]["columns"]
    return df.sort_values(by=TEXT["APPENDIX ORGANIZATION LIST"]["columns"][0], ascending=True).drop_duplicates().reset_index(drop=True)


def create_location_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a table of locations based on the provided DataFrame.

    Args:
        `df` (pd.DataFrame): The Pandas DataFrame containing the data.

    Returns:
        `pd.DataFrame`: A DataFrame containing the location information.

    Preconditions:
        - The Pandas DataFrame must contain the columns `Location External ID`, `Location Name`, and `Location Address 1`.

    Raises:
        None.

    Example:
        >>> data = pd.DataFrame({'Location External ID': ['L1', 'L2', 'L3'],
        ...                     'Location Name': ['Location 1', 'Location 2', 'Location 3'],
        ...                     'Location Address 1': ['Address 1', 'Address 2', 'Address 3']})
        >>> create_location_table(data)
            Location ID     Location Name       Location Address
        0           L1          Location 1              Address 1
        1           L2          Location 2              Address 2
        2           L3          Location 3              Address 3

    Additional Information:
        - The function extracts the specified columns from the provided DataFrame to create a location table.
        - The required columns include:
            - `Location External ID`: Represents the unique ID of the location.
            - `Location Name`: Represents the name of the location.
            - `Location Address 1`: Represents the first line of the location's address.
        - The function creates a new DataFrame containing only the selected columns.
        - Ensure that the provided DataFrame contains the necessary columns and represents the relevant location data.
        - The resulting DataFrame uses the column headers defined in `text.json` under the `APPENDIX LOCATION LIST` section.
        - The resulting DataFrame is sorted by `Location External ID` in ascending order.
        - Duplicate values are dropped to ensure unique locations.
    """
    df = df[['Location External ID', 'Location Name', 'Location Address 1']]
    df.columns = TEXT["APPENDIX LOCATION LIST"]["columns"]
    return df.sort_values(by=TEXT["APPENDIX LOCATION LIST"]["columns"][0], ascending=True).drop_duplicates().reset_index(drop=True)


def create_program_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a table of programs based on the provided DataFrame.

    Args:
        `df` (pd.DataFrame): The Pandas DataFrame containing the data.

    Returns:
        `pd.DataFrame`: A DataFrame containing the program information.

    Preconditions:
        - The Pandas DataFrame must contain the columns `Program External ID` and `Program Name`.

    Raises:
        None.

    Example:
        >>> data = pd.DataFrame({'Program External ID': ['P1', 'P2', 'P3'],
        ...                     'Program Name': ['Program 1', 'Program 2', 'Program 3']})
        >>> create_program_table(data)
            Program ID      Program Name
        0           P1          Program 1
        1           P2          Program 2
        2           P3          Program 3

    Additional Information:
        - The function extracts the specified columns (`Program External ID` and `Program Name`) from the provided DataFrame to create a program table.
        - The columns `Program External ID` and `Program Name` are required to be present in the DataFrame.
        - The resulting table displays the `Program External ID` and name for each program.
        - Ensure that the provided DataFrame contains the necessary columns and represents the relevant program data.
        - The column headers for the table are sourced from `text.json` using the `APPENDIX PROGRAM LIST` section.
        - The values in the table are sorted by `Program External ID` in ascending order.
    """
    df = df[['Program External ID', 'Program Name']]
    df.columns = TEXT["APPENDIX PROGRAM LIST"]["columns"]
    return df.sort_values(by=TEXT["APPENDIX PROGRAM LIST"]["columns"][0], ascending=True).drop_duplicates().reset_index(drop=True)


def create_profile_completion_tiers_table(_: any) -> pd.DataFrame:
    """
    Creates a table of profile completion tiers.

    Args:
        `_` (any): This parameter is not used and can be ignored.

    Returns:
        `pd.DataFrame`: A DataFrame containing the profile completion tiers.

    Preconditions:
        - The global variable `PROFILE_COMPLETION_TIERS` must be defined and contain the path to the `profile_completion_tiers.csv` file.

    Raises:
        None.

    Example:
        >>> create_profile_completion_tiers_table(None)
            Tier Level      Minimum     Maximum
        0   Basic               0           20
        1   Quality             21          35
        2   Exceptional         36

    Additional Information:
        - The function returns a predefined table of profile completion tiers.
        - The tiers are categorized based on the score range.
        - The table contains three columns: `Tier Level`, `Minimum`, and `Maxaximum`.
        - Each row represents a profile completion tier with its corresponding score range.
        - The tiers are defined as `Basic`, `Quality`, and `Exceptional`.
        - This function does not require any input data or parameters.
        - The `PROFILE_COMPLETION_TIERS` variable is a global variable that should be defined in the code
          and should contain the path to the `profile_completion_tiers.csv` file.
        - The column headers for the table are sourced from `text.json` using the `APPENDIX PROGRAM PROFILE COMPLETION TIERS` section.
        - The values in the table are sorted by the `Minimum` column in ascending order.
    """
    df = PROFILE_COMPLETION_TIERS.copy()
    df.columns = TEXT["APPENDIX PROGRAM PROFILE COMPLETION TIERS"]["columns"]
    return df.sort_values(by=TEXT["APPENDIX PROGRAM PROFILE COMPLETION TIERS"]["columns"][1], ascending=True).reset_index(drop=True)


def create_program_category_field_weights(_: any) -> pd.DataFrame:
    """
    Creates a table of program category field weights.

    Args:
        `_` (any): This parameter is not used and can be ignored.

    Returns:
        `pd.DataFrame`: A DataFrame containing the program category field weights.

    Preconditions:
        - The global variable `WEIGHTS` must be defined and contain the field weights.
        - The `weights.json` file must be present in the working directory's `resource` folder to access the completion weight for each column.

    Raises:
        None.

    Example:
        >>> create_program_category_field_weights(None)
                            Field         Weight
        0   Program Contact Phone            1
        1   Program Contact Phone Ext        0
        2   Program Contact Email            1

    Additional Information:
        - The function returns a table of program category field weights.
        - The field weights are defined in the global variable `WEIGHTS`.
        - The table contains two columns: `Field` and `Weight`.
        - Each row represents a program category field with its corresponding weight.
        - The `WEIGHTS` variable is a global variable that should be defined in the code from the `weights.json` file stored in the `resources` folder.
        - This function does not require any input data or parameters.
        - The column headers for the table are sourced from `text.json` using the `APPENDIX PROGRAM CATEGORY FIELD WEIGHTS` section.
        - The values in the table are sorted by the `Weight` column in descending order.
    """
    df = pd.DataFrame.from_dict(WEIGHTS, orient='index').reset_index()
    df.columns = TEXT["APPENDIX PROGRAM CATEGORY FIELD WEIGHTS"]["columns"]
    return df.sort_values(by=TEXT["APPENDIX PROGRAM CATEGORY FIELD WEIGHTS"]["columns"][1], ascending=False).reset_index(drop=True)


def create_program_profile_completion_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a table of program profile completion grades based on the provided DataFrame.

    Args:
        `df` (pd.DataFrame): The Pandas DataFrame containing the data.

    Returns:
        `pd.DataFrame`: A DataFrame containing program profile completion grades for each Location.

    Preconditions:
        - The Pandas DataFrame must contain the columns `Location External ID` and any columns needed to calculate the profile completion grades.
        - The global variable `WEIGHTS` must be defined and contain the field weights.
        - `weights.json` file must be present in the working directory's `resource` folder to access the completion weight for each column.

    Raises:
        None.

    Example:
        >>> data = pd.DataFrame({'Location External ID': ['L1', 'L2', 'L3'],
        ...                     'Location Name': [None, None, 'Good Food'],
        ...                     'Location ZIP': [715359, None, 136135],
        ...                     'Hours Entity Type': ['Program', 'Location', 'Location']})
        >>> create_program_profile_completion_table(data)
            Location ID     Profile Score   Tier Level
        0           L1              5           Basic
        1           L2              5           Basic
        2           L3              8           Basic

    Additional Information:
        - The function calculates the program profile completion score based on the provided DataFrame.
        - Each cell in the DataFrame is checked for the presence of a value. Present values are replaced with 1, and absent values are replaced with 0.
        - The function then multiplies the integers by the corresponding weight from `weights.json` to calculate the profile completion score for each row.
        - The table displays the maximum profile score for each location based on the `Location External ID`.
        - The profile completion grades model after the internal scores Vivery uses to measure profile completeness.
        - The calculated score determines the Tier Level displayed in the table:
            - Score >= 36: Exceptional
            - Score >= 21: Quality
            - Score <= 20: Basic
        - The column headers for the table are sourced from `text.json` using the `APPENDIX PROGRAM PROFILE COMPLETION LIST` section.
        - The values in the table are sorted by the `Profile Score` column in descending order.
        - To ensure an accurate calculation, make sure all required columns are present in the DataFrame.
    """
    df2 = df.copy()
    df2["Profile Score"] = df2.notnull().astype('int').mul(WEIGHTS).sum(axis=1)
    df2 = df2[["Location External ID", "Profile Score"]].groupby(['Location External ID']).max().reset_index()
    df2["Tier Level"] = df2["Profile Score"].apply(lambda score: PROFILE_COMPLETION_TIERS["Tier"][2] if score >= 36 else PROFILE_COMPLETION_TIERS["Tier"][1] if score >= 21 else PROFILE_COMPLETION_TIERS["Tier"][0])
    df2.columns = TEXT["APPENDIX PROGRAM PROFILE COMPLETION LIST"]["columns"]
    return df2.sort_values(by=TEXT["APPENDIX PROGRAM PROFILE COMPLETION LIST"]["columns"][1], ascending=False).drop_duplicates().reset_index(drop=True)


def create_organization_contact_information_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a table of organization contact information based on the provided DataFrame.

    Args:
        `df` (pd.DataFrame): The Pandas DataFrame containing the organization data.

    Returns:
        `pd.DataFrame`: A DataFrame containing the organization contact information.

    Preconditions:
        - The Pandas DataFrame must contain the columns:
            - `Organization External ID`
            - `Organization Contact Name`
            - `Organization Contact Email`
            - `Organization Contact Phone`

    Raises:
        None.

    Example:
        >>> data = pd.DataFrame({
        ...     'Organization External ID': ['O1', 'O2', 'O3'],
        ...     'Organization Contact Name': ['John Doe', 'Jane Smith', 'Adam Johnson'],
        ...     'Organization Contact Email': ['john@example.com', 'jane@example.com', 'adam@example.com'],
        ...     'Organization Contact Phone': ['123456789', '987654321', '555555555']
        ... })
        >>> create_organization_contact_information_table(data)
            Organization ID      Name               Email                   Phone
        0               O1          John Doe            john@example.com        123456789
        1               O2          Jane Smith          jane@example.com        987654321
        2               O3          Adam Johnson        adam@example.com        555555555

    Additional Information:
        - The function extracts the organization contact information from the provided DataFrame.
        - The resulting table includes the following columns: `Organization External ID`,
          `Organization Contact Name`, `Organization Contact Email`, and `Organization Contact Phone`.
        - It is essential to ensure that the provided DataFrame contains all the necessary columns and represents the relevant data.
        - The column headers for the table are sourced from `text.json` using the `APPENDIX ORGANIZATION CONTACT INFORMATION` section.
        - The values in the table are sorted by the `Organization External ID` column in ascending order.
    """
    df = df[['Organization External ID', 'Organization Contact Name', 'Organization Contact Email', 'Organization Contact Phone']]
    df.columns = TEXT["APPENDIX ORGANIZATION CONTACT INFORMATION"]["columns"]
    return df.sort_values(by=TEXT["APPENDIX ORGANIZATION CONTACT INFORMATION"]["columns"][0], ascending=True).drop_duplicates().reset_index(drop=True)


def create_location_contact_information_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a table of location contact information based on the provided DataFrame.

    Args:
        `df` (pd.DataFrame): The Pandas DataFrame containing the location data.

    Returns:
        `pd.DataFrame`: A DataFrame containing the location contact information.

    Preconditions:
        - The Pandas DataFrame must contain the columns `Location External ID`, `Location Contact Name`,
          `Location Contact Email`, `Location Contact Phone`, and `Location Website`.

    Raises:
        None.

    Example:
        >>> data = pd.DataFrame({'Location External ID': ['L1', 'L2', 'L3'],
                                'Location Contact Name': ['John Doe', 'Jane Smith', 'Mark Johnson'],
                                'Location Contact Email': ['john@example.com', 'jane@example.com', 'mark@example.com'],
                                'Location Contact Phone': ['123456789', '987654321', '456123789'],
                                'Location Website': ['www.location1.com', 'www.location2.com', 'www.location3.com']})
        >>> create_location_contact_information_table(data)
            Location ID         Name            Email                   Phone           Website
        0           L1          John Doe            john@example.com        123456789       www.location1.com
        1           L2          Jane Smith          jane@example.com        987654321       www.location2.com
        2           L3          Mark Johnson        mark@example.com        456123789       www.location3.com

    Additional Information:
        - The function extracts the relevant columns from the provided DataFrame: `Location External ID`,
          `Location Contact Name`, `Location Contact Email`, `Location Contact Phone`, and `Location Website`.
        - The resulting DataFrame is sorted in ascending order based on the first column name specified in
          the `APPENDIX LOCATION CONTACT INFORMATION` section of `text.json`.
        - Ensure that the provided DataFrame contains all the necessary columns and represents the relevant data.
        - The column headers for the table are sourced from `text.json` using the `APPENDIX LOCATION CONTACT INFORMATION` section.
    """
    df = df[['Location External ID', 'Location Contact Name', 'Location Contact Email', 'Location Contact Phone', 'Location Website']]
    df.columns = TEXT["APPENDIX LOCATION CONTACT INFORMATION"]["columns"]
    return df.sort_values(by=TEXT["APPENDIX LOCATION CONTACT INFORMATION"]["columns"][0], ascending=True).drop_duplicates().reset_index(drop=True)
    

def create_program_contact_information_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a table of program contact information based on the provided DataFrame.

    Args:
        `df` (pd.DataFrame): The Pandas DataFrame containing the program and location data.

    Returns:
        `pd.DataFrame`: A DataFrame containing the program contact information.

    Preconditions:
        - The Pandas DataFrame must contain the columns:
            - `Program External ID`
            - `Program Contact Name`
            - `Program Contact Email`
            - `Program Contact Phone`
            - `Location External ID`
            - `Location Contact Name`
            - `Location Contact Email`
            - `Location Contact Phone`
            - `Program Use Same Contact As Location`

    Raises:
        None.

    Example:
        >>> data = pd.DataFrame({
        ...     'Program External ID': ['P1', 'P2', 'P3'],
        ...     'Program Contact Name': ['John Doe', 'Jane Smith', 'Adam Johnson'],
        ...     'Program Contact Email': ['john@example.com', 'jane@example.com', 'adam@example.com'],
        ...     'Program Contact Phone': ['123456789', '987654321', '555555555'],
        ...     'Location External ID': ['L1', 'L2', 'L3'],
        ...     'Location Contact Name': ['Sarah Johnson', 'Robert Davis', 'Emma Thompson'],
        ...     'Location Contact Email': ['sarah@example.com', 'robert@example.com', 'emma@example.com'],
        ...     'Location Contact Phone': ['999888777', '777888999', '111222333'],
        ...     'Program Use Same Contact As Location': [True, False, True]
        ... })
        >>> create_program_contact_information_table(data)
            Program ID       Program Contact Name           Program Contact Email           Program Contact Phone
        0           P1                  Sarah Johnson                   sarah@example.com               999888777
        1           P2                  Jane Smith                      jane@example.com                987654321
        2           P3                  Emma Thompson                   emma@example.com                555555555

    Additional Information:
        - The function extracts the program contact information from the provided DataFrame.
        - If the `Program Use Same Contact As Location` flag is set to True, the function retrieves the contact
          information from the corresponding location columns instead of the program columns.
        - The resulting DataFrame includes the columns: `Program External ID`, `Program Contact Name`,
          `Program Contact Email`, and `Program Contact Phone`.
        - Ensure that the provided DataFrame contains the necessary columns and represents the relevant data.
        - The resulting DataFrame is sorted in ascending order based on the first column name specified in
          the `APPENDIX PROGRAM LIST` section.
        - Table column headers are pulled from `text.json`.
    """
    program_contact_info = df[['Program External ID', 'Program Contact Name', 'Program Contact Email', 'Program Contact Phone']]
    location_contact_info = df[['Program External ID', 'Location Contact Name', 'Location Contact Email', 'Location Contact Phone']]
    program_contact_info.loc[df['Program Use Same Contact As Location'] == True] = location_contact_info.loc[df['Program Use Same Contact As Location'] == True]
    program_contact_info.columns = TEXT["APPENDIX PROGRAM CONTACT INFORMATION"]["columns"]
    return program_contact_info.sort_values(by=TEXT["APPENDIX PROGRAM LIST"]["columns"][0], ascending=True).drop_duplicates().reset_index(drop=True)
    

def create_program_by_program_type_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a table of programs grouped by program type based on the provided DataFrame.

    Args:
        `df` (pd.DataFrame): The Pandas DataFrame containing the program data.

    Returns:
        `pd.DataFrame`: A DataFrame containing programs grouped by program type.

    Preconditions:
        - The Pandas DataFrame must contain the columns:
            - `Program External ID`
            - `Program Service Category`
            - `Food Program Category`

    Raises:
        None.

    Example:
        >>> data = pd.DataFrame({
        ...     'Program External ID': ['P1', 'P2', 'P3'],
        ...     'Program Service Category': ['Food Program', 'Case Management Services', 'Housing Assistance'],
        ...     'Food Program Category': ['Food Distribution', 'Hot/Cold Meal Program', 'Other']
        ... })
        >>> create_program_by_program_type_table(data)
            Program ID           Program Type                    Type Specification
        0           P1               Food Program                    Food Distribution
        1           P2               Case Management Services        Hot/Cold Meal Program
        2           P3               Housing Assistance              Other

    Additional Information:
        - The function groups programs based on their program type, represented by the `Program Service Category`
          column, and their type specification, represented by the `Food Program Category` column.
        - The resulting DataFrame includes the columns: `Program External ID`, `Program Type`, and `Type Specification`.
        - The function removes any duplicate rows in the resulting DataFrame.
        - Ensure that the provided DataFrame contains the necessary columns and represents the relevant data.
        - Table column headers are pulled from `text.json`.
    """
    df = df[['Program External ID', 'Program Service Category', 'Food Program Category']]
    df.columns = TEXT["APPENDIX PROGRAM TYPE"]["columns"]
    return df.drop_duplicates().reset_index(drop=True)


def create_program_by_program_audience_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a table of programs categorized by their program audience groups based on the provided DataFrame.

    Args:
        `df` (pd.DataFrame): The Pandas DataFrame containing the program data.

    Returns:
        `pd.DataFrame`: A DataFrame containing the program external IDs and their corresponding program audience groups.

    Preconditions:
        - The Pandas DataFrame must contain the columns `Program External ID` and `Program Audience Groups`.

    Raises:
        None.

    Example:
        >>> data = pd.DataFrame({
        ...     'Program External ID': ['P1', 'P2', 'P3', 'P4', 'P5'],
        ...     'Program Audience Groups': ['Teenagers / Young Adults;LGBTQ+', 'LGBTQ+', 'LGBTQ+', 'Veterans', 'Homebound']
        ... })
        >>> create_program_by_program_audience_table(data)
            Program ID          Program Audience
        0           P1                  Teenagers / Young Adults;LGBTQ+
        1           P2                  LGBTQ+
        2           P3                  LGBTQ+
        3           P4                  Veterans
        4           P5                  Homebound

    Additional Information:
        - The function extracts the columns `Program External ID` and `Program Audience Groups` from the provided DataFrame.
        - Duplicate rows are dropped to ensure each program external ID is listed only once in the resulting DataFrame.
        - The resulting DataFrame provides a mapping between program external IDs and their corresponding program audience groups.
        - Ensure that the provided DataFrame contains the necessary columns and represents the relevant program data.
        - Table column headers are pulled from `text.json`.
    """
    df = df[['Program External ID', 'Program Audience Groups']]
    df.columns = TEXT["APPENDIX PROGRAM AUDIENCE"]["columns"]
    return df.sort_values(by=TEXT["APPENDIX PROGRAM AUDIENCE"]["columns"][0], ascending=True).drop_duplicates().reset_index(drop=True)


def create_program_by_program_languages_spoken_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a table of programs categorized by the languages spoken based on the provided DataFrame.

    Args:
        `df` (pd.DataFrame): The Pandas DataFrame containing the program data.

    Returns:
        `pd.DataFrame`: A DataFrame containing the program external IDs and their corresponding languages spoken.

    Preconditions:
        - The Pandas DataFrame must contain the columns `Program External ID` and `Languages Spoken`.

    Raises:
        None.

    Example:
        >>> data = pd.DataFrame({
        ...     'Program External ID': ['P1', 'P2', 'P3', 'P4', 'P5'],
        ...     'Languages Spoken': ['English', 'Spanish', 'English; Spanish', 'Japanese', 'English; French']
        ... })
        >>> create_program_by_program_languages_spoken_table(data)
            Program ID   Program Languages
        0           P1          English
        1           P2          Spanish
        2           P3          English;Spanish
        3           P4          Japanese
        4           P5          English;French

    Additional Information:
        - The function extracts the columns `Program External ID` and `Languages Spoken` from the provided DataFrame.
        - Duplicate rows are dropped to ensure each program external ID is listed only once in the resulting DataFrame.
        - The resulting DataFrame provides a mapping between program external IDs and their corresponding languages spoken.
        - The languages spoken may be listed as a single language or a combination of multiple languages.
        - Ensure that the provided DataFrame contains the necessary columns and represents the relevant program data.
        - Table column headers are pulled from `text.json`.
    """
    df = df[['Program External ID', 'Languages Spoken']]
    df.columns = TEXT["APPENDIX PROGRAM LANGUAGES SPOKEN"]["columns"]
    return df.sort_values(by=TEXT["APPENDIX PROGRAM LANGUAGES SPOKEN"]["columns"][0], ascending=True).drop_duplicates().reset_index(drop=True)


def create_program_by_program_features_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a table of programs categorized by the program features based on the provided DataFrame.

    Args:
        `df` (pd.DataFrame): The Pandas DataFrame containing the program data.

    Returns:
        `pd.DataFrame`: A DataFrame containing the program external IDs and their corresponding program features.

    Preconditions:
        - The Pandas DataFrame must contain the columns `Program External ID` and `Food Program Features`.

    Raises:
        None.

    Example:
        >>> data = pd.DataFrame({
        ...     'Program External ID': ['P1', 'P2', 'P3', 'P4', 'P5'],
        ...     'Food Program Features': ['Grocery / Client Choice', 'Home Delivery Service', 'Pre-Packed Boxes / Bags', 'Outdoor Seating', 'Other']
        ... })
        >>> create_program_by_program_features_table(data)
            Program ID     Program Features
        0           P1              Grocery / Client Choice
        1           P2              Home Delivery Service
        2           P3              Pre-Packed Boxes / Bags
        3           P4              Outdoor Seating
        4           P5              Other

    Additional Information:
        - The function extracts the columns `Program External ID` and `Food Program Features` from the provided DataFrame.
        - Duplicate rows are dropped to ensure each program external ID is listed only once in the resulting DataFrame.
        - The resulting DataFrame provides a mapping between program external IDs and their corresponding program features.
        - Ensure that the provided DataFrame contains the necessary columns and represents the relevant program data.
        - Table column headers are pulled from `text.json`.
    """
    df = df[['Program External ID', 'Food Program Features']]
    df.columns = TEXT["APPENDIX PROGRAM FEATURES"]["columns"]
    return df.sort_values(by=TEXT["APPENDIX PROGRAM FEATURES"]["columns"][0], ascending=True).drop_duplicates().reset_index(drop=True)


def create_program_by_program_items_offered_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a table of programs categorized by dietary options based on the provided DataFrame.

    Args:
        `df` (pd.DataFrame): The Pandas DataFrame containing the program data.

    Returns:
        `pd.DataFrame`: A DataFrame containing the program external IDs and their corresponding dietary options.

    Preconditions:
        - The Pandas DataFrame must contain the columns `Program External ID` and `Items Offered`.

    Raises:
        None.

    Example:
        >>> data = pd.DataFrame({
        ...     'Program External ID': ['P1', 'P2', 'P3', 'P4', 'P5'],
        ...     'Items Offered': ['Dairy', 'Eggs', 'Meat', 'Fruits & Vegetables', 'Shelf-Stable / Non-Perishable Goods']
        ... })
        >>> create_program_by_program_dietary_options_table(data)
            Program ID      Items Offered
        0           P1              Dairy
        1           P2              Eggs
        2           P3              Meat
        3           P4              Fruits & Vegetables
        4           P5              Shelf-Stable / Non-Perishable Goods


    Additional Information:
        - The function extracts the columns `Program External ID` and `Items Offered` from the provided DataFrame.
        - Duplicate rows are dropped to ensure each program external ID is listed only once in the resulting DataFrame.
        - The resulting DataFrame provides a mapping between program external IDs and their corresponding dietary options.
        - The dietary options may include categories such as vegetarian, vegan, gluten-free, etc.
        - Ensure that the provided DataFrame contains the necessary columns and represents the relevant program data.
        - Table column headers are pulled from `text.json`.
    """
    df = df[['Program External ID', 'Items Offered']]
    df.columns = TEXT["APPENDIX PROGRAM ITEMS OFFERED"]["columns"]
    return df.sort_values(by=TEXT["APPENDIX PROGRAM ITEMS OFFERED"]["columns"][0], ascending=True).drop_duplicates().reset_index(drop=True)


def create_program_by_program_dietary_options_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a table of programs categorized by dietary options based on the provided DataFrame.

    Args:
        `df` (pd.DataFrame): The Pandas DataFrame containing the program data.

    Returns:
        `pd.DataFrame`: A DataFrame containing the program external IDs and their corresponding dietary options.

    Preconditions:
        - The Pandas DataFrame must contain the columns `Program External ID` and `Dietary Options Available`.

    Raises:
        None.

    Example:
        >>> data = pd.DataFrame({
        ...     'Program External ID': ['P1', 'P2', 'P3', 'P4', 'P5'],
        ...     'Dietary Options Available': ['Gluten Free', 'Vegan', 'Halal', 'Vegetarian', 'Other']
        ... })
        >>> create_program_by_program_dietary_options_table(data)
            Program ID         Dietary Options Available
        0           P1                      Gluten Free
        1           P2                      Vegan
        2           P3                      Halal
        3           P4                      Vegetarian
        4           P5                      Other

    Additional Information:
        - The function extracts the columns `Program External ID` and `Dietary Options Available` from the provided DataFrame.
        - Duplicate rows are dropped to ensure each program external ID is listed only once in the resulting DataFrame.
        - The resulting DataFrame provides a mapping between program external IDs and their corresponding dietary options.
        - The dietary options may include categories such as vegetarian, vegan, gluten-free, etc.
        - The resulting DataFrame is sorted based on the `Program External ID` column in ascending order.
        - Ensure that the provided DataFrame contains the necessary columns and represents the relevant program data.
        - Table column headers are pulled from `text.json`.
    """
    df = df[['Program External ID', 'Dietary Options Available']]
    df.columns = TEXT["APPENDIX PROGRAM DIETARY OPTIONS"]["columns"]
    return df.sort_values(by=TEXT["APPENDIX PROGRAM DIETARY OPTIONS"]["columns"][0], ascending=True).drop_duplicates().reset_index(drop=True)


def create_location_hours_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a table of location hours based on the provided DataFrame.

    Args:
        `df` (pd.DataFrame): The Pandas DataFrame containing the location hours data.

    Returns:
        `pd.DataFrame`: A DataFrame containing the location external IDs, hours, day of week, and frequency.

    Preconditions:
        - The Pandas DataFrame must contain the columns `Location External ID`, `Hours Entity Type`, `Hours Open X`, `Hours Closed X`, `Day of Week`, `Frequency`, and `Specific Date`.

    Raises:
        None.

    Example:
        >>> data = pd.DataFrame({
        ...     'Location External ID': [1992, 1993, 1992, 1992],
        ...     'Hours Entity Type': ['Location', 'Location', 'Location', 'Location'],
        ...     'Hours Open 1': ['9:30', '11:00', '13:00', '17:00'],
        ...     'Hours Closed 1': ['11:30', '13:00', '15:00', '19:00'],
        ...     'Day of Week': ['Sunday', '2023-05-13', 'Sunday', 'Sunday'],
        ...     'Frequency': ['Weekly', 'Date Specific', 'Weekly', 'Weekly'],
        ...     'Specific Date': [None, None, None, None]
        ... })
        >>> create_location_hours_table(data)
            Location ID         Hours Type          Opening Hour      Closing Hour          Day             Frequency
        0           1992             Location             9:30              11:30           Sunday              Weekly
        1           1993             Location            11:00              13:00           2023-05-13          Date Specific
        2           1992             Location            13:00              15:00           Sunday              Weekly
        3           1992             Location            17:00              19:00           Sunday              Weekly

    Additional Information:
        - The function extracts the relevant columns from the provided DataFrame to create the location hours table.
        - Rows are filtered based on the conditions: `Hours Entity Type` is `Location`, and `Hours Open X` and `Hours Closed X` are not null.
        - The resulting table includes columns for location external ID, hours open, hours closed, day of the week, and frequency.
        - Duplicate rows are dropped to ensure each set of location hours appears only once in the resulting table.
        - The `Frequency` column is filled with `Date Specific` for rows where the `Frequency` column is null.
        - The `Day of Week` column is filled with values from the `Specific Date` column for rows where `Day of Week` is null.
        - The resulting DataFrame is sorted based on the `Location External ID` column in ascending order.
        - Ensure that the provided DataFrame contains the necessary columns and represents the relevant location hours data.
        - Table column headers are pulled from `text.json`.
    """
    location_hours_one = df[['Location External ID', 'Hours Entity Type', 'Hours Open 1', 'Hours Closed 1', 'Day of Week', 'Frequency']].loc[(df['Hours Entity Type'] == 'Location')  & (df['Hours Open 1'].notna()) & (df['Hours Closed 1'].notna())].rename(columns={'Hours Open 1': 'Hours Open',
                                                                                                                                                                                                                                      'Hours Closed 1': 'Hours Closed'})
    location_hours_two = df[['Location External ID', 'Hours Entity Type', 'Hours Open 2', 'Hours Closed 2', 'Day of Week', 'Frequency']].loc[(df['Hours Entity Type'] == 'Location')  & (df['Hours Open 2'].notna()) & (df['Hours Closed 2'].notna())].rename(columns={'Hours Open 2': 'Hours Open',
                                                                                                                                                                                                                                      'Hours Closed 2': 'Hours Closed'})
    location_hours_three = df[['Location External ID', 'Hours Entity Type', 'Hours Open 3', 'Hours Closed 3', 'Day of Week', 'Frequency']].loc[(df['Hours Entity Type'] == 'Location')  & (df['Hours Open 3'].notna())  & (df['Hours Closed 3'].notna())].rename(columns={'Hours Open 3': 'Hours Open',
                                                                                                                                                                                                                                      'Hours Closed 3': 'Hours Closed'})
    location_hours = pd.concat([location_hours_one, location_hours_two, location_hours_three], axis=0).drop_duplicates()
    location_hours['Frequency'] = location_hours['Frequency'].fillna('Date Specific')
    location_date_specific = df['Specific Date'].loc[(df['Hours Entity Type'] == 'Location')].dropna().drop_duplicates()
    location_hours['Day of Week'] = location_hours['Day of Week'].fillna(location_date_specific)
    location_hours.columns = TEXT["APPENDIX LOCATION HOURS INFORMATION"]["columns"]
    return location_hours.sort_values(by=TEXT["APPENDIX LOCATION HOURS INFORMATION"]["columns"][0], ascending=True).drop_duplicates().reset_index(drop=True)


def create_program_hours_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a table of program hours based on the provided DataFrame.

    Args:
        `df` (pd.DataFrame): The Pandas DataFrame containing the program hours data.

    Returns:
        `pd.DataFrame`: A DataFrame containing the program external IDs, hours, day of week, and frequency.

    Preconditions:
        - The Pandas DataFrame must contain the columns `Program External ID`, `Hours Entity Type`, `Hours Open X`, `Hours Closed X`, `Day of Week`, `Frequency`, and `Specific Date`.

    Raises:
        None.

    Example:
        >>> data = pd.DataFrame({
        ...     'Program External ID': [1992, 1993, 1992, 1992],
        ...     'Hours Entity Type': ['Program', 'Program', 'Program', 'Program'],
        ...     'Hours Open 1': ['9:30', '11:00', '13:00', '17:00'],
        ...     'Hours Closed 1': ['11:30', '13:00', '15:00', '19:00'],
        ...     'Day of Week': ['Sunday', '2023-05-13', 'Sunday', 'Sunday'],
        ...     'Frequency': ['Weekly', 'Date Specific', 'Weekly', 'Weekly'],
        ...     'Specific Date': [None, None, None, None]
        ... })
        >>> create_program_hours_table(data)
            Program ID          Hours Type          Opening Hour      Closing Hour          Day             Frequency
        0           1992             Program             9:30               11:30           Sunday              Weekly
        1           1993             Program            11:00               13:00           2023-05-13          Date Specific
        2           1992             Program            13:00               15:00           Sunday              Weekly
        3           1992             Program            17:00               19:00           Sunday              Weekly

    Additional Information:
        - The function extracts the relevant columns from the provided DataFrame to create the program hours table.
        - Rows are filtered based on the conditions: `Hours Entity Type` is `Program`, and `Hours Open X` and `Hours Closed X` are not null.
        - The resulting table includes columns for program external ID, hours open, hours closed, day of the week, and frequency.
        - Duplicate rows are dropped to ensure each set of program hours appears only once in the resulting table.
        - The `Frequency` column is filled with `Date Specific` for rows where the `Frequency` column is null.
        - The `Day of Week` column is filled with values from the `Specific Date` column for rows where `Day of Week` is null.
        - The resulting DataFrame is sorted based on the `Program External ID` column in ascending order.
        - Ensure that the provided DataFrame contains the necessary columns and represents the relevant program hours data.
        - Table column headers are pulled from `text.json`.
    """
    program_hours_one = df[['Program External ID', 'Hours Entity Type', 'Hours Open 1', 'Hours Closed 1', 'Day of Week', 'Frequency']].loc[(df['Hours Entity Type'] == 'Program')  & (df['Hours Open 1'].notna()) & (df['Hours Closed 1'].notna())].rename(columns={'Hours Open 1': 'Hours Open',
                                                                                                                                                                                                                                      'Hours Closed 1': 'Hours Closed'})
    program_hours_two = df[['Program External ID', 'Hours Entity Type', 'Hours Open 2', 'Hours Closed 2', 'Day of Week', 'Frequency']].loc[(df['Hours Entity Type'] == 'Program')  & (df['Hours Open 2'].notna()) & (df['Hours Closed 2'].notna())].rename(columns={'Hours Open 2': 'Hours Open',
                                                                                                                                                                                                                                      'Hours Closed 2': 'Hours Closed'})
    program_hours_three = df[['Program External ID', 'Hours Entity Type', 'Hours Open 3', 'Hours Closed 3', 'Day of Week', 'Frequency']].loc[(df['Hours Entity Type'] == 'Program')  & (df['Hours Open 3'].notna())  & (df['Hours Closed 3'].notna())].rename(columns={'Hours Open 3': 'Hours Open',
                                                                                                                                                                                                                                      'Hours Closed 3': 'Hours Closed'})
    program_hours = pd.concat([program_hours_one, program_hours_two, program_hours_three], axis=0).drop_duplicates()
    program_hours['Frequency'] = program_hours['Frequency'].fillna('Date Specific')
    program_date_specific = df['Specific Date'].loc[(df['Hours Entity Type'] == 'Program')].dropna().drop_duplicates()
    program_hours['Day of Week'] = program_hours['Day of Week'].fillna(program_date_specific)
    program_hours.columns = TEXT["APPENDIX PROGRAM HOURS INFORMATION"]["columns"]
    return program_hours.sort_values(by=TEXT["APPENDIX PROGRAM HOURS INFORMATION"]["columns"][0], ascending=True).drop_duplicates().reset_index(drop=True)


def create_program_by_program_qualifications_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a table of programs categorized by qualifications based on the provided DataFrame.

    Args:
        `df` (pd.DataFrame): The Pandas DataFrame containing the program data.

    Returns:
        `pd.DataFrame`: A DataFrame containing the program external IDs and their corresponding qualifications.

    Preconditions:
        - The Pandas DataFrame must contain the columns `Program External ID` and `Program Qualifications`.

    Raises:
        None.

    Example:
        >>> data = pd.DataFrame({
        ...     'Program External ID': ['P1', 'P2', 'P3', 'P4', 'P5'],
        ...     'Program Qualifications': ['Within the service area', 'Seniors only', 'Students only', 'None', 'None']
        ... })
        >>> create_program_by_program_qualifications_table(data)
            Program ID       Program Qualifications
        0           P1                      Within the service area
        1           P2                      Seniors only
        2           P3                      Students only
        3           P4                      None
        4           P5                      None


    Additional Information:
        - The function extracts the columns `Program External ID` and `Program Qualifications` from the provided DataFrame.
        - Duplicate rows are dropped to ensure each program external ID is listed only once in the resulting table.
        - The resulting table provides a mapping between program external IDs and their corresponding qualifications.
        - The qualifications may include categories such as certified, licensed, qualified, etc.
        - The resulting DataFrame is sorted based on the `Program External ID` column in ascending order.
        - Ensure that the provided DataFrame contains the necessary columns and represents the relevant program data.
        - Table column headers are pulled from `text.json`.
    """
    df = df[['Program External ID', 'Program Qualifications']]
    df.columns = TEXT["APPENDIX PROGRAM QUALIFICATIONS"]["columns"]
    return df.sort_values(by=TEXT["APPENDIX PROGRAM QUALIFICATIONS"]["columns"][0], ascending=True).drop_duplicates().reset_index(drop=True)


def create_program_by_program_services_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a table of programs categorized by service area based on the provided DataFrame.

    Args:
        `df` (pd.DataFrame): The Pandas DataFrame containing the program data.

    Returns:
        `pd.DataFrame`: A DataFrame containing the program external IDs and their corresponding services.

    Preconditions:
        - The Pandas DataFrame must contain the columns `Program External ID` and `Program Service Area`.

    Raises:
        None.

    Example:
        >>> data = pd.DataFrame({
        ...     'Program External ID': ['P1', 'P2', 'P3', 'P4', 'P5'],
        ...     'Program Service Area': ['County: Greendale; Zip Code: 10023/40192', 'County: Los Angeles; Zip Code: 90272', 'County: Vancouver; Zip Code: V6Z2T9', 'County: Greendale; Zip Code: 10023/40192', 'County: Greendale; Zip Code: 10023/40192']
        ... })
        >>> create_program_by_program_services_table(data)
            Program ID         Program Service Area
        0           P1                  County: Greendale; Zip Code: 10023/40192
        1           P2                  County: Los Angeles; Zip Code: 90272
        2           P3                  County: Vancouver; Zip Code: V6Z2T9
        3           P4                  County: Greendale; Zip Code: 10023/40192
        4           P5                  County: Greendale; Zip Code: 10023/40192

    Additional Information:
        - The function extracts the columns `Program External ID` and `Program Service Area` from the provided DataFrame.
        - Duplicate rows are dropped to ensure each program external ID is listed only once in the resulting table.
        - The resulting table provides a mapping between program external IDs and their corresponding services.
        - The service area describes the area neighbors must be in to receive service from the program.
        - Ensure that the provided DataFrame contains the necessary columns and represents the relevant program data.
        - The resulting DataFrame is sorted based on the `Program External ID` column in ascending order.
        - Table column headers are pulled from `text.json`.
    """
    df = df[['Program External ID', 'Program Service Area']]
    df.columns = TEXT["APPENDIX PROGRAM SERVICE AREAS"]["columns"]
    return df.sort_values(by=TEXT["APPENDIX PROGRAM SERVICE AREAS"]["columns"][0], ascending=True).drop_duplicates().reset_index(drop=True)




# MAIN
if __name__ == "__main__":
    # Define console parser
    parser = argparse.ArgumentParser(description="Analyze bulk upload data")
    # Add file argument
    parser.add_argument("file", action="store", help="The file to validate.")
    # Add silent argument
    parser.add_argument('--silent', action='store', nargs='+', help='Name of functions to not run')
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
        create_recommended_filters_slice,
        create_hour_type_usage_table,
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
        create_profile_completion_tiers_table,
        create_program_category_field_weights,
        create_program_by_program_qualifications_table,
        create_program_by_program_services_table,
        create_program_profile_completion_table
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

    # Execute functions
    [graph(df, directory) for graph in valid_graphing_functions]
    # [print(dataframe(df)) for dataframe in valid_dataframe_functions]

    # Save State
    save_state(TEXT, TEXT_SAVE_NAME.replace('resources/', ''), directory)
    save_state(WEIGHTS, WEIGHTS_SAVE_NAME.replace('resources/', ''), directory)
    save_state(RECOMMENDED_FILTERS, RECOMMENDED_FILTERS_SAVE_NAME.replace('resources/', ''), directory)
    save_state(PROFILE_COMPLETION_TIERS, PROFILE_COMPLETION_TIERS_SAVE_NAME.replace('resources/', ''), directory)
