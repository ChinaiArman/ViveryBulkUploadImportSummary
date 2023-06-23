"""
"""


# PACKAGE IMPORTS
import pandas as pd                 # Pandas, used to represent CSVs and large data sets as a DataFrame.
import numpy as np                  # NumPy, adds Arrays to python and enables large arithmatic operations.
import matplotlib.pyplot as plt     # MatPlotLib's PyPlot, used to graph data sets and create data visualizations.
import argparse, os, shutil         # Argparse, OS, and Shutil, used for File Manipulation and the Command Line Interface
import json                         # JSON, used to parse JSON files and convert to Dictionary data types.

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




# GRAPHS
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
    Creates a network overview table based on the provided DataFrame.

    Args:
        `df` (pd.DataFrame): The Pandas DataFrame containing the network data.

    Returns:
        `pd.DataFrame`: A DataFrame containing the network overview information.

    Preconditions:
        - The Pandas DataFrame must contain the columns:
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
              Level  Active  Inactive  Total
        0  Organizations       2         1      3
        1      Locations       3         2      3
        2       Programs       2         1      3

    Additional Information:
        - The network overview table provides a summary of active, inactive, and total counts
          for organizations, locations, and programs.
        - An active organization, location, or program is determined by the `Organization Active Status`,
          `Location Active Status`, or `Program Active Status` columns, respectively.
        - An approved organization, location, or program is determined by the `Organization Approval Status`,
          `Location Approval Status`, or `Program Approval Status` columns, respectively.
        - The count of unique entities is based on their respective external ID columns.
    """
    level = ['Organizations', 'Locations', 'Programs']
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
        'Level': level,
        'Active': active,
        'Inactive': inactive,
        'Total': total
        }
    return pd.DataFrame(data)


def create_highest_graded_profiles_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a table of the highest graded program profiles based on the provided DataFrame.

    Args:
        `df` (pd.DataFrame): The Pandas DataFrame containing the data.

    Returns:
        `pd.DataFrame`: A DataFrame containing the highest graded program profiles.

    Preconditions:
        - The Pandas DataFrame must contain the necessary columns to calculate program profile completion, as required by the `create_program_profile_completion_table` function.
        - Weights.py file must be present in the working directory to access the completion weight for each column.

    Raises:
        None.

    Example:
        >>> data = pd.DataFrame({'Location External ID': ['L1', 'L2', 'L3'],
        ...                     'Location Name': [None, None, 'Good Food'],
        ...                     'Location ZIP': [715359, None, 136135],
        ...                     'Hours Entity Type': ['Program', 'Location', 'Location']})
        >>> create_program_profile_completion_table(data)
          Location External ID  Profile Score
        0                   L3              8
        1                   L1              5
        2                   L2              5

    Additional Information:
        - The function calls the `create_program_profile_completion_table` function to create a table of program profile completion based on the provided DataFrame.
        - It then sorts the resulting table in descending order of the profile scores.
        - The table displays the top 5 highest graded program profiles based on the 'Profile Score' column.
        - The profile completion grades model after the internal scores Vivery uses to measure profile completeness.
        - Ensure that the provided DataFrame contains the necessary columns and represents the relevant data to calculate program profile completion.
        - For an accurate calculation, ensure all columns are present in the DataFrame. 
    """ 
    return create_program_profile_completion_table(df).sort_values(by='Profile Score', ascending=False).head(5)


def create_lowest_graded_profiles_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a table of the lowest graded program profiles based on the provided DataFrame.

    Args:
        `df` (pd.DataFrame): The Pandas DataFrame containing the data.

    Returns:
        `pd.DataFrame`: A DataFrame containing the lowest graded program profiles.

    Preconditions:
        - The Pandas DataFrame must contain the necessary columns to calculate program profile completion, as required by the `create_program_profile_completion_table` function.
        - Weights.py file must be present in the working directory to access the completion weight for each column.

    Raises:
        None.

    Example:
        >>> data = pd.DataFrame({'Location External ID': ['L1', 'L2', 'L3'],
        ...                     'Location Name': [None, None, 'Good Food'],
        ...                     'Location ZIP': [715359, None, 136135],
        ...                     'Hours Entity Type': ['Program', 'Location', 'Location']})
        >>> create_program_profile_completion_table(data)
          Location External ID  Profile Score
        0                   L1              5
        1                   L2              5
        2                   L3              8

    Additional Information:
        - The function calls the `create_program_profile_completion_table` function to create a table of program profile completion based on the provided DataFrame.
        - It then sorts the resulting table in descending order of the profile scores.
        - The table displays the 5 lowest graded program profiles based on the 'Profile Score' column.
        - The profile completion grades model after the internal scores Vivery uses to measure profile completeness.
        - Ensure that the provided DataFrame contains the necessary columns and represents the relevant data to calculate program profile completion.
        - For an accurate calculation, ensure all columns are present in the DataFrame. 
    """
    return create_program_profile_completion_table(df).sort_values(by='Profile Score', ascending=True).head(5) 


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
            Program Audience            Location Features            Program Features           Items Offered           Dietary Options
        0       Seniors                     Safe Space                  Reservations                Dairy                   Gluten Free
        1       Immigrants                  Wi-Fi Available             Indoor Service              Eggs                    Vegan
        2       Youth                                                   Prepared Food               Meat                    Vegetarian

    Additional Information:
        - The function reads the `recommended_filters.csv` file from the `resources` directory to create the table.
        - The table includes filter categories and their corresponding filter names.
        - The placeholder argument `_` is ignored and not used in the function.
    """
    return RECOMMENDED_FILTERS


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
            Hour Type   Location Usage  Program Usage
        0   'Weekly'                     1              1
        1   'Every Other Week'           1              1
        2   'Week of Month'              1              1
        3   'Day of Month'               1              1

    Additional Information:
        - The function calculates the usage of hour types based on the `Hours Entity Type` and `Frequency` columns in the DataFrame.
        - The table displays the count of unique `Location External ID` and `Program External ID` for each hour type frequency.
        - The hour type frequencies are `Weekly`, `Every Other Week`, `Week of Month`, and `Day of Month`.
        - Ensure that the provided DataFrame contains the necessary columns and represents the relevant data.
    """
    hour_type = ['Weekly', 'Every Other Week', 'Week of Month', 'Day of Month']
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
        'Hour Type': hour_type,
        'Location Usage': locations,
        'Program Usage': programs,
    }
    return pd.DataFrame(data)


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
           Organization External ID Organization Name Organization Address 1
        0                        O1              Org1               Address1
        1                        O2              Org2               Address2
        2                        O3              Org3               Address3

    Additional Information:
        - The function extracts specific columns related to organizations from the input DataFrame.
        - The selected columns include:
            - `Organization External ID`: Represents the unique ID of the organization.
            - `Organization Name`: Represents the name of the organization.
            - `Organization Address 1`: Represents the first line of the organization's address.
        - The function creates a new DataFrame containing only the selected columns.
        - Ensure that the input DataFrame `df` represents the relevant data and contains the necessary columns.
    """
    return df[['Organization External ID', 'Organization Name', 'Organization Address 1']].drop_duplicates()


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
          Location External ID Location Name Location Address 1
        0                   L1    Location 1           Address 1
        1                   L2    Location 2           Address 2
        2                   L3    Location 3           Address 3

    Additional Information:
        - The function extracts the specified columns from the provided DataFrame to create a location table.
        - The columns `Location External ID`, `Location Name`, and `Location Address 1` are required to be present in the DataFrame.
        - The table displays the `Location External ID`, `Name`, and `Address` for each location.
        - Ensure that the provided DataFrame contains the necessary columns and represents the relevant location data.
    """
    return df[['Location External ID', 'Location Name', 'Location Address 1']].drop_duplicates()


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
          Program External ID Program Name
        0                  P1   Program 1
        1                  P2   Program 2
        2                  P3   Program 3

    Additional Information:
        - The function extracts the specified columns from the provided DataFrame to create a program table.
        - The columns `Program External ID` and `Program Name` are required to be present in the DataFrame.
        - The table displays the `Program External ID` and name for each program.
        - Ensure that the provided DataFrame contains the necessary columns and represents the relevant program data.
    """
    return df[['Program External ID', 'Program Name']].drop_duplicates()


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
            Tier            Min     Max
        0   Basic            0      20
        1   Quality         21      35
        2   Exceptional     36

    Additional Information:
        - The function returns a predefined table of profile completion tiers.
        - The tiers are categorized based on the score range.
        - The table contains three columns: `Tier`, `Min`, `Max`.
        - Each row represents a profile completion tier with its corresponding score range.
        - The tiers are defined as `Basic`, `Quality`, and `Exceptional`.
        - This function does not require any input data or parameters.
        - The `PROFILE_COMPLETION_TIERS` variable is a global variable that should be defined in the code
          and should contain the path to the `profile_completion_tiers.csv` file.
    """
    return PROFILE_COMPLETION_TIERS


def create_program_category_field_weights(_: any) -> pd.DataFrame:
    """
    Creates a table of program category field weights.

    Args:
        `_` (any): This parameter is not used and can be ignored.

    Returns:
        `pd.DataFrame`: A DataFrame containing the program category field weights.

    Preconditions:
        - The global variable `WEIGHTS` must be defined and contain the field weights.
        - `weights.json` file must be present in the working directory's `resource` folder to access the completion weight for each column.

    Raises:
        None.

    Example:
        >>> create_program_category_field_weights(None)
                        Columns         Weight
        0   Program Contact Phone            1
        1   Program Contact Phone Ext        0
        2   Program Contact Email            1

    Additional Information:
        - The function returns a table of program category field weights.
        - The field weights are defined in the global variable `WEIGHTS`.
        - The table contains two columns: `Columns` and `Weight`.
        - Each row represents a program category field with its corresponding weight.
        - The `WEIGHTS` variable is a global variable that should be defined in the code from the `weights.json` file stored in the `resources` folder.
        - This function does not require any input data or parameters.
    """
    df = pd.DataFrame.from_dict(WEIGHTS, orient='index')
    return df.reset_index().rename(columns={'index': 'Columns',
                                            0: 'Weight'})


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
          Location External ID  Profile Score
        0                   L1              5
        1                   L2              5
        2                   L3              8

    Additional Information:
        - The function calculates the program profile completion score based on the provided DataFrame.
        - The function checks for if a value is present in each cell, replacing present values with 1 and absent values with zeo.
        - The function then multiplies the integers by the grade key, and sums the value in each row to calculate the profiles completeness.
        - The grade key is stored in `resources/weights.json`, which the function uses to determine the weightage for each column.
        - The table displays the maximum profile score for each location based on the `Location External ID`.
        - The profile completion grades model after the internal scores Vivery uses to measure profile completeness.
        - For an accurate calculation, ensure all columns are present in the DataFrame. 
    """
    df2 = df.copy()
    df2["Profile Score"] = df2.notnull().astype('int').mul(WEIGHTS).sum(axis=1)
    return df2[["Location External ID", "Profile Score"]].groupby(['Location External ID']).max().reset_index()


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
          Organization External ID Organization Contact Name Organization Contact Email Organization Contact Phone
        0                      O1                 John Doe          john@example.com                  123456789
        1                      O2              Jane Smith          jane@example.com                  987654321
        2                      O3            Adam Johnson          adam@example.com                  555555555

    Additional Information:
        - The function extracts the organization contact information from the provided DataFrame.
        - The table includes the columns: `Organization External ID`, `Organization Contact Name`,
          `Organization Contact Email`, and `Organization Contact Phone`.
        - Ensure that the provided DataFrame contains the necessary columns and represents the relevant data.
    """
    return df[['Organization External ID', 'Organization Contact Name', 'Organization Contact Email', 'Organization Contact Phone']].drop_duplicates()


def create_location_contact_information_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    """
    return df[['Location External ID', 'Location Contact Name', 'Location Contact Email', 'Location Contact Phone', 'Location Website']].drop_duplicates()


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
          Program External ID Program Contact Name Program Contact Email Program Contact Phone
        0                  P1            Sarah Johnson    sarah@example.com            999888777
        1                  P2           Jane Smith       jane@example.com            987654321
        2                  P3            Emma Thompson    emma@example.com            555555555

    Additional Information:
        - The function extracts the program contact information from the provided DataFrame.
        - If the `Program Use Same Contact As Location` flag is set to True, the function retrieves the contact
          information from the corresponding location columns instead of the program columns.
        - The table includes the columns: `Program External ID`, `Program Contact Name`, `Program Contact Email`,
          and `Program Contact Phone`.
        - Ensure that the provided DataFrame contains the necessary columns and represents the relevant data.
    """
    program_contact_info = df[['Program External ID', 'Program Contact Name', 'Program Contact Email', 'Program Contact Phone']]
    location_contact_info = df[['Location External ID', 'Location Contact Name', 'Location Contact Email', 'Location Contact Phone']]
    program_contact_info.loc[df['Program Use Same Contact As Location'] == True] = location_contact_info.loc[df['Program Use Same Contact As Location'] == True]
    return program_contact_info.drop_duplicates()
    

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
          Program External ID           Program Type                    Type Specification
        0                  P1           Food Program                    Food Distribution
        1                  P2           Case Management Services        Hot/Cold Meal Program
        2                  P3           Housing Assistance              Other

    Additional Information:
        - The function groups programs based on their program type, represented by the 'Program Service Category'
          column, and their type specification, represented by the 'Food Program Category' column.
        - The resulting table includes the columns 'Program External ID', 'Program Type', and 'Type Specification'.
        - The function removes any duplicate rows in the resulting table.
        - Ensure that the provided DataFrame contains the necessary columns and represents the relevant data.
    """
    return df[['Program External ID', 'Program Service Category', 'Food Program Category']].drop_duplicates().rename(columns={'Program External ID': 'Program External ID',
                                                                                                                              'Program Service Category': 'Program Type',
                                                                                                                              'Food Program Category': 'Type Specification'})


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
    # Create a list of summation functions
    summation_functions = [

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
    [print(dataframe(df)) for dataframe in valid_dataframe_functions]
    [print(summation.__name__ + ": " + str(summation(df))) for summation in valid_summation_functions]

    # Save State
    save_state(TEXT, TEXT_SAVE_NAME.replace('resources/', ''), directory)
    save_state(WEIGHTS, WEIGHTS_SAVE_NAME.replace('resources/', ''), directory)
    save_state(RECOMMENDED_FILTERS, RECOMMENDED_FILTERS_SAVE_NAME.replace('resources/', ''), directory)
    save_state(PROFILE_COMPLETION_TIERS, PROFILE_COMPLETION_TIERS_SAVE_NAME.replace('resources/', ''), directory)
