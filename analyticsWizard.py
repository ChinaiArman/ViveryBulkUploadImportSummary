# Import packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse, os, shutil

# Import local files
import keys




# GRAPHS
def save_graph(file_name: str, directory: str, dpi: int) -> None:
    """
    Saves the active PyPlot with a given file name in a specified directory, with a specified size (dots per square inch).

    :param file_name: A string containing the name for the new image file.
    :param directory: A string with the path to the directory to save the file in.
    :param dpi: An integer representing the DPI to save the image in.
    :return: None.

    :precondition: This function needs a PyPlot to be active.
    :precondition: The directory must be a local path.
    """
    plt.savefig(file_name, dpi=dpi)
    try:
        shutil.move(file_name, directory)
    except:
        os.remove(directory + '\\' + file_name)
        shutil.move(file_name, directory)
    plt.close()
    return


def create_map(df: pd.DataFrame, directory: str) -> None:
    pass


def graph_profile_grade(df: pd.DataFrame, directory: str) -> None:
    pass


def graph_missing_organization_contact_info(df: pd.DataFrame, directory: str) -> None:
    pass


def graph_missing_location_contact_info(df: pd.DataFrame, directory: str) -> None:
    pass


def graph_missing_program_contact_info(df: pd.DataFrame, directory: str) -> None:
    pass


def graph_program_type(df: pd.DataFrame, directory: str) -> None:
    pass


def graph_food_program_breakdown(df: pd.DataFrame, directory: str) -> None:
    pass


def graph_program_filter_usage(df: pd.DataFrame, directory: str) -> None:
    pass


def graph_network_hours_overview(df: pd.DataFrame, directory: str) -> None:
    pass


def graph_sample_location_hours(df: pd.DataFrame, directory: str) -> None:
    pass


def graph_sample_program_hours(df: pd.DataFrame, directory: str) -> None:
    pass


def graph_program_qualifications(df: pd.DataFrame, directory: str) -> None:
    pass


def graph_program_service_areas(df: pd.DataFrame, directory: str) -> None:
    pass




# TABLES
def create_network_overview_table(df: pd.DataFrame) -> pd.DataFrame:
    return


def create_highest_graded_profiles_table(df: pd.DataFrame) -> pd.DataFrame:
    return


def create_lowest_graded_profiles_table(df: pd.DataFrame) -> pd.DataFrame:
    return


def create_recommended_program_filters_table(df: pd.DataFrame) -> pd.DataFrame:
    return


def create_hour_type_usage_table(df: pd.DataFrame) -> pd.DataFrame:
    return


def create_organization_table(df: pd.DataFrame) -> pd.DataFrame:
    return


def create_location_table(df: pd.DataFrame) -> pd.DataFrame:
    return


def create_program_table(df: pd.DataFrame) -> pd.DataFrame:
    return


def create_program_profile_completion_table(df: pd.DataFrame) -> pd.DataFrame:
    return


def create_organization_contact_information_table(df: pd.DataFrame) -> pd.DataFrame:
    return


def create_location_contact_information_table(df: pd.DataFrame) -> pd.DataFrame:
    return


def create_program_contact_information_table(df: pd.DataFrame) -> pd.DataFrame:
    return


def create_program_by_program_type_table(df: pd.DataFrame) -> pd.DataFrame:
    return


def create_program_by_program_audience_table(df: pd.DataFrame) -> pd.DataFrame:
    return


def create_program_by_program_languages_spoken_table(df: pd.DataFrame) -> pd.DataFrame:
    return


def create_program_by_program_features_table(df: pd.DataFrame) -> pd.DataFrame:
    return


def create_program_by_program_items_offered_table(df: pd.DataFrame) -> pd.DataFrame:
    return


def create_program_by_program_dietary_options_table(df: pd.DataFrame) -> pd.DataFrame:
    return


def create_location_hours_table(df: pd.DataFrame) -> pd.DataFrame:
    return


def create_program_hours_table(df: pd.DataFrame) -> pd.DataFrame:
    return


def create_program_by_program_qualifications_table(df: pd.DataFrame) -> pd.DataFrame:
    return


def create_program_by_program_services_table(df: pd.DataFrame) -> pd.DataFrame:
    return




# SUMMATIONS
def count_organizations(df: pd.DataFrame) -> int:
    """
    Counts the number of unique organizations in a DataFrame.

    :param df: A Pandas DataFrame
    :return: The number of unique organizations, represented as an integer.

    :precondition: The Pandas DataFrame must contain the column 'Organization External ID'.

    :note: Unique organizations are determined by the 'Organization External ID' column.
    """
    return df['Organization External ID'].nunique()


def count_valid_organizations(df: pd.DataFrame) -> int:
    """
    Counts the number of unique organizations that are both active and approved.

    :param df: A Pandas DataFrame
    :return: The number of unique organizations that are both approved and active, represented as an integer. 

    :precondition: The Pandas DataFrame must contain the columns 'Organization External ID', 'Organization Active Status', and 'Organization Approved Status'.

    :note: Active and Approved organizations are determined by the 'Organization Active Status' and 'Organization Approved Status' columns.
    :note: Unique organizations are determined by the 'Organization External ID' column.
    """
    df = df[(df['Organization Active Status'] == True) & (df['Organization Approval Status'] == True)]
    return df['Organization External ID'].nunique()


def count_locations(df: pd.DataFrame) -> int:
    """
    Counts the number of unique locations in a DataFrame.

    :param df: A Pandas DataFrame
    :return: The number of unique locations, represented as an integer.

    :precondition: The Pandas DataFrame must contain the column 'Location External ID'.

    :note: Unique locations are determined by the 'Location External ID' column.
    """
    return df['Location External ID'].nunique()


def count_valid_locations(df: pd.DataFrame) -> int:
    """
    Counts the number of unique locations that are both active and approved.

    :param df: A Pandas DataFrame
    :return: The number of unique locations that are both approved and active, represented as an integer. 

    :precondition: The Pandas DataFrame must contain the columns 'Location External ID', 'Location Active Status', and 'Location Approved Status'.

    :note: Active and Approved locations are determined by the 'Location Active Status' and 'Location Approved Status' columns.
    :note: Unique locations are determined by the 'Location External ID' column.
    """
    df = df[(df['Location Active Status'] == True) & (df['Location Approval Status'] == True)]
    return df['Location External ID'].nunique()


def count_programs(df: pd.DataFrame) -> int:
    """
    Counts the number of unique programs in a DataFrame.

    :param df: A Pandas DataFrame
    :return: The number of unique programs, represented as an integer.

    :precondition: The Pandas DataFrame must contain the column 'Program External ID'.

    :note: Unique programs are determined by the 'Program External ID' column.
    """
    return df['Program External ID'].nunique()


def count_valid_programs(df: pd.DataFrame) -> int:
    """
    Counts the number of unique programs that are both active and approved.

    :param df: A Pandas DataFrame
    :return: The number of unique programs that are both approved and active, represented as an integer. 

    :precondition: The Pandas DataFrame must contain the columns 'Program External ID', 'Program Active Status', and 'Program Approved Status'.

    :note: Active and Approved programs are determined by the 'Program Active Status' and 'Program Approved Status' columns.
    :note: Unique programs are determined by the 'Program External ID' column.
    """
    df = df[(df['Program Active Status'] == True) & (df['Program Approval Status'] == True)]
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
    # Create a list of visualization functions
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
    # Create a list of text functions
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

    # Create valid visualizations functions
    valid_graphing_functions = [graph for graph in graphing_functions if graph.__name__ not in silenced_functions]
    # Create valid text functions
    valid_summation_functions = [summation for summation in summation_functions if summation.__name__ not in silenced_functions]
    # Create valid DataFrame functions
    valid_dataframe_functions = [dataframe for dataframe in dataframe_functions if dataframe.__name__ not in silenced_functions]
    # Execute functions
    [graph(df, directory) for graph in valid_graphing_functions]
    [print(dataframe.__name__ + ": " + dataframe(df)) for dataframe in valid_dataframe_functions]
    [print(summation.__name__ + ": " + str(summation(df))) for summation in valid_summation_functions]
