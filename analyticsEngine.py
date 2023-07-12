"""
Analytics Engine API.

@author Arman Chinai
@version 1.1.0

The primary purpose of this file is to serve as an API for the pdfWizard, assisting in creating the analytical report (PDF).
This file provides a full range of functions used to perform data analytics on a network bulk upload file.
The file outputs various graphs (PNGs) and dataframes (CSVs) when provided with a CSV.
The output is stored in a dedicated folder created by the scripts.

---> OPERATIONAL INSTRUCTIONS <---

Package Imports:
    * Pandas                            * Graph Objects (Plotly)                * ArgParse                          * PIL (Image)
    * NumPy                             * JSON                                  * OS                                * DateTime
    * PyPlot (MatPlotLib)               * Math                                  * Shutil                            * Calendar

API Keys: (stored in keys.py)
    * MapBoxAPI Secret Key: https://docs.mapbox.com/help/getting-started/access-tokens/
    * MapBoxAPI Public Key: https://docs.mapbox.com/help/getting-started/access-tokens/

Fonts:
    * Roobert Font Suite (found in Resources)

Instructions:
    1) Package Imports:
        a) Create a new terminal
        b) Run `pip install -r requirements.txt`
    2) API Keys:
        a) Visit `https://docs.mapbox.com/help/getting-started/access-tokens/`
        b) Complete steps to acquire API Keys
        c) Create a file `keys.py`
        d) Define two variables (SK, PK) and assign the appropriate key values
    3) Fonts (Windows OS):
        a) From root directory: `'resources' > 'Roobert Font Suite' > 'TTF'`
        b) Open all TTF files and click `Install`
        c) From the Windows folder: `Fonts`
        d) Clear MatPlotLib font cache by deleting the cache file (fontlist.json, likely stored in `Users/{user}/.matplotlib`)
    4) Add a bulk upload file to the working directory
    5) Run the following command: `python analyticsEngine.py "{path to file from root directory}"`
    -----
    6) POTENTIAL FONT ERROR: `findfont: Font family `Roobert Medium` not found`.
        a) Navigate to the MatPlotLib font cache file (fontlist.json, likely stored in `Users/{user}/.matplotlib`)
        b) Open the file in an IDE (VSCode)
        c) Use `ctrl + F` and search `Roobert`
        d) For each value of `Roobert` under the `name` key, change the name to match the specific font (found at the end of the string under the `fname` key)
            - Example:
                BEFORE:
                    {
                    "fname": "C:\\Users\\arman\\AppData\\Local\\Microsoft\\Windows\\Fonts\\Roobert-Medium.ttf",
                    "name": "Roobert",
                    "style": "normal",
                    "variant": "normal",
                    "weight": 500,
                    "stretch": "normal",
                    "size": "scalable",
                    "__class__": "FontEntry"
                    },
                AFTER:
                    {
                    "fname": "C:\\Users\\arman\\AppData\\Local\\Microsoft\\Windows\\Fonts\\Roobert-Medium.ttf",
                    "name": "Roobert Medium",
                    "style": "normal",
                    "variant": "normal",
                    "weight": 500,
                    "stretch": "normal",
                    "size": "scalable",
                    "__class__": "FontEntry"
                    },

Desired Output:
    * A folder will be created with the name `data_{bulk upload file name}`, containing the directories `csvs`, `images`, and `resources`, as well as the bulk upload file.
    * Within `csvs`, a copy of all dataframes generated will be stored in CSV format.
    * Within `images`, a copy of all graphs generated will be stored in PNG format.
    * Within `resources`, a copy of all generation data will be stored in CSV/JSON format.

Still have questions? Send an email to `arman@vivery.org` with the subject line `Analytics Engine API - {question}`. 
"""


# PACKAGE IMPORTS
import pandas as pd                     # Pandas, used to represent CSVs and large data sets as a DataFrame.
import numpy as np                      # NumPy, adds Arrays to python and enables large arithmatic operations.
import matplotlib.pyplot as plt         # MatPlotLib's PyPlot, used to graph data sets and create data visualizations.
import argparse, os, shutil             # Argparse, OS, and Shutil, used for File Manipulation and the Command Line Interface
import plotly.graph_objects as go       # Plotly, used to create the map object using the MapBox API.
import json                             # JSON, used to parse JSON files and convert to Dictionary data types.
import math                             # Math, used for basic mathematical operations.
from PIL import Image                   # Image, used to handle varius tasks with Image files like PNGs.
import datetime                         # Datetime, used to handle date related tasks and allows python to have access to real world calendar data.
import calendar                         # Calendar, used to match dates to their months and days using real world calendar data.
import glob                             # Glob, used for grouping files together and working with OS storing system.
import os                               # OS, used to navigate the OS for file storage and manipulation.

# LOCAL FILE IMPORTS


# IMPORT CONSTANTS
from keys import PK, SK                                                                                         # PK and SK, used for the MapBoxAPI; stored in the API Key File 'keys'.
TEXT_SAVE_NAME = "resources/text.json"                                                                          # Path to TEXT save file (JSON).
with open(TEXT_SAVE_NAME) as file: TEXT = json.load(file)                                                       # TEXT, used for all of the text in the PDF report; stored in the file, 'resources/text.json'.
WEIGHTS_SAVE_NAME = "resources/weights.json"                                                                    # Path to WEIGHTS save file (JSON).
with open(WEIGHTS_SAVE_NAME) as file: WEIGHTS = json.load(file)                                                 # WEIGHTS, used for the weightage of each column in the profile completion grades; stored in the file, 'resources/weights.json'.
RECOMMENDED_FILTERS_SAVE_NAME = 'resources/recommended_filters.csv'                                             # Path to Recommended Filters (CSV).
RECOMMENDED_FILTERS = pd.read_csv(RECOMMENDED_FILTERS_SAVE_NAME)                                                # RECOMMENDED_FILTERS, used to store the recommended filters for locations and programs, stored in the file, 'resources/recommended_filters.csv'
PROFILE_COMPLETION_TIERS_SAVE_NAME = 'resources/profile_completion_tiers.csv'                                   # Path to Profile Completion Tiers (CSV).
PROFILE_COMPLETION_TIERS = pd.read_csv(PROFILE_COMPLETION_TIERS_SAVE_NAME)                                      # PROFILE_COMPLETION_TIERS, used to store the profile completion tiers for locations, stored in the file, 'resources/profile_completion_tiers.csv'

# MISC CONSTANTS
MAP_SCOPE_KEY = {0: 12, 0.1: 10, 0.2: 9, 0.4: 8, 0.9: 7, 1.5: 6, 3.5: 5, 7: 4, 25: 3, 32: 2, 70: 1}             # A dictionary, used to map the difference between the max/min lon/lat values to map scopes.

# COLOURS
VIVERY_GREEN = '#00483D'                                                                                        # A colour in the Vivery colour scheme.
VIRIDIAN = '#5F9575'                                                                                            # A colour in the Vivery colour scheme.
SAGE = '#A2C3A8'                                                                                                # A colour in the Vivery colour scheme.
SALMON = '#D4A392'                                                                                              # A colour in the Vivery colour scheme.
WARM_WHITE = '#FAF9F6'                                                                                          # A colour in the Vivery colour scheme.
NEON_LIME = '#BBD98D'                                                                                           # A colour in the Vivery colour scheme.
NEON_BLUE = '#8CCFB6'                                                                                           # A colour in the Vivery colour scheme.

# STYLES
AXES_LABEL_FONT_DICT = {'family': 'Roobert Medium', 'color':  VIVERY_GREEN, 'weight': 'bold', 'size': 16}       # A Dictionary used to style the pyplot axes text.
PIE_SLICE_FONT_DICT = {'family': 'Roobert Medium', 'color':  VIVERY_GREEN, 'weight': 'bold', 'size': 16}        # A Dictionary used to style the pyplot axes text.




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
    plt.savefig(file_name, dpi=dpi, bbox_inches='tight')
    try:
        shutil.move(file_name, directory + "/images")
    except OSError:
        os.remove(directory + "/images"+ '/' + file_name)
        shutil.move(file_name, directory + "/images")
    plt.close()
    return directory + "/images/" + file_name


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


def map_scope(value: int) -> None:
    """
    Maps the difference between the maximum and minimum lat/lon value to a corresponding map scope.

    Args:
        `value` (int): The integer value to be mapped to a scope.

    Returns:
        `None`.

    Preconditions:
        None.

    Raises:
        None.

    Example:
        >>> value = 40
        >>> scope = map_scope(value)
        >>> print(f"The scope for value {value} is {scope}")
        The scope for value 40 is 4


    Additional Information:
        - The function maps an input integer value to a specific scope.
        - The function uses a dictionary to map ranges to their corresponding scopes.
        - The keys in the dictionary represent the upper bounds of the ranges.
        - The values in the dictionary represent the corresponding scopes.
        - The function iterates through the dictionary and returns the first matching scope based on the value else returns 12.
        - Ensure that the input value is an integer.
    """
    for range_end, scope in MAP_SCOPE_KEY.items():
        if range_end >= value:
            return scope
    print('one')
    return 0


def crop_image(width: int, height: int, filename: str, directory: str) -> None:
    """
    Crops an image to a specified width and height.

    Args:
        `width` (int): The desired width of the cropped image.
        `height` (int): The desired height of the cropped image.
        `filename` (str): The name of the image file to be cropped.
        `directory` (str): The directory where the image file is located.

    Returns:
        `None`

    Preconditions:
        - The image file specified by `filename` must exist in the given `directory`.
        - The `width` and `height` values must be positive integers.

    Raises:
        FileNotFoundError: If the specified image file does not exist in the given directory.

    Example:
        >>> crop_image(200, 150, "image.jpg", "/path/to/images")
        # The image.jpg file in the /path/to/images directory will be cropped to a width of 200 and height of 150.

    Additional Information:
        - The `crop_image` function uses the Python Imaging Library (PIL) to open the specified image file.
        - The function crops the image using the coordinates (height/2, width/2, height/2 + width, width/2 + height).
        - The resulting cropped image is saved as a PNG file in the same directory with the same filename, overwriting the original file.
        - Ensure that the image file exists in the specified directory, the dimensions are positive integers, and the dimensions are valid for cropping.
    """
    try:
        im = Image.open(directory + "/images/" + filename)
    except FileNotFoundError:
        raise FileNotFoundError(f"The image file '{filename}' does not exist in the directory '{directory}'/images.")
    im = im.crop((height/2, width/2, height/2 + width, width/2 + height))
    im.save(directory + "/images/" + filename, "png")
    return directory + "/images/" + filename


def plot_bar_graph(x_axis: list, y_axis: list, text_section: str, barcolor: str, xlabel="xlabel", ylabel="ylabel", rotation=0) -> None:
    """
    Plots a bar graph based on the provided data.

    Args:
        `x_axis` (list): The values for the x-axis.
        `y_axis` (list): The values for the y-axis.
        `text_section` (str): The key of the text section in the `TEXT` dictionary for labeling.
        `barcolor` (str): The color of the bars.
        `xlabel` (str) [kwargg]: A keyword argument used to find the X Axis Label in the `TEXT` dictionary.
        `ylabel` (str) [kwargg]: A keyword argument used to find the Y Axis Label in the `TEXT` dictionary.
        `rotation` (int) [kwargg]: A keyword argument used to rotate the x-axis tickmarks.

    Returns:
        `None`

    Preconditions:
        - The lengths of `x_axis` and `y_axis` must be the same.
        - `text_section` must be a valid key in the `TEXT` dictionary.
        - `barcolor` must be a valid color string.

    Raises:
        None

    Example:
        >>> plot_bar_graph([1, 2, 3, 4], [10, 20, 30, 40], "bar_graph_section", VIVERY_GREEN)
        # Plots a bar graph with x-axis values [1, 2, 3, 4], y-axis values [10, 20, 30, 40],
        # using the text section "bar_graph_section" for labeling, and blue color for the bars.

    Additional Information:
        - The function creates a bar graph using the provided x-axis and y-axis values.
        - The width of the bars is set to 0.5.
        - The x-axis ticks are customized with the font `Roobert Medium`, fontsize 10, and color `VIVERY_GREEN`.
        - The y-axis ticks are customized with the font `Roobert Medium`, fontsize 10, and color `VIVERY_GREEN`.
        - If the maximum value in the y-axis data is less than or equal to 10, the y-axis ticks are set to a range based on the minimum and maximum values.
        - Y-dash lines are added at each y-axis tick except the first one.
        - The top, right, and left spines of the plot are removed.
        - The x-axis label is set using the specified `text_section` key and the `AXES_LABEL_FONT_DICT` font settings.
        - The y-axis label is set using the specified `text_section` key and the `AXES_LABEL_FONT_DICT` font settings.
        - No box or frame is drawn around the plot.

    Note:
        - Ensure that the lengths of `x_axis` and `y_axis` are the same, and the `text_section` key and `barcolor` are valid.
    """
    # Create Graph
    fig, ax = plt.subplots()
    ax.bar(x_axis, y_axis, width=0.5, color=barcolor, zorder=2)

    # X-Ticks
    plt.xticks(font="Roobert Medium", fontsize=11, color=VIVERY_GREEN, rotation=rotation)

    # Y-Ticks
    if max(y_axis) <= 10:
        plt.yticks(range(math.floor(min(y_axis)), math.ceil(max(y_axis))+1))
    plt.yticks(font="Roobert Medium", fontsize=11, color=VIVERY_GREEN)
    ax.tick_params(axis=u'both', which=u'both',length=0)

    # Y-Dash Lines
    for tick in plt.yticks()[0][1:]:
        ax.axhline(y=tick, color='grey', linewidth=0.3, zorder=1)
    
    # Remove Box
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Axis Labels
    if TEXT[text_section][xlabel] != "":
        plt.xlabel(TEXT[text_section][xlabel], fontdict=AXES_LABEL_FONT_DICT, labelpad=10)
    plt.ylabel(TEXT[text_section][ylabel], fontdict=AXES_LABEL_FONT_DICT, labelpad=10)
    return


def plot_pie_graph(sizes: list, colours: list, text_section: str, labels="labels") -> None:
    """
    Generates a pie chart to visualize data.

    Args:
        `sizes` (list): A list of values representing the sizes of each pie slice.
        `colours` (list): A list of colours to be applied to each pie slice.
        `text_section` (str): The key for the text section in the TEXT dictionary containing labels.
        `labels` (str) [kwargg]: The key for the labels in the TEXT[text_section].

    Preconditions:
        - The length of `sizes` and `colours` should be the same.
        - `text_section` and `labels` must correspond to valid keys in the TEXT dictionary.

    Raises:
        None

    Example:
        >>> plot_pie_graph([10, 20, 30], ['red', 'blue', 'green'], `DATA_SECTION`, `label_key`)
        # Generates a pie chart with slices corresponding to the values [10, 20, 30].
        # The colours 'red', 'blue', and 'green' are applied to the slices.
        # The labels for the pie slices are retrieved from the `label_key` in the `DATA_SECTION` of the TEXT dictionary.

    Additional Information:
        - The function creates a figure and axis objects using `plt.subplots()`.
        - The pie slices are created using `ax.pie()` with the provided sizes, labels, colours, start angle, percentage format, and text properties.
        - A donut hole is created using `plt.Circle()` and added to the graph.
        - The percentage values on the pie chart are styled using `plt.setp()` to set the color and fontsize.
        - The box surrounding the graph is removed by hiding the spines.
        - The labels are matched with their corresponding patch colors by setting the text color to the patch face color.
    """
    # Remove elements of size 0
    indexes = [i for i in range(len(sizes)) if sizes[i] == 0]
    indexes = sorted(indexes, reverse=True)
    for index in indexes:
        del sizes[index], colours[index], TEXT[text_section][labels][index]

    # Create Graph
    fig, ax = plt.subplots()
    patches, texts, percents = ax.pie(x=sizes, labels=TEXT[text_section][labels], colors=colours, startangle=90, autopct='%1.2f%%', pctdistance=0.80, explode=[0.05] * len(sizes), textprops=PIE_SLICE_FONT_DICT)

    # Create Donut Hole
    hole = plt.Circle((0, 0), 0.5, facecolor='white')
    plt.gcf().gca().add_artist(hole)

    # Percentage Styling
    plt.setp(percents, color=WARM_WHITE, fontsize=11)

    # Remove Box
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    # Labels
    for i, patch in enumerate(patches):
        texts[i].set_color(patch.get_facecolor())
    return




# GRAPHS
def create_map(df: pd.DataFrame, directory: str) -> str:
    """
    Creates a map visualization based on the provided DataFrame.

    Args:
        `df` (pd.DataFrame): The Pandas DataFrame containing the map data.
        `directory` (str): The directory where the map image will be saved.

    Returns:
        `str`: A string containing the path to the graph, saved as a png, from the root directory. 

    Preconditions:
        - The Pandas DataFrame must contain the required columns: `Location Latitude`, `Location Longitude`, `Organization Approval Status`,
          `Organization Active Status`, `Location Active Status`, and `Location Approval Status`.
        - The `Location Latitude` and `Location Longitude` columns must contain valid latitude and longitude values.
        - The `Organization Approval Status`, `Organization Active Status`, `Location Approval Status`, and `Location Active Status` columns
          must contain boolean values.

    Raises:
        None

    Example:
        >>> create_map(data, "/path/to/maps")
        # Creates a map visualization based on the provided DataFrame and saves the map image in the /path/to/maps directory.

    Additional Information:
        - The function creates a scattermapbox plot using the latitude and longitude coordinates from the DataFrame.
        - The marker color is determined based on the conditions specified using the Organization and Location statuses.
        - The resulting map is centered based on the average latitude and longitude values.
        - The zoom level is determined dynamically based on the range of latitude and longitude values in the DataFrame.
        - The generated map image is saved as a PNG file in the specified directory.
        - The function uses the `crop_image` function to crop the map image to a specific width and height (624x403).
        - Ensure that the DataFrame contains the required columns and represents the relevant map data, and the directory is valid.
    """
    df2 = df.copy()
    df2 = df2[['Location Latitude', 'Location Longitude', 'Organization Approval Status', 'Organization Active Status', 'Location Active Status', 'Location Approval Status']]
    df2['Color'] = np.where((df['Organization Approval Status'] == True) & (df['Organization Active Status'] == True) & (df['Location Approval Status'] == True) & (df['Location Active Status'] == True), VIRIDIAN, SALMON)

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
            zoom=min(map_scope((df2['Location Longitude'].max() - df2['Location Longitude'].min())), map_scope((df2['Location Latitude'].max() - df2['Location Latitude'].min())))
        ),
    )
    fig.write_image(directory + "/images" + '/map.png', width=1000, height=1000)
    return crop_image(624, 403, "map.png", directory)


def graph_profile_grade(df: pd.DataFrame, directory: str) -> str:
    """
    Generates a bar graph to visualize the profile completion grade based on the provided DataFrame.

    Args:
        `df` (pd.DataFrame): The Pandas DataFrame containing the profile completion data.
        `directory` (str): The directory where the generated graph will be saved.

    Returns:
        `str`: A string containing the path to the graph, saved as a png, from the root directory. 

    Preconditions:
        - The Pandas DataFrame `df` must contain the necessary columns and represent the relevant profile completion data.
        - `directory` must be a valid directory path.

    Raises:
        None

    Example:
        >>> graph_profile_grade(data, "/path/to/directory")
        # Generates a bar graph based on the profile completion data in the DataFrame `data`,
        # and saves the graph in the specified directory.

    Notes:
        - Ensure that the DataFrame `df` contains the necessary columns and represents the relevant profile completion data.
        - Provide a valid directory path in `directory` to save the generated graph.

    Additional Information:
        - The function first creates a program profile completion table based on the provided DataFrame using the `create_program_profile_completion_table` function.
        - The x-axis values for the bar graph are retrieved from the `TEXT["PROFILE COMPLETENESS"]["xaxis"]` dictionary key.
        - The y-axis values represent the count of each profile completion grade.
        - The function iterates over the x-axis values and retrieves the corresponding count from the program profile completion table.
        - If a profile completion grade does not exist in the table, the count is set to 0.
        - The `plot_bar_graph` function is called to generate the bar graph using the x-axis and y-axis values.
        - The graph is saved with the filename specified in `TEXT["PROFILE COMPLETENESS"]["filename"]` in the specified directory.
    """
    df = create_program_profile_completion_table(df)
    x_axis = TEXT["PROFILE COMPLETENESS"]["xaxis"]
    y_axis = [0, 0, 0]
    for i in range(3):
        try:
            y_axis[i] = df[TEXT["APPENDIX PROGRAM PROFILE COMPLETION LIST"]["columns"][2]].value_counts()[x_axis[i]]
        except KeyError:
            y_axis[i] = 0
    plot_bar_graph(x_axis, y_axis, "PROFILE COMPLETENESS", VIRIDIAN)
    return save_graph(TEXT["PROFILE COMPLETENESS"]["filename"], directory, 300)


def graph_missing_organization_contact_info(df: pd.DataFrame, directory: str) -> str:
    """
    Generates a bar graph to visualize the missing organization contact information based on the provided DataFrame.

    Args:
        `df` (pd.DataFrame): The Pandas DataFrame containing the organization contact information data.
        `directory` (str): The directory where the generated graph will be saved.

    Returns:
        `str`: A string containing the path to the graph, saved as a png, from the root directory. 

    Preconditions:
        - The Pandas DataFrame `df` must contain the necessary columns and represent the relevant organization contact information data.
        - `directory` must be a valid directory path.

    Raises:
        None

    Example:
        >>> graph_missing_organization_contact_info(data, "/path/to/directory")
        # Generates a bar graph based on the missing organization contact information data in the DataFrame `data`,
        # and saves the graph in the specified directory.

    Notes:
        - Ensure that the DataFrame `df` contains the necessary columns and represents the relevant organization contact information data.
        - Provide a valid directory path in `directory` to save the generated graph.

    Additional Information:
        - The function first creates an organization contact information table based on the provided DataFrame using the `create_organization_contact_information_table` function.
        - The x-axis values for the bar graph are retrieved from the `TEXT["VIVERY CONTACT INFORMATION"]["xaxis"]` dictionary key.
        - The y-axis values represent the count of missing values for different contact information fields.
        - The function calculates the count of missing values for each contact information field:
          - The first y-axis value represents the count of rows where all contact information fields are missing.
          - The second y-axis value represents the count of rows where only the first contact information field is missing.
          - The third y-axis value represents the count of rows where only the second contact information field is missing.
          - The fourth y-axis value represents the count of rows where only the third contact information field is missing.
          - The fifth y-axis value represents the count of rows where all contact information fields are present.
        - The `plot_bar_graph` function is called to generate the bar graph using the x-axis and y-axis values.
        - The graph is saved with the filename specified in `TEXT["VIVERY CONTACT INFORMATION"]["filename"]` in the specified directory.
    """
    df = create_organization_contact_information_table(df)
    x_axis = TEXT["VIVERY CONTACT INFORMATION"]["xaxis"]
    y_axis = [
        len(df[df[TEXT["APPENDIX ORGANIZATION CONTACT INFORMATION"]["columns"][1:]].isna().all(axis=1)]),
        len(df[df[TEXT["APPENDIX ORGANIZATION CONTACT INFORMATION"]["columns"][1]].isna()]) - len(df[df[TEXT["APPENDIX ORGANIZATION CONTACT INFORMATION"]["columns"][1:]].isna().all(axis=1)]),
        len(df[df[TEXT["APPENDIX ORGANIZATION CONTACT INFORMATION"]["columns"][2]].isna()]) - len(df[df[TEXT["APPENDIX ORGANIZATION CONTACT INFORMATION"]["columns"][1:]].isna().all(axis=1)]),
        len(df[df[TEXT["APPENDIX ORGANIZATION CONTACT INFORMATION"]["columns"][3]].isna()]) - len(df[df[TEXT["APPENDIX ORGANIZATION CONTACT INFORMATION"]["columns"][1:]].isna().all(axis=1)]),
        len(df[df[TEXT["APPENDIX ORGANIZATION CONTACT INFORMATION"]["columns"][1:]].notna().all(axis=1)])
        ]
    plot_bar_graph(x_axis, y_axis, "VIVERY CONTACT INFORMATION", VIVERY_GREEN)
    return save_graph(TEXT["VIVERY CONTACT INFORMATION"]["filename"], directory, 300)


def graph_missing_location_contact_info(df: pd.DataFrame, directory: str) -> str:
    """
    Generates a bar graph to visualize the missing location contact information based on the provided DataFrame.

    Args:
        `df` (pd.DataFrame): The Pandas DataFrame containing the location contact information data.
        `directory` (str): The directory where the generated graph will be saved.

    Returns:
        `str`: A string containing the path to the graph, saved as a png, from the root directory. 

    Preconditions:
        - The Pandas DataFrame `df` must contain the necessary columns and represent the relevant location contact information data.
        - `directory` must be a valid directory path.

    Raises:
        None

    Example:
        >>> graph_missing_location_contact_info(data, "/path/to/directory")
        # Generates a bar graph based on the missing location contact information data in the DataFrame `data`,
        # and saves the graph in the specified directory.

    Notes:
        - Ensure that the DataFrame `df` contains the necessary columns and represents the relevant location contact information data.
        - Provide a valid directory path in `directory` to save the generated graph.

    Additional Information:
        - The function first creates a location contact information table based on the provided DataFrame using the `create_location_contact_information_table` function.
        - The x-axis values for the bar graph are retrieved from the `TEXT["PUBLIC CONTACT INFORMATION"]["location xaxis"]` dictionary key.
        - The y-axis values represent the count of missing values for different contact information fields.
        - The function calculates the count of missing values for each contact information field:
          - The first y-axis value represents the count of rows where all contact information fields are missing.
          - The second y-axis value represents the count of rows where only the first contact information field is missing.
          - The third y-axis value represents the count of rows where only the second contact information field is missing.
          - The fourth y-axis value represents the count of rows where only the third contact information field is missing.
          - The fifth y-axis value represents the count of rows where only the fourth contact information field is missing.
          - The sixth y-axis value represents the count of rows where all contact information fields are present.
        - The `plot_bar_graph` function is called to generate the bar graph using the x-axis and y-axis values.
        - The graph is saved with the filename specified in `TEXT["PUBLIC CONTACT INFORMATION"]["location filename"]` in the specified directory.
    """
    df = create_location_contact_information_table(df)
    x_axis = TEXT["PUBLIC CONTACT INFORMATION"]["location xaxis"]
    y_axis = [
        len(df[df[TEXT["APPENDIX LOCATION CONTACT INFORMATION"]["columns"][1:]].isna().all(axis=1)]),
        len(df[df[TEXT["APPENDIX LOCATION CONTACT INFORMATION"]["columns"][1]].isna()]) - len(df[df[TEXT["APPENDIX LOCATION CONTACT INFORMATION"]["columns"][1:]].isna().all(axis=1)]),
        len(df[df[TEXT["APPENDIX LOCATION CONTACT INFORMATION"]["columns"][2]].isna()]) - len(df[df[TEXT["APPENDIX LOCATION CONTACT INFORMATION"]["columns"][1:]].isna().all(axis=1)]),
        len(df[df[TEXT["APPENDIX LOCATION CONTACT INFORMATION"]["columns"][3]].isna()]) - len(df[df[TEXT["APPENDIX LOCATION CONTACT INFORMATION"]["columns"][1:]].isna().all(axis=1)]),
        len(df[df[TEXT["APPENDIX LOCATION CONTACT INFORMATION"]["columns"][4]].isna()]) - len(df[df[TEXT["APPENDIX LOCATION CONTACT INFORMATION"]["columns"][1:]].isna().all(axis=1)]),
        len(df[df[TEXT["APPENDIX LOCATION CONTACT INFORMATION"]["columns"][1:]].notna().all(axis=1)])
        ]
    plot_bar_graph(x_axis, y_axis, "PUBLIC CONTACT INFORMATION", VIRIDIAN, xlabel="location xlabel", ylabel="location ylabel")
    return save_graph(TEXT["PUBLIC CONTACT INFORMATION"]["location filename"], directory, 300)


def graph_missing_program_contact_info(df: pd.DataFrame, directory: str) -> str:
    """
    Generates a bar graph to visualize the missing program contact information based on the provided DataFrame.

    Args:
        `df` (pd.DataFrame): The Pandas DataFrame containing the program contact information data.
        `directory` (str): The directory where the generated graph will be saved.

    Returns:
        `str`: A string containing the path to the graph, saved as a png, from the root directory. 

    Preconditions:
        - The Pandas DataFrame `df` must contain the necessary columns and represent the relevant program contact information data.
        - `directory` must be a valid directory path.

    Raises:
        None

    Example:
        >>> graph_missing_program_contact_info(data, "/path/to/directory")
        # Generates a bar graph based on the missing program contact information data in the DataFrame `data`,
        # and saves the graph in the specified directory.

    Notes:
        - Ensure that the DataFrame `df` contains the necessary columns and represents the relevant program contact information data.
        - Provide a valid directory path in `directory` to save the generated graph.

    Additional Information:
        - The function first creates a program contact information table based on the provided DataFrame using the `create_program_contact_information_table` function.
        - The x-axis values for the bar graph are retrieved from the `TEXT["PUBLIC CONTACT INFORMATION"]["program xaxis"]` dictionary key.
        - The y-axis values represent the count of missing values for different contact information fields.
        - The function calculates the count of missing values for each contact information field:
          - The first y-axis value represents the count of rows where all contact information fields are missing.
          - The second y-axis value represents the count of rows where only the first contact information field is missing.
          - The third y-axis value represents the count of rows where only the second contact information field is missing.
          - The fourth y-axis value represents the count of rows where only the third contact information field is missing.
          - The fifth y-axis value represents the count of rows where all contact information fields are present.
        - The `plot_bar_graph` function is called to generate the bar graph using the x-axis and y-axis values.
        - The graph is saved with the filename specified in `TEXT["PUBLIC CONTACT INFORMATION"]["program filename"]` in the specified directory.
    """
    df = create_program_contact_information_table(df)
    x_axis = TEXT["PUBLIC CONTACT INFORMATION"]["program xaxis"]
    y_axis = [
        len(df[df[TEXT["APPENDIX PROGRAM CONTACT INFORMATION"]["columns"][1:]].isna().all(axis=1)]),
        len(df[df[TEXT["APPENDIX PROGRAM CONTACT INFORMATION"]["columns"][1]].isna()]) - len(df[df[TEXT["APPENDIX PROGRAM CONTACT INFORMATION"]["columns"][1:]].isna().all(axis=1)]),
        len(df[df[TEXT["APPENDIX PROGRAM CONTACT INFORMATION"]["columns"][2]].isna()]) - len(df[df[TEXT["APPENDIX PROGRAM CONTACT INFORMATION"]["columns"][1:]].isna().all(axis=1)]),
        len(df[df[TEXT["APPENDIX PROGRAM CONTACT INFORMATION"]["columns"][3]].isna()]) - len(df[df[TEXT["APPENDIX PROGRAM CONTACT INFORMATION"]["columns"][1:]].isna().all(axis=1)]),
        len(df[df[TEXT["APPENDIX PROGRAM CONTACT INFORMATION"]["columns"][1:]].notna().all(axis=1)])
        ]
    plot_bar_graph(x_axis, y_axis, "PUBLIC CONTACT INFORMATION", SAGE, xlabel="program xlabel", ylabel="program ylabel")
    return save_graph(TEXT["PUBLIC CONTACT INFORMATION"]["program filename"], directory, 300)


def graph_program_type(df: pd.DataFrame, directory: str) -> str:
    """
    Generates a pie chart to visualize the distribution of program types.

    Args:
        `df` (pd.DataFrame): The Pandas DataFrame containing the program data.
        `directory` (str): The directory where the graph will be saved.

    Returns:
        `str`: A string containing the path to the graph, saved as a png, from the root directory. 

    Preconditions:
        - The Pandas DataFrame `df` must contain the necessary columns and represent the relevant program data.
        - The `directory` must be a valid path to an existing directory.

    Raises:
        None

    Example:
        >>> graph_program_type(data, "graphs/")
        # Generates a pie chart based on the program types in the provided DataFrame.
        # The resulting graph is saved in the "graphs/" directory.

    Additional Information:
        - The function calls `create_program_by_program_type_table()` to create a DataFrame with program types.
        - The number of programs in each program type is calculated and stored in `sizes`.
        - The colours for the pie chart slices are defined in `colours`.
        - The function calls `plot_pie_graph()` to generate the pie chart using `sizes`, `colours`, and the appropriate text section and labels.
        - The resulting graph is saved in the specified directory with a filename retrieved from the `TEXT` dictionary.
    """
    df = create_program_by_program_type_table(df)
    sizes = [len(df.loc[df["Program Type"] == "Food Program"]), len(df) - len(df.loc[df["Program Type"] == "Food Program"])]
    colours = [SAGE, VIRIDIAN]
    plot_pie_graph(sizes, colours, "PROGRAM TYPES", labels="program types labels")
    return save_graph(TEXT["PROGRAM TYPES"]["program types filename"], directory, 300)


def graph_food_program_breakdown(df: pd.DataFrame, directory: str) -> str:
    """
    Generates a pie chart to provide a breakdown of food programs.

    Args:
        `df` (pd.DataFrame): The Pandas DataFrame containing the food program data.
        `directory` (str): The directory where the graph will be saved.

    Returns:
        `str`: A string containing the path to the graph, saved as a png, from the root directory. 

    Preconditions:
        - The Pandas DataFrame `df` must contain the necessary columns and represent the relevant food program data.
        - The `directory` must be a valid path to an existing directory.

    Raises:
        None

    Example:
        >>> graph_food_program_breakdown(data, "graphs/")
        # Generates a pie chart based on the food program breakdown in the provided DataFrame.
        # The resulting graph is saved in the "graphs/" directory.

    Additional Information:
        - The function calls `create_program_by_program_type_table()` to create a DataFrame for program types.
        - The number of rows in each category of food programs is calculated and stored in `sizes`.
        - The colours for the pie chart slices are defined in `colours`.
        - The function calls `plot_pie_graph()` to generate the pie chart using `sizes`, `colours`, and the appropriate text section.
        - The resulting graph is saved in the specified directory with a filename retrieved from the `TEXT` dictionary.
    """
    df = create_program_by_program_type_table(df)
    sizes = [
        len(df.loc[df["Type Specification"] == 'Food Distribution']),
        len(df.loc[df["Type Specification"] == "Hot/Cold Meal Program"]),
        len(df.loc[df["Type Specification"] == "Pop-Up/Mobile Resource"]),
        len(df.loc[df["Type Specification"] == "Shelter"]),
        len(df.loc[(df["Type Specification"] != 'Food Distribution') & (df["Type Specification"] != 'Hot/Cold Meal Program') & (df["Type Specification"] != 'Pop-Up/Mobile Resource') & (df["Type Specification"] != 'Shelter')])
        ]
    colours = [VIVERY_GREEN, VIRIDIAN, SAGE, NEON_LIME, NEON_BLUE]
    plot_pie_graph(sizes, colours, "PROGRAM TYPES", labels="food program types labels")
    return save_graph(TEXT["PROGRAM TYPES"]["food program types filename"], directory, 300)


def graph_program_filter_usage(df: pd.DataFrame, directory: str) -> str:
    """
    Generates a bar graph to visualize the usage of program and location filter fields.

    Args:
        `df` (pd.DataFrame): The DataFrame containing the program and location filter fields data.
        `directory` (str): The directory path where the generated graph will be saved.

    Returns:
        `str`: A string containing the path to the graph, saved as a png, from the root directory. 

    Preconditions:
        - The DataFrame `df` must contain the necessary columns representing the program and location filter fields.
        - The `directory` must be a valid directory path.

    Raises:
        None

    Example:
        >>> graph_program_filter_usage(data, "/path/to/directory")
        # Generates a bar graph based on the usage of program and location filter fields in the DataFrame `data`,
        # and saves the graph in the specified directory.

    Additional Information:
        - The function retrieves the count of non-null values for each program filter field from the DataFrame `df`.
        - The function also retrieves the count of non-null values for each location filter field from the DataFrame `df`.
        - The x-axis values for the bar graph are retrieved from the `TEXT["PROGRAM FILTER FIELDS"]["xaxis"]` dictionary key.
        - The y-axis values represent the count of non-null values for each program and location filter field.
        - The function calculates the y-axis values by concatenating the counts of program filter fields and location filter fields.
        - The `plot_bar_graph` function is called to generate the bar graph using the `x-axis` and `y-axis` values.
        - The graph is saved with the filename specified in `TEXT["PROGRAM FILTER FIELDS"]["filename"]` in the specified directory.
    """
    programs = df[["Program External ID", "Program Audience Groups", "Languages Spoken", "Food Program Features", "Items Offered", "Dietary Options Available"]].drop_duplicates().notna().sum().to_list()[1:]
    locations = df[["Location External ID", "Location Features"]].drop_duplicates().notna().sum().to_list()[1:]
    x_axis = TEXT["PROGRAM FILTER FIELDS"]["xaxis"]
    y_axis = programs + locations
    plot_bar_graph(x_axis, y_axis, "PROGRAM FILTER FIELDS", SAGE)
    return save_graph(TEXT["PROGRAM FILTER FIELDS"]["filename"], directory, 300)


def graph_network_hours_overview(df: pd.DataFrame, directory: str) -> str:
    """
    Generates a pie chart to provide an overview of network hours.

    Args:
        `df` (pd.DataFrame): The Pandas DataFrame containing the network hours data.
        `directory` (str): The directory where the graph will be saved.

    Returns:
        `str`: A string containing the path to the graph, saved as a png, from the root directory.       

    Preconditions:
        - The Pandas DataFrame `df` must contain the necessary columns and represent the relevant network hours data.
        - The `directory` must be a valid path to an existing directory.

    Raises:
        None

    Example:
        >>> graph_network_hours_overview(data, "graphs/")
        # Generates a pie chart based on the network hours in the provided DataFrame.
        # The resulting graph is saved in the "graphs/" directory.

    Additional Information:
        - The function calls `create_location_hours_table()` and `create_program_hours_table()` to create DataFrames for location hours and program hours, respectively.
        - The number of rows in each DataFrame is calculated and stored in `sizes`.
        - The colours for the pie chart slices are defined in `colours`.
        - The function calls `plot_pie_graph()` to generate the pie chart using `sizes`, `colours`, and the appropriate text section.
        - The resulting graph is saved in the specified directory with a filename retrieved from the `TEXT` dictionary.
    """
    location_hours_dataframe = create_location_hours_table(df)
    program_hours_dataframe = create_program_hours_table(df)
    sizes = [len(program_hours_dataframe), len(location_hours_dataframe)]
    colours = [SAGE, VIRIDIAN]
    plot_pie_graph(sizes, colours, "NETWORK HOURS OVERVIEW")
    return save_graph(TEXT["NETWORK HOURS OVERVIEW"]["filename"], directory, 300)


def graph_sample_location_hours_current_month(df: pd.DataFrame, directory: str) -> str:
    """
    Generates a bar graph to display the sample location hours for the current month.

    Args:
        `df` (pd.DataFrame): The DataFrame containing location hours data.
        `directory` (str): The directory path where the generated graph will be saved.

    Returns:
        `str`: A string containing the path to the graph, saved as a png, from the root directory.       

    Preconditions:
        - The DataFrame `df` must contain the necessary columns representing location hours data.
        - The `directory` must be a valid directory path.

    Raises:
        None

    Example:
        >>> graph_sample_location_hours_current_month(data, "/path/to/directory")
        # Generates a bar graph based on the sample location hours for the current month using the DataFrame `data`,
        # and saves the graph in the specified directory.

    Additional Information:
        - The function initializes `current_month` as a dictionary with dates as keys and initial values set to zero.
        - The function retrieves weekly hours data and updates the corresponding weekdays in `current_month` based on the opening and closing hours.
        - The function retrieves every other week hours data and updates the corresponding weekdays in `current_month` based on the opening and closing hours.
        - The function retrieves week of the month hours data and updates the corresponding dates in `current_month` based on the opening and closing hours and the specified week and day of the week.
        - The function retrieves day of the month hours data and updates the corresponding dates in `current_month` based on the opening and closing hours and the specified day and day of the week.
        - The function retrieves specific date hours data and updates the corresponding dates in `current_month` based on the opening and closing hours and the specified specific dates.
        - The function generates a bar graph using the x-axis values from `current_month` and the y-axis values representing the accumulated hours.
        - The graph is saved with the filename specified in `TEXT["LOCATION HOURS PREVIEW"]["current month filename"]` in the specified directory.
    """
    # Initialize dates
    current_month = {day: 0 for day in pd.date_range(start=datetime.date.today().replace(day=1),
                                                     end=(datetime.date.today().replace(day=1) + datetime.timedelta(days=32)).replace(day=1), freq='D'
                                                     ).to_pydatetime()}
    
    # Weekly hours
    weekly_weekdays = {"Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0, "Saturday": 0, "Sunday": 0}
    weekly_hours = create_location_hours_table(df.loc[df["Frequency"] == "Weekly"])
    for _, rows in weekly_hours.iterrows():
        weekly_weekdays[rows["Day"]] += int(datetime.datetime.strptime(rows["Closing Hour"], '%H:%M').hour - datetime.datetime.strptime(rows["Opening Hour"], '%H:%M').hour)
    for day, _ in current_month.items():
        current_month[day] += weekly_weekdays[calendar.day_name[day.weekday()]]

    # Every other week hours
    every_other_week_weekdays = {"Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0, "Saturday": 0, "Sunday": 0}
    every_other_week_hours = create_location_hours_table(df.loc[df["Frequency"] == "Every Other Week"])
    for _, rows in every_other_week_hours.iterrows():
        every_other_week_weekdays[rows["Day"]] += int(datetime.datetime.strptime(rows["Closing Hour"], '%H:%M').hour - datetime.datetime.strptime(rows["Opening Hour"], '%H:%M').hour)
    for day, _ in current_month.items():
        if (day.toordinal() % 14 <= 6):
            current_month[day] += every_other_week_weekdays[calendar.day_name[day.weekday()]]
    
    # Week of month
    week_of_month_hours = df.loc[(df["Frequency"] == "Week of Month") & (df['Hours Entity Type'] == 'Program')]
    for _, rows in week_of_month_hours.iterrows():
        current_month_day_indexer = datetime.date.today().replace(day=1)
        current_month_week_counter = 1
        current_month_day_counter = 1
        while calendar.day_name[current_month_day_indexer.weekday()] != rows['Day of Week'] or current_month_week_counter != rows['Week of Month']:
            current_month_day_indexer = datetime.date.today().replace(day=current_month_day_counter)
            current_month_day_counter += 1
            current_month_week_counter += calendar.day_name[current_month_day_indexer.weekday()] == "Saturday"
        for i in range(1, 4):
            try:
                current_month[datetime.datetime.strptime(str(current_month_day_indexer), '%Y-%m-%d')] += int(datetime.datetime.strptime(rows["Hours Closed " + str(i)], '%H:%M').hour - datetime.datetime.strptime(rows["Hours Open " + str(i)], '%H:%M').hour)
            except TypeError:
                pass

    # Day of month
    day_of_month_hours = df.loc[(df["Frequency"] == "Day of Month") & (df['Hours Entity Type'] == 'Location')]
    for _, rows in day_of_month_hours.iterrows():
        current_month_indexer = pd.date_range(datetime.date.today().replace(day=1), (datetime.date.today().replace(day=1) + datetime.timedelta(days=32)).replace(day=1), freq='WOM-'+ str(int(rows['Day of Month'])) + rows['Day of Week'][0:3].upper())[0]
        for i in range(1, 4):
            try:
                current_month[current_month_indexer] += int(datetime.datetime.strptime(rows["Hours Closed " + str(i)], '%H:%M').hour - datetime.datetime.strptime(rows["Hours Open " + str(i)], '%H:%M').hour)
            except TypeError:
                pass
    
    # Specific date
    specific_date_hours = df.loc[(df["Specific Date Reason"].notna()) & (df["Hours Entity Type"] == "Location")]
    for _, rows in specific_date_hours.iterrows():
        if pd.date_range(start=datetime.datetime.strptime(str(rows["Specific Date"]), '%Y-%m-%d'), periods=1).to_pydatetime()[0] in current_month.keys():
            for i in range(1, 4):
                try:
                    current_month[datetime.datetime.strptime(str(rows["Specific Date"]), '%Y-%m-%d')] += int(datetime.datetime.strptime(rows["Hours Closed " + str(i)], '%H:%M').hour - datetime.datetime.strptime(rows["Hours Open " + str(i)], '%H:%M').hour)
                except TypeError:
                    pass
        if pd.date_range(start=datetime.datetime.strptime(str(rows["Specific Date"]), '%Y-%m-%d'), periods=1).to_pydatetime()[0] in current_month.keys() and rows["Specific Date Closed Indicator"] == "CLOSED":
            current_month[datetime.datetime.strptime(str(rows["Specific Date"]), '%Y-%m-%d')] = 0

    # Graph
    x_axis = [str(date.strftime("%d")) for date in list(current_month.keys())[:-1]]
    y_axis = list(current_month.values())[:-1]
    TEXT["LOCATION HOURS PREVIEW"]["xlabel"] = calendar.month_name[int(list(current_month.keys())[0].strftime("%m"))]
    TEXT["LOCATION HOURS PREVIEW"]["current month filename"] = "location_hours_" + calendar.month_name[int(list(current_month.keys())[0].strftime("%m"))].lower() + ".png"
    plot_bar_graph(x_axis, y_axis, "LOCATION HOURS PREVIEW", VIRIDIAN, rotation=45)
    return save_graph(TEXT["LOCATION HOURS PREVIEW"]["current month filename"], directory, 300)


def graph_sample_location_hours_next_month(df: pd.DataFrame, directory: str) -> str:
    """
    Generates a bar graph to display the sample location hours for the next month.

    Args:
        `df` (pd.DataFrame): The DataFrame containing location hours data.
        `directory` (str): The directory path where the generated graph will be saved.

    Returns:
        `str`: A string containing the path to the graph, saved as a png, from the root directory.   

    Preconditions:
        - The DataFrame `df` must contain the necessary columns representing location hours data.
        - The `directory` must be a valid directory path.

    Raises:
        None

    Example:
        >>> graph_sample_location_hours_next_month(data, "/path/to/directory")
        # Generates a bar graph based on the sample location hours for the next month using the DataFrame `data`,
        # and saves the graph in the specified directory.

    Additional Information:
        - The function initializes `next_month` as a dictionary with dates as keys and initial values set to zero.
        - The function retrieves weekly hours data and updates the corresponding weekdays in `next_month` based on the opening and closing hours.
        - The function retrieves every other week hours data and updates the corresponding weekdays in `next_month` based on the opening and closing hours.
        - The function retrieves week of the month hours data and updates the corresponding dates in `next_month` based on the opening and closing hours and the specified week and day of the week.
        - The function retrieves day of the month hours data and updates the corresponding dates in `next_month` based on the opening and closing hours and the specified day and day of the week.
        - The function retrieves specific date hours data and updates the corresponding dates in `next_month` based on the opening and closing hours and the specified specific dates.
        - The function generates a bar graph using the x-axis values from `next_month` and the y-axis values representing the accumulated hours.
        - The graph is saved with the filename specified in `TEXT["LOCATION HOURS PREVIEW"]["next month filename"]` in the specified directory.
    """
    # Initialize dates
    next_month = {day: 0 for day in pd.date_range(start=(datetime.date.today().replace(day=1) + datetime.timedelta(days=32)).replace(day=1),
                                                  end=(datetime.date.today().replace(day=1) + datetime.timedelta(days=63)).replace(day=1), freq='D'
                                                  ).to_pydatetime()}
    
    # WEEKLY HOURS
    weekly_weekdays = {"Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0, "Saturday": 0, "Sunday": 0}
    weekly_hours = create_location_hours_table(df.loc[df["Frequency"] == "Weekly"])
    for _, rows in weekly_hours.iterrows():
        weekly_weekdays[rows["Day"]] += int(datetime.datetime.strptime(rows["Closing Hour"], '%H:%M').hour - datetime.datetime.strptime(rows["Opening Hour"], '%H:%M').hour)
    for day, _ in next_month.items():
        next_month[day] += weekly_weekdays[calendar.day_name[day.weekday()]]

    # EVERY OTHER WEEK HOURS
    every_other_week_weekdays = {"Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0, "Saturday": 0, "Sunday": 0}
    every_other_week_hours = create_location_hours_table(df.loc[df["Frequency"] == "Every Other Week"])
    for _, rows in every_other_week_hours.iterrows():
        every_other_week_weekdays[rows["Day"]] += int(datetime.datetime.strptime(rows["Closing Hour"], '%H:%M').hour - datetime.datetime.strptime(rows["Opening Hour"], '%H:%M').hour)
    for day, _ in next_month.items():
        if (day.toordinal() % 14 <= 6):
            next_month[day] += every_other_week_weekdays[calendar.day_name[day.weekday()]]
    
    # WEEK OF MONTH
    week_of_month_hours = df.loc[(df["Frequency"] == "Week of Month") & (df['Hours Entity Type'] == 'Location')]
    for _, rows in week_of_month_hours.iterrows():
        next_month_day_indexer = (datetime.date.today().replace(day=1) + datetime.timedelta(days=32)).replace(day=1)
        next_month_week_counter = 1
        next_month_day_counter = 1
        while calendar.day_name[next_month_day_indexer.weekday()] != rows['Day of Week'] or next_month_week_counter != rows['Week of Month']:
            next_month_day_indexer = (datetime.date.today().replace(day=1) + datetime.timedelta(days=32)).replace(day=next_month_day_counter)
            next_month_day_counter += 1
            next_month_week_counter += calendar.day_name[next_month_day_indexer.weekday()] == "Saturday"
        for i in range(1, 4):
            try:
                next_month[datetime.datetime.strptime(str(next_month_day_indexer), '%Y-%m-%d')] += int(datetime.datetime.strptime(rows["Hours Closed " + str(i)], '%H:%M').hour - datetime.datetime.strptime(rows["Hours Open " + str(i)], '%H:%M').hour)
            except TypeError:
                pass

    # DAY OF MONTH
    day_of_month_hours = df.loc[(df["Frequency"] == "Day of Month") & (df['Hours Entity Type'] == 'Location')]
    for _, rows in day_of_month_hours.iterrows():
        next_month_indexer = pd.date_range((datetime.date.today().replace(day=1) + datetime.timedelta(days=32)).replace(day=1), (datetime.date.today().replace(day=1) + datetime.timedelta(days=63)).replace(day=1), freq='WOM-'+ str(int(rows['Day of Month'])) + rows['Day of Week'][0:3].upper())[0]
        for i in range(1, 4):
            try:
                next_month[next_month_indexer] += int(datetime.datetime.strptime(rows["Hours Closed " + str(i)], '%H:%M').hour - datetime.datetime.strptime(rows["Hours Open " + str(i)], '%H:%M').hour)
            except TypeError:
                pass
    
    specific_date_hours = df.loc[(df["Specific Date Reason"].notna()) & (df["Hours Entity Type"] == "Location")]
    for _, rows in specific_date_hours.iterrows():
        if pd.date_range(start=datetime.datetime.strptime(str(rows["Specific Date"]), '%Y-%m-%d'), periods=1).to_pydatetime()[0] in next_month.keys():
            for i in range(1, 4):
                try:
                    next_month[datetime.datetime.strptime(str(rows["Specific Date"]), '%Y-%m-%d')] += int(datetime.datetime.strptime(rows["Hours Closed " + str(i)], '%H:%M').hour - datetime.datetime.strptime(rows["Hours Open " + str(i)], '%H:%M').hour)
                except TypeError:
                    pass
        if pd.date_range(start=datetime.datetime.strptime(str(rows["Specific Date"]), '%Y-%m-%d'), periods=1).to_pydatetime()[0] in next_month.keys() and rows["Specific Date Closed Indicator"] == "CLOSED":
            next_month[datetime.datetime.strptime(str(rows["Specific Date"]), '%Y-%m-%d')] = 0
    # Graph
    x_axis = [str(date.strftime("%d")) for date in list(next_month.keys())[:-1]]
    y_axis = list(next_month.values())[:-1]
    TEXT["LOCATION HOURS PREVIEW"]["xlabel"] = calendar.month_name[int(list(next_month.keys())[0].strftime("%m"))]
    TEXT["LOCATION HOURS PREVIEW"]["current month filename"] = "location_hours_" + calendar.month_name[int(list(next_month.keys())[0].strftime("%m"))].lower() + ".png"
    plot_bar_graph(x_axis, y_axis, "LOCATION HOURS PREVIEW", VIRIDIAN, rotation=45)
    return save_graph(TEXT["LOCATION HOURS PREVIEW"]["current month filename"], directory, 300)


def graph_sample_program_hours_current_month(df: pd.DataFrame, directory: str) -> str:
    """
    Generates a bar graph to display the sample program hours for the current month.

    Args:
        `df` (pd.DataFrame): The DataFrame containing program hours data.
        `directory` (str): The directory path where the generated graph will be saved.

    Returns:
        `str`: A string containing the path to the graph, saved as a png, from the root directory.   

    Preconditions:
        - The DataFrame `df` must contain the necessary columns representing program hours data.
        - The `directory` must be a valid directory path.

    Raises:
        None

    Example:
        >>> graph_sample_program_hours_current_month(data, "/path/to/directory")
        # Generates a bar graph based on the sample program hours for the current month using the DataFrame `data`,
        # and saves the graph in the specified directory.

    Additional Information:
        - The function initializes `current_month` as a dictionary with dates as keys and initial values set to zero.
        - The function retrieves weekly hours data and updates the corresponding weekdays in `current_month` based on the opening and closing hours.
        - The function retrieves every other week hours data and updates the corresponding weekdays in `current_month` based on the opening and closing hours.
        - The function retrieves week of the month hours data and updates the corresponding dates in `current_month` based on the opening and closing hours and the specified week and day of the week.
        - The function retrieves day of the month hours data and updates the corresponding dates in `current_month` based on the opening and closing hours and the specified day and day of the week.
        - The function retrieves specific date hours data and updates the corresponding dates in `current_month` based on the opening and closing hours and the specified specific dates.
        - The function generates a bar graph using the x-axis values from `current_month` and the y-axis values representing the accumulated hours.
        - The graph is saved with the filename specified in `TEXT["PROGRAM HOURS PREVIEW"]["current month filename"]` in the specified directory.
    """
    # Initialize dates
    current_month = {day: 0 for day in pd.date_range(start=datetime.date.today().replace(day=1),
                                                     end=(datetime.date.today().replace(day=1) + datetime.timedelta(days=32)).replace(day=1), freq='D'
                                                     ).to_pydatetime()}
    
    # Weekly hours
    weekly_weekdays = {"Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0, "Saturday": 0, "Sunday": 0}
    weekly_hours = create_program_hours_table(df.loc[df["Frequency"] == "Weekly"])
    for _, rows in weekly_hours.iterrows():
        weekly_weekdays[rows["Day"]] += int(datetime.datetime.strptime(rows["Closing Hour"], '%H:%M').hour - datetime.datetime.strptime(rows["Opening Hour"], '%H:%M').hour)
    for day, _ in current_month.items():
        current_month[day] += weekly_weekdays[calendar.day_name[day.weekday()]]

    # Every other week hours
    every_other_week_weekdays = {"Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0, "Saturday": 0, "Sunday": 0}
    every_other_week_hours = create_program_hours_table(df.loc[df["Frequency"] == "Every Other Week"])
    for _, rows in every_other_week_hours.iterrows():
        every_other_week_weekdays[rows["Day"]] += int(datetime.datetime.strptime(rows["Closing Hour"], '%H:%M').hour - datetime.datetime.strptime(rows["Opening Hour"], '%H:%M').hour)
    for day, _ in current_month.items():
        if (day.toordinal() % 14 <= 6):
            current_month[day] += every_other_week_weekdays[calendar.day_name[day.weekday()]]
    
    # Week of month
    week_of_month_hours = df.loc[(df["Frequency"] == "Week of Month") & (df['Hours Entity Type'] == 'Program')]
    for _, rows in week_of_month_hours.iterrows():
        current_month_day_indexer = datetime.date.today().replace(day=1)
        current_month_week_counter = 1
        current_month_day_counter = 1
        while calendar.day_name[current_month_day_indexer.weekday()] != rows['Day of Week'] or current_month_week_counter != rows['Week of Month']:
            current_month_day_indexer = datetime.date.today().replace(day=current_month_day_counter)
            current_month_day_counter += 1
            current_month_week_counter += calendar.day_name[current_month_day_indexer.weekday()] == "Saturday"
        for i in range(1, 4):
            try:
                current_month[datetime.datetime.strptime(str(current_month_day_indexer), '%Y-%m-%d')] += int(datetime.datetime.strptime(rows["Hours Closed " + str(i)], '%H:%M').hour - datetime.datetime.strptime(rows["Hours Open " + str(i)], '%H:%M').hour)
            except TypeError:
                pass

    # Day of month
    day_of_month_hours = df.loc[(df["Frequency"] == "Day of Month") & (df['Hours Entity Type'] == 'Program')]
    for _, rows in day_of_month_hours.iterrows():
        current_month_indexer = pd.date_range(datetime.date.today().replace(day=1), (datetime.date.today().replace(day=1) + datetime.timedelta(days=32)).replace(day=1), freq='WOM-'+ str(int(rows['Day of Month'])) + rows['Day of Week'][0:3].upper())[0]
        for i in range(1, 4):
            try:
                current_month[current_month_indexer] += int(datetime.datetime.strptime(rows["Hours Closed " + str(i)], '%H:%M').hour - datetime.datetime.strptime(rows["Hours Open " + str(i)], '%H:%M').hour)
            except TypeError:
                pass
    
    # Specific date
    specific_date_hours = df.loc[(df["Specific Date Reason"].notna()) & (df["Hours Entity Type"] == 'Program')]
    for _, rows in specific_date_hours.iterrows():
        if pd.date_range(start=datetime.datetime.strptime(str(rows["Specific Date"]), '%Y-%m-%d'), periods=1).to_pydatetime()[0] in current_month.keys():
            for i in range(1, 4):
                try:
                    current_month[datetime.datetime.strptime(str(rows["Specific Date"]), '%Y-%m-%d')] += int(datetime.datetime.strptime(rows["Hours Closed " + str(i)], '%H:%M').hour - datetime.datetime.strptime(rows["Hours Open " + str(i)], '%H:%M').hour)
                except TypeError:
                    pass
        if pd.date_range(start=datetime.datetime.strptime(str(rows["Specific Date"]), '%Y-%m-%d'), periods=1).to_pydatetime()[0] in current_month.keys() and rows["Specific Date Closed Indicator"] == "CLOSED":
            current_month[datetime.datetime.strptime(str(rows["Specific Date"]), '%Y-%m-%d')] = 0

    # Graph
    x_axis = [str(date.strftime("%d")) for date in list(current_month.keys())[:-1]]
    y_axis = list(current_month.values())[:-1]
    TEXT["PROGRAM HOURS PREVIEW"]["xlabel"] = calendar.month_name[int(list(current_month.keys())[0].strftime("%m"))]
    TEXT["PROGRAM HOURS PREVIEW"]["current month filename"] = "program_hours_" + calendar.month_name[int(list(current_month.keys())[0].strftime("%m"))].lower() + ".png"
    plot_bar_graph(x_axis, y_axis, "PROGRAM HOURS PREVIEW", SAGE, rotation=45)
    return save_graph(TEXT["PROGRAM HOURS PREVIEW"]["current month filename"], directory, 300)


def graph_sample_program_hours_next_month(df: pd.DataFrame, directory: str) -> str:
    """
    Generates a bar graph to display the sample program hours for the next month.

    Args:
        `df` (pd.DataFrame): The DataFrame containing program hours data.
        `directory` (str): The directory path where the generated graph will be saved.

    Returns:
        `str`: A string containing the path to the graph, saved as a png, from the root directory.

    Preconditions:
        - The DataFrame `df` must contain the necessary columns representing program hours data.
        - The `directory` must be a valid directory path.

    Raises:
        None

    Example:
        >>> graph_sample_program_hours_next_month(data, "/path/to/directory")
        # Generates a bar graph based on the sample program hours for the next month using the DataFrame `data`,
        # and saves the graph in the specified directory.

    Additional Information:
        - The function initializes `next_month` as a dictionary with dates as keys and initial values set to zero.
        - The function retrieves weekly hours data and updates the corresponding weekdays in `next_month` based on the opening and closing hours.
        - The function retrieves every other week hours data and updates the corresponding weekdays in `next_month` based on the opening and closing hours.
        - The function retrieves week of the month hours data and updates the corresponding dates in `next_month` based on the opening and closing hours and the specified week and day of the week.
        - The function retrieves day of the month hours data and updates the corresponding dates in `next_month` based on the opening and closing hours and the specified day and day of the week.
        - The function retrieves specific date hours data and updates the corresponding dates in `next_month` based on the opening and closing hours and the specified specific dates.
        - The function generates a bar graph using the x-axis values from `next_month` and the y-axis values representing the accumulated hours.
        - The graph is saved with the filename specified in `TEXT["PROGRAM HOURS PREVIEW"]["next month filename"]` in the specified directory.
    """
    # Initialize dates
    next_month = {day: 0 for day in pd.date_range(start=(datetime.date.today().replace(day=1) + datetime.timedelta(days=32)).replace(day=1),
                                                  end=(datetime.date.today().replace(day=1) + datetime.timedelta(days=63)).replace(day=1), freq='D'
                                                  ).to_pydatetime()}
    
    # WEEKLY HOURS
    weekly_weekdays = {"Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0, "Saturday": 0, "Sunday": 0}
    weekly_hours = create_program_hours_table(df.loc[df["Frequency"] == "Weekly"])
    for _, rows in weekly_hours.iterrows():
        weekly_weekdays[rows["Day"]] += int(datetime.datetime.strptime(rows["Closing Hour"], '%H:%M').hour - datetime.datetime.strptime(rows["Opening Hour"], '%H:%M').hour)
    for day, _ in next_month.items():
        next_month[day] += weekly_weekdays[calendar.day_name[day.weekday()]]

    # EVERY OTHER WEEK HOURS
    every_other_week_weekdays = {"Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0, "Saturday": 0, "Sunday": 0}
    every_other_week_hours = create_program_hours_table(df.loc[df["Frequency"] == "Every Other Week"])
    for _, rows in every_other_week_hours.iterrows():
        every_other_week_weekdays[rows["Day"]] += int(datetime.datetime.strptime(rows["Closing Hour"], '%H:%M').hour - datetime.datetime.strptime(rows["Opening Hour"], '%H:%M').hour)
    for day, _ in next_month.items():
        if (day.toordinal() % 14 <= 6):
            next_month[day] += every_other_week_weekdays[calendar.day_name[day.weekday()]]
    
    # WEEK OF MONTH
    week_of_month_hours = df.loc[(df["Frequency"] == "Week of Month") & (df['Hours Entity Type'] == 'Program')]
    for _, rows in week_of_month_hours.iterrows():
        next_month_day_indexer = (datetime.date.today().replace(day=1) + datetime.timedelta(days=32)).replace(day=1)
        next_month_week_counter = 1
        next_month_day_counter = 1
        while calendar.day_name[next_month_day_indexer.weekday()] != rows['Day of Week'] or next_month_week_counter != rows['Week of Month']:
            next_month_day_indexer = (datetime.date.today().replace(day=1) + datetime.timedelta(days=32)).replace(day=next_month_day_counter)
            next_month_day_counter += 1
            next_month_week_counter += calendar.day_name[next_month_day_indexer.weekday()] == "Saturday"
        for i in range(1, 4):
            try:
                next_month[datetime.datetime.strptime(str(next_month_day_indexer), '%Y-%m-%d')] += int(datetime.datetime.strptime(rows["Hours Closed " + str(i)], '%H:%M').hour - datetime.datetime.strptime(rows["Hours Open " + str(i)], '%H:%M').hour)
            except TypeError:
                pass

    # DAY OF MONTH
    day_of_month_hours = df.loc[(df["Frequency"] == "Day of Month") & (df['Hours Entity Type'] == 'Program')]
    for _, rows in day_of_month_hours.iterrows():
        next_month_indexer = pd.date_range((datetime.date.today().replace(day=1) + datetime.timedelta(days=32)).replace(day=1), (datetime.date.today().replace(day=1) + datetime.timedelta(days=63)).replace(day=1), freq='WOM-'+ str(int(rows['Day of Month'])) + rows['Day of Week'][0:3].upper())[0]
        for i in range(1, 4):
            try:
                next_month[next_month_indexer] += int(datetime.datetime.strptime(rows["Hours Closed " + str(i)], '%H:%M').hour - datetime.datetime.strptime(rows["Hours Open " + str(i)], '%H:%M').hour)
            except TypeError:
                pass
    
    specific_date_hours = df.loc[(df["Specific Date Reason"].notna()) & (df["Hours Entity Type"] == 'Program')]
    for _, rows in specific_date_hours.iterrows():
        if pd.date_range(start=datetime.datetime.strptime(str(rows["Specific Date"]), '%Y-%m-%d'), periods=1).to_pydatetime()[0] in next_month.keys():
            for i in range(1, 4):
                try:
                    next_month[datetime.datetime.strptime(str(rows["Specific Date"]), '%Y-%m-%d')] += int(datetime.datetime.strptime(rows["Hours Closed " + str(i)], '%H:%M').hour - datetime.datetime.strptime(rows["Hours Open " + str(i)], '%H:%M').hour)
                except TypeError:
                    pass
        if pd.date_range(start=datetime.datetime.strptime(str(rows["Specific Date"]), '%Y-%m-%d'), periods=1).to_pydatetime()[0] in next_month.keys() and rows["Specific Date Closed Indicator"] == "CLOSED":
            next_month[datetime.datetime.strptime(str(rows["Specific Date"]), '%Y-%m-%d')] = 0
    # Graph
    x_axis = [str(date.strftime("%d")) for date in list(next_month.keys())[:-1]]
    y_axis = list(next_month.values())[:-1]
    TEXT["PROGRAM HOURS PREVIEW"]["xlabel"] = calendar.month_name[int(list(next_month.keys())[0].strftime("%m"))]
    TEXT["PROGRAM HOURS PREVIEW"]["current month filename"] = "program_hours_" + calendar.month_name[int(list(next_month.keys())[0].strftime("%m"))].lower() + ".png"
    plot_bar_graph(x_axis, y_axis, "PROGRAM HOURS PREVIEW", SAGE, rotation=45)
    return save_graph(TEXT["PROGRAM HOURS PREVIEW"]["current month filename"], directory, 300)


def graph_program_qualifications(df: pd.DataFrame, directory: str) -> str:
    """
    Generates a bar graph to visualize the number of programs with missing qualifications.

    Args:
        `df` (pd.DataFrame): The DataFrame containing program data.
        `directory` (str): The directory path where the generated graph will be saved.

    Returns:
        `str`: A string containing the path to the graph, saved as a png, from the root directory.

    Preconditions:
        - The DataFrame `df` must contain the necessary columns representing program qualifications.
        - The `directory` must be a valid directory path.

    Raises:
        None

    Example:
        >>> graph_program_qualifications(data, "/path/to/directory")
        # Generates a bar graph based on the number of programs with missing qualifications in the DataFrame `data`,
        # and saves the graph in the specified directory.

    Additional Information:
        - The function creates two DataFrame objects:
            - `create_program_by_program_qualifications_table(df).dropna()`: Contains programs with non-null qualifications.
            - `create_program_table(df)`: Contains all programs.
        - The x-axis values for the bar graph are retrieved from the `TEXT["MISSING PROGRAM QUALIFICATIONS"]["xaxis"]` dictionary key.
        - The y-axis values represent the number of programs with missing qualifications and the number of programs with qualifications, respectively.
        - The `plot_bar_graph` function is called to generate the bar graph using the `x-axis` and `y-axis` values.
        - The graph is saved with the filename specified in `TEXT["MISSING PROGRAM QUALIFICATIONS"]["filename"]` in the specified directory.
    """
    x_axis = TEXT["MISSING PROGRAM QUALIFICATIONS"]["xaxis"]
    y_axis = [len(create_program_by_program_qualifications_table(df).dropna()), len(create_program_table(df)) - len(create_program_by_program_qualifications_table(df).dropna())] 
    plot_bar_graph(x_axis, y_axis, "MISSING PROGRAM QUALIFICATIONS", SAGE)
    return save_graph(TEXT["MISSING PROGRAM QUALIFICATIONS"]["filename"], directory, 300)


def graph_program_service_areas(df: pd.DataFrame, directory: str) -> str:
    """
    Generates a bar graph to visualize the number of programs with missing service areas.

    Args:
        `df` (pd.DataFrame): The DataFrame containing program data.
        `directory` (str): The directory path where the generated graph will be saved.

    Returns:
        `str`: A string containing the path to the graph, saved as a png, from the root directory.

    Preconditions:
        - The DataFrame `df` must contain the necessary columns representing program service areas.
        - The `directory` must be a valid directory path.

    Raises:
        None

    Example:
        >>> graph_program_service_areas(data, "/path/to/directory")
        # Generates a bar graph based on the number of programs with missing service areas in the DataFrame `data`,
        # and saves the graph in the specified directory.

    Additional Information:
        - The function creates two DataFrame objects:
            - `create_program_by_program_services_table(df).dropna()`: Contains programs with non-null service areas.
            - `create_program_table(df)`: Contains all programs.
        - The x-axis values for the bar graph are retrieved from the `TEXT["MISSING PROGRAM SERVICE AREA"]["xaxis"]` dictionary key.
        - The y-axis values represent the number of programs with missing service areas and the number of programs with service areas, respectively.
        - The `plot_bar_graph` function is called to generate the bar graph using the `x-axis` and `y-axis` values.
        - The graph is saved with the filename specified in `TEXT["MISSING PROGRAM SERVICE AREA"]["filename"]` in the specified directory.
    """
    x_axis = TEXT["MISSING PROGRAM SERVICE AREA"]["xaxis"]
    y_axis = [len(create_program_by_program_services_table(df).dropna()), len(create_program_table(df)) - len(create_program_by_program_services_table(df).dropna())] 
    plot_bar_graph(x_axis, y_axis, "MISSING PROGRAM SERVICE AREA", SAGE)
    return save_graph(TEXT["MISSING PROGRAM SERVICE AREA"]["filename"], directory, 300)




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
        df[['Location External ID', 'Location Approval Status', 'Location Active Status']].loc[(df['Location Approval Status'] == True) & (df['Location Active Status'] == True) & (df['Organization Approval Status'] == True) & (df['Organization Active Status'] == True)]['Location External ID'].nunique(),
        df[['Program External ID', 'Program Approval Status', 'Program Active Status']].loc[(df['Program Approval Status'] == True) & (df['Program Active Status'] == True) & (df['Location Approval Status'] == True) & (df['Location Active Status'] == True) & (df['Organization Approval Status'] == True) & (df['Organization Active Status'] == True)]['Program External ID'].nunique()
        ]
    inactive = [
        df[['Organization External ID', 'Organization Approval Status', 'Organization Active Status']].loc[(df['Organization Approval Status'] != True) | (df['Organization Active Status'] != True)]['Organization External ID'].nunique(),
        df[['Location External ID', 'Location Approval Status', 'Location Active Status']].loc[(df['Location Approval Status'] != True) | (df['Location Active Status'] != True) | (df['Organization Approval Status'] != True) | (df['Organization Active Status'] != True)]['Location External ID'].nunique(),
        df[['Program External ID', 'Program Approval Status', 'Program Active Status']].loc[(df['Program Approval Status'] != True) | (df['Program Active Status'] != True) | (df['Location Approval Status'] != True) | (df['Location Active Status'] != True) | (df['Organization Approval Status'] != True) | (df['Organization Active Status'] != True)]['Program External ID'].nunique()
        ]
    total = [
        df[['Organization External ID', 'Organization Approval Status', 'Organization Active Status']]['Organization External ID'].nunique(),
        df[['Location External ID', 'Location Approval Status', 'Location Active Status']]['Location External ID'].nunique(),
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
    return create_program_profile_completion_table(df).sort_values(by=[TEXT["APPENDIX PROGRAM PROFILE COMPLETION LIST"]["columns"][1], TEXT["APPENDIX PROGRAM PROFILE COMPLETION LIST"]["columns"][0]], ascending=[False, True]).head(5).reset_index(drop=True)


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
    return create_program_profile_completion_table(df).sort_values(by=[TEXT["APPENDIX PROGRAM PROFILE COMPLETION LIST"]["columns"][1], TEXT["APPENDIX PROGRAM PROFILE COMPLETION LIST"]["columns"][0]], ascending=[True, False]).head(5).reset_index(drop=True)


def create_high_low_graded_profiles_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Concatenates the highest graded profiles table and the lowest graded profiles table.

    Args:
        `df` (pd.DataFrame): The Pandas DataFrame containing the profile data.

    Returns:
        `pd.DataFrame`: A DataFrame containing the highest and lowest graded program profiles.
    
    Preconditions:
        - The Pandas DataFrame `df` must contain the necessary columns and represent the relevant profile data.

    Raises:
        None

    Example:
        >>> profile_data = pd.DataFrame({
        ...     'Location': ['A0001', 'A0003', 'A0005', 'A0006'],
        ...     'Points': [18.0, 20.0, 11.0, 6.0],
        ...     'Tier': ['Basic', 'Basic', 'Basic', 'Basic']
        ... })
        >>> result = create_high_low_graded_profiles_table(profile_data)
        >>> print(result)
            Location    Points  Tier    Location    Points      Tier
        0    A0003      20.0    Basic    A0006      6.0         Basic
        1    A0001      18.0    Basic    A0005      11.0        Basic

    Additional Information:
        - The function calls `create_highest_graded_profiles_table()` to create the highest graded profiles table.
        - The function calls `create_lowest_graded_profiles_table()` to create the lowest graded profiles table.
        - The resulting tables are concatenated using `pd.concat()` along the columns axis (axis=1).
        - The concatenated table is returned as the result.
    """
    return pd.concat([create_highest_graded_profiles_table(df), create_lowest_graded_profiles_table(df)], axis=1)


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




# NUMBERS
def calculate_percent_locations_inactive(df: pd.DataFrame, text: dict, section: str, field: str) -> dict:
    """
    Calculates the percentage of inactive locations based on the provided DataFrame.

    Args:
        `df` (pd.DataFrame): The Pandas DataFrame containing the network overview data.
        `text` (dict): The dictionary containing the text sections and fields for updating the results.
        `section` (str): The section in the text dictionary to update.
        `field` (str): The field in the specified section to update.

    Returns:
        `dict`: A dictionary with the modifications to the text field.

    Preconditions:
        - The Pandas DataFrame `df` must contain the necessary columns and represent the network overview data.
        - The `text`, `section`, `field`, must be a valid string with a splot for modifying the string with an integer value.

    Raises:
        None

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
        >>> result = calculate_percent_locations_inactive(data, TEXT, "NETWORK OVERVIEW", "paragraph")
        >>> print(result)
        The percentage of inactive locations is 40%.

    Additional Information:
        - The function calls `create_network_overview_table()` to generate a network overview DataFrame.
        - The percentage of inactive locations is calculated by dividing the number of inactive locations by the total number of locations and multiplying by 100.
        - The result is rounded and stored in the variable `percent_locations_inactive`.
        - The updated `text` dictionary is returned, with the provided `section` and `field` updated with the calculated results.
    """
    df = create_network_overview_table(df)
    percent_locations_inactive = round((list(df[TEXT["NETWORK OVERVIEW"]["columns"][2]])[1] / list(df[TEXT["NETWORK OVERVIEW"]["columns"][3]])[1]) * 100, 1)
    text[section][field] = text[section][field].format(percent_locations_inactive)
    return text


def calculate_locations_programs_without_contact(df: pd.DataFrame, text: dict, section: str, field: str) -> None:
    """
    Calculates the number of locations and programs without contact information based on the provided DataFrame.

    Args:
        `df` (pd.DataFrame): The Pandas DataFrame containing the location and program contact information data.
        `text` (dict): The dictionary containing the text sections and fields for updating the results.
        `section` (str): The section in the text dictionary to update.
        `field` (str): The field in the specified section to update.

    Preconditions:
        - The Pandas DataFrame `df` must contain the necessary columns and represent the location and program contact information data.
        - The `text` dictionary must contain the specified `section` and `field`.
        - The `section` and `field` must be valid keys in the `text` dictionary.

    Returns:
        None. The `text` dictionary is updated with the calculated results.

    Raises:
        None

    Example:
        >>> data = pd.DataFrame({
        ...     'Location External ID': ['L1', 'L2', 'L3', 'L4', 'L5'],
        ...     'Contact Name': [None, 'John', 'Jane', None, 'Mike'],
        ...     'Contact Email': [None, 'john@example.com', 'jane@example.com', 'None', None],
        ...     'Program External ID': ['P1', 'P2', 'P3', 'P4', 'P5'],
        ...     'Contact Name': ['Peter', None, 'Emily', None, 'Sam'],
        ...     'Contact Email': ['peter@example.com', None, 'emily@example.com', 'info@example.com', None]
        ... })
        >>> text = {
        ...     'section1': {
        ...         'field1': 'There are {} locations and {} programs without contact information.'
        ...     }
        ... }
        >>> calculate_locations_programs_without_contact(data, text, 'section1', 'field1')
        >>> print(text)
        {
            'section1': {
                'field1': 'There are 2 locations and 1 programs without contact information.'
            }
        }

    Additional Information:
        - The function calls `create_location_contact_information_table()` to create a DataFrame for location contact information.
        - The function calls `create_program_contact_information_table()` to create a DataFrame for program contact information.
        - The number of locations without contact information is calculated by filtering the location DataFrame for rows where all contact information columns are NaN.
        - The number of programs without contact information is calculated by filtering the program DataFrame for rows where all contact information columns are NaN.
        - The results are formatted using the specified `section` and `field` in the `text` dictionary.
        - The updated `text` dictionary is returned, with the provided `section` and `field` updated with the calculated results.
    """
    location_df = create_location_contact_information_table(df)
    program_df = create_program_contact_information_table(df)
    locations_without_contact = len(location_df.loc[(location_df[TEXT["APPENDIX LOCATION CONTACT INFORMATION"]["columns"][1]].isna()) & (location_df[TEXT["APPENDIX LOCATION CONTACT INFORMATION"]["columns"][2]].isna()) & (location_df[TEXT["APPENDIX LOCATION CONTACT INFORMATION"]["columns"][3]].isna()) & (location_df[TEXT["APPENDIX LOCATION CONTACT INFORMATION"]["columns"][4]].isna())])
    programs_without_contact = len(program_df.loc[(program_df[TEXT["APPENDIX PROGRAM CONTACT INFORMATION"]["columns"][1]].isna()) & (program_df[TEXT["APPENDIX PROGRAM CONTACT INFORMATION"]["columns"][2]].isna()) & (program_df[TEXT["APPENDIX PROGRAM CONTACT INFORMATION"]["columns"][3]].isna())])
    text[section][field] = text[section][field].format(locations_without_contact, programs_without_contact)
    return text


def calculate_food_distribution_program_percent(df: pd.DataFrame, text: dict, section: str, field: str) -> None:
    """
    Calculates the percentage of food distribution programs based on the provided DataFrame.

    Args:
        `df` (pd.DataFrame): The Pandas DataFrame containing the program data.
        `text` (dict): The dictionary containing the text sections and fields for updating the results.
        `section` (str): The section in the text dictionary to update.
        `field` (str): The field in the specified section to update.

    Preconditions:
        - The Pandas DataFrame `df` must contain the necessary columns and represent the program data.
        - The `text` dictionary must contain the specified `section` and `field`.
        - The `section` and `field` must be valid keys in the `text` dictionary.

    Returns:
        None. The `text` dictionary is updated with the calculated results.

    Raises:
        None

    Example:
        >>> data = pd.DataFrame({
        ...     'Program External ID': ['P1', 'P2', 'P3', 'P4', 'P5'],
        ...     'Program Type': ['Food Distribution', 'Food Pantry', 'Meal Program', 'Food Distribution', 'Food Distribution']
        ... })
        >>> text = {
        ...     'section1': {
        ...         'field1': 'The percentage of food distribution programs is {}%.'
        ...     }
        ... }
        >>> calculate_food_distribution_program_percent(data, text, 'section1', 'field1')
        >>> print(text)
        {
            'section1': {
                'field1': 'The percentage of food distribution programs is 60.0%.'
            }
        }

    Additional Information:
        - The function calls `create_program_by_program_type_table()` to create a DataFrame for program types.
        - The relevant column for program types is selected using the appropriate key from the TEXT dictionary.
        - The number of rows in the selected column that have the value 'Food Distribution' is calculated.
        - The total number of rows in the selected column is calculated.
        - The percentage of food distribution programs is calculated by dividing the count of 'Food Distribution' rows by the total count and multiplying by 100.
        - The results are formatted using the specified `section` and `field` in the `text` dictionary.
        - The updated `text` dictionary is returned, with the provided `section` and `field` updated with the calculated results.
    """
    df = create_program_by_program_type_table(df)[TEXT["APPENDIX PROGRAM TYPE"]["columns"][2]]
    percent_food_distribution = round((len(df.loc[(df == 'Food Distribution')]) / len(df)) * 100, 1)
    text[section][field] = text[section][field].format(percent_food_distribution)
    return text


def calculate_least_used_programs(df: pd.DataFrame, text: dict, section: str, field: str) -> None:
    """
    Calculates the least used program filters based on the provided DataFrame.

    Args:
        `df` (pd.DataFrame): The Pandas DataFrame containing the program and location data.
        `text` (dict): The dictionary containing the text sections and fields for updating the results.
        `section` (str): The section in the text dictionary to update.
        `field` (str): The field in the specified section to update.

    Returns:
        None. The `text` dictionary is updated with the calculated results.

    Preconditions:
        - The Pandas DataFrame `df` must contain the necessary columns and represent the program and location data.
        - The `text` dictionary must contain the specified `section` and `field`.
        - The `section` and `field` must be valid keys in the `text` dictionary.    

    Raises:
        None

    Example:
        >>> data = pd.DataFrame({
        ...     'Program External ID': ['P1', 'P2', 'P2', 'P3', 'P1'],
        ...     'Program Audience Groups': ['Group1', 'Group2', 'Group1', 'Group3', 'Group1'],
        ...     'Languages Spoken': ['English', 'Spanish', 'English', 'French', 'English'],
        ...     'Food Program Features': [True, False, False, True, True],
        ...     'Items Offered': ['Item1', 'Item2', 'Item1', 'Item3', 'Item1'],
        ...     'Dietary Options Available': ['Option1', 'Option1', 'Option2', 'Option2', 'Option1'],
        ...     'Location External ID': ['L1', 'L2', 'L2', 'L3', 'L1'],
        ...     'Location Features': ['Feature1', 'Feature2', 'Feature1', 'Feature3', 'Feature1']
        ... })
        >>> text = {
        ...     'section1': {
        ...         'field1': 'The least used program filters are "{}" and "{}".'
        ...     }
        ... }
        >>> calculate_least_used_programs(data, text, 'section1', 'field1')
        >>> print(text)
        {
            'section1': {
                'field1': 'The least used program filters are "Languages Spoken" and "Program Audience Groups".'
            }
        }

    Additional Information:
        - The function extracts the necessary columns from the DataFrame for program filters and drops any duplicate rows.
        - The number of non-null values for each program filter is calculated and stored in the `programs` list.
        - The number of non-null values for each location filter is calculated and stored in the `locations` list.
        - The filter usage counts for programs and locations are combined into the `filter_usage` list.
        - The filter groups from the TEXT dictionary are assigned to the `filter_groups` variable.
        - A dictionary `filter_groups_usage` is created to map each filter group to its corresponding usage count.
        - The least used filter group is identified by finding the key with the minimum value in `filter_groups_usage`.
        - The least used filter group is removed from `filter_groups_usage` dictionary.
        - The second least used filter group is identified by finding the key with the new minimum value in `filter_groups_usage`.
        - The results are formatted using the specified `section` and `field` in the `text` dictionary.
        - The updated `text` dictionary is returned, with the provided `section` and `field` updated with the calculated results.
    """
    programs = df[["Program External ID", "Program Audience Groups", "Languages Spoken", "Food Program Features", "Items Offered", "Dietary Options Available"]].drop_duplicates().notna().sum().to_list()[1:]
    locations = df[["Location External ID", "Location Features"]].drop_duplicates().notna().sum().to_list()[1:]
    filter_usage = programs + locations
    filter_groups = TEXT["PROGRAM FILTER FIELDS"]["xaxis"]
    filter_groups_usage = {group: usage for group in filter_groups for usage in filter_usage}
    least_used = [key for key, value in filter_groups_usage.items() if value == min(filter_groups_usage.values())][0]
    del filter_groups_usage[least_used]
    second_least_used = [key for key, value in filter_groups_usage.items() if value == min(filter_groups_usage.values())][0]
    text[section][field] = text[section][field].format(least_used.replace("\n", " "), second_least_used.replace("\n", " "))
    return text




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
        graph_sample_location_hours_current_month,
        graph_sample_location_hours_next_month,
        graph_sample_program_hours_current_month,
        graph_sample_program_hours_next_month,
        graph_program_qualifications,
        graph_program_service_areas
    ]
    # Create a list of DataFrame functions
    dataframe_functions = [
        create_network_overview_table,
        create_highest_graded_profiles_table,
        create_lowest_graded_profiles_table,
        create_high_low_graded_profiles_table,
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
    if not os.path.isdir(directory + "/resources"):
        os.mkdir(directory + "/resources")
    if not os.path.isdir(directory + "/resources/images"):
        os.mkdir(directory + "/resources/images")
    if not os.path.isdir(directory + "/csvs"):
        os.mkdir(directory + "/csvs")
    if not os.path.isdir(directory + "/images"):
        os.mkdir(directory + "/images")
    # Move file to directory
    if args.file.split("\\")[0] != directory:
        shutil.move(args.file, directory)
    # Move resource images to directory
    for image in glob.iglob("resources/images/*png"):
        shutil.copyfile(image, directory + "/resources/images/" + image.split("\\")[1])

    # Create list of silenced functions
    silenced_functions = args.silent if args.silent else []

    # Create valid graphing functions
    valid_graphing_functions = [graph for graph in graphing_functions if graph.__name__ not in silenced_functions]
    # Create valid DataFrame functions
    valid_dataframe_functions = [dataframe for dataframe in dataframe_functions if dataframe.__name__ not in silenced_functions]

    # Execute functions
    # [graph(df, directory) for graph in valid_graphing_functions]
    # [dataframe(df).to_csv(directory + "/csvs/" + dataframe.__name__ + ".csv") for dataframe in valid_dataframe_functions]
    TEXT = calculate_percent_locations_inactive(df, TEXT, "NETWORK OVERVIEW", "paragraph")
    TEXT = calculate_locations_programs_without_contact(df, TEXT, "PUBLIC CONTACT INFORMATION", "paragraph")
    TEXT = calculate_food_distribution_program_percent(df, TEXT, "PROGRAM TYPES", "paragraph two")
    TEXT = calculate_least_used_programs(df, TEXT, "PROGRAM FILTER FIELDS", "paragraph")

    # Save State
    save_state(TEXT, TEXT_SAVE_NAME.replace('resources/', ''), directory + "/resources")
    save_state(WEIGHTS, WEIGHTS_SAVE_NAME.replace('resources/', ''), directory + "/resources")
    save_state(RECOMMENDED_FILTERS, RECOMMENDED_FILTERS_SAVE_NAME.replace('resources/', ''), directory + "/resources")
    save_state(PROFILE_COMPLETION_TIERS, PROFILE_COMPLETION_TIERS_SAVE_NAME.replace('resources/', ''), directory + "/resources")
