"""
"""


# PACKAGE IMPORTS
from fpdf import FPDF               #
import pandas as pd                 # Pandas, used to represent CSVs and large data sets as a DataFrame.
import argparse, os, shutil         # Argparse, OS, and Shutil, used for File Manipulation and the Command Line Interface
import json                         # JSON, used to parse JSON files and convert to Dictionary data types.
from datetime import date           #
from PIL import Image
import calendar
import glob
import os

# LOCAL FILE IMPORTS
import analyticsEngine as ae        # AnalyticsWizard, used as an API to parse and process the Bulk Upload Data File into small chunks of information.

# IMPORT CONSTANTS
TEXT_SAVE_NAME = "resources/text.json"                                                                          # Path to TEXT save file (JSON).
with open(TEXT_SAVE_NAME) as file: TEXT = json.load(file)                                                       # TEXT, used for all of the text in the PDF report; stored in the file, 'resources/text.json'.
WEIGHTS_SAVE_NAME = "resources/weights.json"                                                                    # Path to WEIGHTS save file (JSON).
with open(WEIGHTS_SAVE_NAME) as file: WEIGHTS = json.load(file)                                                 # WEIGHTS, used for the weightage of each column in the profile completion grades; stored in the file, 'resources/weights.json'.
RECOMMENDED_FILTERS_SAVE_NAME = 'resources/recommended_filters.csv'                                             # Path to Recommended Filters (CSV).
RECOMMENDED_FILTERS = pd.read_csv(RECOMMENDED_FILTERS_SAVE_NAME)                                                # RECOMMENDED_FILTERS, used to store the recommended filters for locations and programs, stored in the file, 'resources/recommended_filters.csv'
PROFILE_COMPLETION_TIERS_SAVE_NAME = 'resources/profile_completion_tiers.csv'                                   # Path to Profile Completion Tiers (CSV).
PROFILE_COMPLETION_TIERS = pd.read_csv(PROFILE_COMPLETION_TIERS_SAVE_NAME)                                      # PROFILE_COMPLETION_TIERS, used to store the profile completion tiers for locations, stored in the file, 'resources/profile_completion_tiers.csv'

# MISC CONSTANTS
PAGE_WIDTH = 8.5                         #
PAGE_HEIGHT = 11                         #

# COLOURS


# STYLES





# PDFCONSTRUCTOR CLASS
class pdfConstructor:
    """
    """
    def __init__(self, new_df: pd.DataFrame(), new_directory: str,new_filename: str,new_network_name: str) -> None:
        """
        """
        # Initialize class variables
        self.df = new_df
        self.directory = new_directory
        self.filename = new_filename
        self.network_name = new_network_name

        # Add network name to TEXT
        TEXT["FILE"]["network name"] = new_network_name
        
        # Create PDF
        self.pdf = FPDF(orientation='P', unit='in', format='letter')
        self.pdf.set_top_margin(1)
        self.pdf.set_auto_page_break(1)
        self.pdf.set_left_margin(1)
        self.pdf.set_right_margin(1)

        # Add font family
        self.pdf.add_font('Roobert Medium', '', fname='resources\Roobert Font Suite\TTF\Roobert-Medium.ttf')
        self.pdf.add_font('Roobert Light Italic', '', fname='resources\Roobert Font Suite\TTF\Roobert-LightItalic.ttf')
        self.pdf.add_font('Roobert Light', '', fname='resources\Roobert Font Suite\TTF\Roobert-Light.ttf')
        self.pdf.add_font('Roobert Regular', '', fname='resources\Roobert Font Suite\TTF\Roobert-Regular.ttf')
        self.pdf.add_font('Roobert Regular', 'B', fname='resources\Roobert Font Suite\TTF\Roobert-SemiBold.ttf')
        self.pdf.add_font('Roobert Regular', 'I', fname='resources\Roobert Font Suite\TTF\Roobert-RegularItalic.ttf')
        self.pdf.add_font('Roobert Bold', '', fname='resources\Roobert Font Suite\TTF\Roobert-Bold.ttf')
        return
    

    def add_cover_page(self) -> None:
        """
        """
        # Add Background Image
        self.pdf.set_top_margin(0)
        self.pdf.set_auto_page_break(0)
        self.pdf.set_left_margin(0)
        self.pdf.set_right_margin(0)
        self.pdf.image("resources\images\cover.png", 0, 0, PAGE_WIDTH, PAGE_HEIGHT)

        # Set Date Font
        self.pdf.set_xy(0.6, 8.5)
        self.pdf.set_text_color(216, 255, 170)
        self.pdf.set_font('Roobert Light', '', 16)

        # Calculate Date
        current_date = date.today().strftime("%m/%d/%Y")
        month = calendar.month_name[int(current_date[0:2])] + " "
        current_date = current_date[3:].replace('/', ', ')
        current_date = month + current_date
        self.pdf.multi_cell(0, self.pdf.font_size + 0.05, current_date, 0, 'L')

        # Add Title
        self.pdf.set_xy(0.5, 8.75)
        self.pdf.set_text_color(216, 255, 170)
        self.pdf.set_font('Roobert Bold', '', 40)
        self.pdf.multi_cell(0, self.pdf.font_size + 0.05, TEXT["FILE"]["network name"] + "\nData Analysis", 0, 'L')

        # Reset Margins
        self.pdf.set_top_margin(1)
        self.pdf.set_auto_page_break(1)
        self.pdf.set_left_margin(1)
        self.pdf.set_right_margin(1)
        return


    def add_page(self) -> None:
        """
        """
        self.pdf.add_page()
        if self.pdf.page_no() > 1:
            self.pdf.set_right_margin(0.5)
            self.pdf.set_y(PAGE_HEIGHT - 0.5)
            self.pdf.set_text_color(0, 72, 61)
            self.pdf.set_font('Roobert Light', '', 10)
            self.pdf.cell(0, 0, '%s' % self.pdf.page_no(), align='R')
            self.pdf.set_y(1)
            self.pdf.set_right_margin(1)
        return
    

    def save_pdf(self) -> None:
        """
        """
        self.pdf.output(self.filename)
        try:
            shutil.move(self.filename, self.directory)
        except OSError:
            os.remove(self.directory + '/' + self.filename)
            shutil.move(self.filename, self.directory)
        return
    

    def add_image(self, filepath: str, height: int, pagenumber: int=-2) -> None:
        """
        """
        real_width, real_height = Image.open(filepath).size
        width = (real_width * height)/real_height

        if pagenumber > -2:
            pagelink = self.pdf.add_link()
            self.pdf.set_link(pagelink, page=pagenumber)
        else:
            pagelink = None
        self.pdf.image(filepath, (PAGE_WIDTH - width)/2, FPDF.get_y(self.pdf), h=height, link=pagelink)
        self.pdf.ln(height)
        return
    

    def add_two_images(self, filepath_one: str, filepath_two: str, height: int, pagenumber_one: int=-2, pagenumber_two: int=-2) -> None:
        """
        """
        real_width, real_height = Image.open(filepath_one).size
        width = (real_width * height)/real_height

        if pagenumber_one > -2:
            pagelink_one = self.pdf.add_link()
            self.pdf.set_link(pagelink_one, page=pagenumber_one)
        else:
            pagelink_one = None
        if pagenumber_two > -2:
            pagelink_two = self.pdf.add_link()
            self.pdf.set_link(pagelink_two, page=pagenumber_two)
        else:
            pagelink_two = None
        current_y = FPDF.get_y(self.pdf)
        self.pdf.image(filepath_one, (PAGE_WIDTH - width*2)/2, current_y, h=height, link=pagelink_one)
        self.pdf.image(filepath_two, ((PAGE_WIDTH - width*2)/2) + width, current_y, h=height, link=pagelink_one)
        self.pdf.ln(height)
        return


    def add_h1_text(self, text: str) -> None:
        """
        """
        self.pdf.set_y(FPDF.get_y(self.pdf))
        if FPDF.get_y(self.pdf) > 1:
            self.pdf.ln(0.5)
        self.pdf.set_text_color(0, 72, 61)
        self.pdf.set_font('Roobert Medium', '', 20)
        self.pdf.cell(0, 0, text, align='C')
        self.pdf.ln(0.3)
        return
    

    def add_normal_text(self, text: str, alignment: str='L') -> None:
        """
        """
        self.pdf.ln(0.10)
        self.pdf.set_y(FPDF.get_y(self.pdf))
        self.pdf.set_text_color(0, 72, 61)
        self.pdf.set_font('Roobert Regular', '', 13)
        self.pdf.multi_cell(6.3, self.pdf.font_size + 0.05, text, align=alignment, markdown=True)
        self.pdf.set_x(1)
        return


    def add_subtitle_text(self, text: str) -> None:
        """
        """
        self.pdf.ln(0.1)
        self.pdf.set_y(FPDF.get_y(self.pdf))
        self.pdf.set_text_color(0, 72, 61)
        self.pdf.set_font('Roobert Light Italic', '', 10)
        self.pdf.multi_cell(6.3, self.pdf.font_size, text, 0, 'C')


    def add_horizontal_line(self) -> None:
        """
        """
        self.pdf.ln(0.05)
        self.pdf.set_draw_color(0, 72, 61)
        self.pdf.set_line_width(0.05)
        self.pdf.line(1, FPDF.get_y(self.pdf), PAGE_WIDTH - 1, FPDF.get_y(self.pdf))
        return


    def add_table(self, function, pagenumber: int=-2) -> None:
        """
        """
        # Create iterable data
        df_copy = self.df.copy()
        df_copy = function(df_copy)
        list_of_lists = df_copy.values

        # Define number of columns
        num_of_columns = len(list(df_copy.columns))

        # Define Page Linker
        if pagenumber > -2:
            pagelink = self.pdf.add_link()
            self.pdf.set_link(pagelink, page=pagenumber)
        else:
            pagelink = None
        
        # Header Row
        self.pdf.set_fill_color(0, 72, 61)
        self.pdf.set_text_color(250, 249, 246)
        self.pdf.set_font('Roobert Regular', 'B', 14)
        for element in list(df_copy.columns):
            self.pdf.cell((PAGE_WIDTH-2)/num_of_columns, self.pdf.font_size + 0.2, element, align='C', fill=True, link=pagelink)
        self.pdf.ln(self.pdf.font_size + 0.2)
        self.pdf.set_x(1)

        # Datum Rows
        self.pdf.set_text_color(0, 72, 61)
        self.pdf.set_font('Roobert Regular', '', 12)
        for row in list_of_lists:
            for datum in row:
                self.pdf.cell((PAGE_WIDTH-2)/num_of_columns, self.pdf.font_size + 0.2, str(datum), align='C', link=pagelink)
            self.pdf.ln(self.pdf.font_size + 0.2)
            self.pdf.set_x(1)
        
        # Save
        df_copy.to_csv(self.directory + "/csvs/" + function.__name__ + ".csv")
        return


    def add_h2_text(self, header_row: list, pagenumber: int=-2, padding=True) -> None:
        """
        """
        # Define number of columns
        columns = len(header_row)

        # Define Page Linker
        if pagenumber > -2:
            pagelink = self.pdf.add_link()
            self.pdf.set_link(pagelink, page=pagenumber)
        else:
            pagelink = None
        
        # Header Row
        self.pdf.set_x(1)
        self.pdf.set_fill_color(0, 72, 61)
        self.pdf.set_text_color(250, 249, 246)
        self.pdf.set_font('Roobert Regular', 'B', 14)
        if len(header_row) == 1:
            self.pdf.multi_cell(PAGE_WIDTH-2, self.pdf.font_size + 0.2, header_row[0], align='C', fill=True, link=pagelink)
        else:
            for element in header_row:
                self.pdf.cell((PAGE_WIDTH-2)/columns, self.pdf.font_size + 0.2, element, align='C', fill=True, link=pagelink)
        if padding:
            self.pdf.ln(self.pdf.font_size + 0.2)
        self.pdf.set_x(1)


    def add_vertical_space(self, height: int) -> None:
        """
        """
        self.pdf.ln(height)
        return




# MAIN
if __name__ == "__main__":
    # Define console parser
    parser = argparse.ArgumentParser(description="Create data visualizations for a Pre-Validated file")
    # Add file argument
    parser.add_argument("file", action="store", help="The file to validate.")
    # Add network name argument
    parser.add_argument("network_name", action="store", help="To name the PDF and customize to the specific Network")
    # Console arguments
    args = parser.parse_args()
    
    # Create directory name
    directory = "data_" + args.file.split("\\")[-1].replace(".csv", "")
    # Create network name
    network_name = args.network_name
    # Create DataFrame
    df = pd.read_csv(args.file)

    # Create directory within project folder
    if not os.path.isdir(directory):
        os.mkdir(directory)
    if not os.path.isdir(directory + "/resources"):
        os.mkdir(directory + "/resources")
    if not os.path.isdir(directory + "/csvs"):
        os.mkdir(directory + "/csvs")
    if not os.path.isdir(directory + "/resources/images"):
        os.mkdir(directory + "/resources/images")
    if not os.path.isdir(directory + "/images"):
        os.mkdir(directory + "/images")
    # Move file to directory
    if args.file.split("\\")[0] != directory:
        shutil.move(args.file, directory)
    # Move resource images to directory
    for image in glob.iglob("resources/images/*png"):
        shutil.copyfile(image, directory + "/resources/images/" + image.split("\\")[1])

    # Create pdfConstructor instance
    constructor = pdfConstructor(df, directory, network_name.replace(" ", "_").lower() + TEXT["FILE"]["filename"], network_name)

    # Cover Page
    constructor.add_page()
    constructor.add_cover_page()

    # Table of Contents
    constructor.add_page()
    constructor.add_h1_text(TEXT["TABLE OF CONTENTS"]["title"])

    # Location Map
    constructor.add_page()
    constructor.add_h1_text(TEXT["LOCATION MAP"]["title"])
    constructor.add_image(ae.create_map(df, directory), 4.2)
    constructor.add_subtitle_text(TEXT["LOCATION MAP"]["subtitle"])
    constructor.add_normal_text(TEXT["LOCATION MAP"]["paragraph"], alignment='C')

    # Network Overview
    constructor.add_h1_text(TEXT["NETWORK OVERVIEW"]["title"])
    constructor.add_table(ae.create_network_overview_table)
    constructor.add_horizontal_line()
    TEXT = ae.calculate_percent_locations_inactive(df, TEXT, "NETWORK OVERVIEW", "paragraph")
    constructor.add_normal_text(TEXT["NETWORK OVERVIEW"]["paragraph"])

    # Profile Completeness
    constructor.add_page()
    constructor.add_h1_text(TEXT["PROFILE COMPLETENESS"]["title"])
    constructor.add_horizontal_line()
    constructor.add_normal_text(TEXT["PROFILE COMPLETENESS"]["paragraph"])
    constructor.add_image(ae.graph_profile_grade(df, directory), 3.75)
    constructor.add_subtitle_text(TEXT["PROFILE COMPLETENESS"]["subtitle"])

    # Highest Lowest Profile Grades
    constructor.add_h1_text(TEXT["HIGH LOW PROFILE GRADES"]["title"])
    constructor.add_h2_text(TEXT["HIGH LOW PROFILE GRADES"]["header row"])
    constructor.add_table(ae.create_high_low_graded_profiles_table)
    constructor.add_horizontal_line()
    constructor.add_normal_text(TEXT["HIGH LOW PROFILE GRADES"]["paragraph"])

    # Vivery Contact Information
    constructor.add_page()
    constructor.add_h1_text(TEXT["VIVERY CONTACT INFORMATION"]["title"])
    constructor.add_horizontal_line()
    constructor.add_normal_text(TEXT["VIVERY CONTACT INFORMATION"]["paragraph"])
    constructor.add_image(ae.graph_missing_organization_contact_info(df, directory), 3.75)

    # Public Contact Information
    constructor.add_h1_text(TEXT["PUBLIC CONTACT INFORMATION"]["title"])
    constructor.add_horizontal_line()
    TEXT = ae.calculate_locations_programs_without_contact(df, TEXT, "PUBLIC CONTACT INFORMATION", "paragraph")
    constructor.add_normal_text(TEXT["PUBLIC CONTACT INFORMATION"]["paragraph"])
    constructor.add_vertical_space(0.075)
    constructor.add_h2_text(TEXT["PUBLIC CONTACT INFORMATION"]["subtitle"], padding=False)
    constructor.add_vertical_space(0.01)
    constructor.add_two_images(ae.graph_missing_location_contact_info(df, directory), ae.graph_missing_program_contact_info(df, directory), 2.25)

    # Program Types
    constructor.add_page()
    constructor.add_h1_text(TEXT["PROGRAM TYPES"]["title"])
    constructor.add_horizontal_line()
    constructor.add_normal_text(TEXT["PROGRAM TYPES"]["paragraph one"])
    constructor.add_image(ae.graph_program_type(df, directory), 3.25)
    constructor.add_horizontal_line()
    constructor.add_vertical_space(0.1)
    TEXT = ae.calculate_food_distribution_program_percent(df, TEXT, "PROGRAM TYPES", "paragraph two")
    constructor.add_normal_text(TEXT["PROGRAM TYPES"]["paragraph two"])
    constructor.add_vertical_space(0.075)
    constructor.add_h2_text(TEXT["PROGRAM TYPES"]["subtitle"], padding=False)
    constructor.add_vertical_space(0.01)
    constructor.add_image(ae.graph_food_program_breakdown(df, directory), 3.25)

    # Filter Fields
    constructor.add_page()
    constructor.add_h1_text(TEXT["PROGRAM FILTER FIELDS"]["title"])
    constructor.add_horizontal_line()
    TEXT = ae.calculate_least_used_programs(df, TEXT, "PROGRAM FILTER FIELDS", "paragraph")
    constructor.add_normal_text(TEXT["PROGRAM FILTER FIELDS"]["paragraph"])
    constructor.add_image(ae.graph_program_filter_usage(df, directory), 3.25)

    # Recommended Filter Options
    constructor.add_h1_text(TEXT["RECOMMENDED FILTER OPTIONS"]["title"])
    constructor.add_horizontal_line()
    constructor.add_normal_text(TEXT["RECOMMENDED FILTER OPTIONS"]["paragraph"])
    constructor.add_vertical_space(0.1)
    constructor.add_table(ae.create_recommended_filters_slice)

    # Network Hours Overview
    constructor.add_page()
    constructor.add_h1_text(TEXT["NETWORK HOURS OVERVIEW"]["title"])
    constructor.add_horizontal_line()
    constructor.add_normal_text(TEXT["NETWORK HOURS OVERVIEW"]["paragraph"])
    constructor.add_image(ae.graph_network_hours_overview(df, directory), 3.25)

    # Network Hour Type Usage
    constructor.add_h1_text(TEXT["NETWORK HOUR TYPE USAGE"]["title"])
    constructor.add_horizontal_line()
    constructor.add_normal_text(TEXT["NETWORK HOUR TYPE USAGE"]["paragraph"])
    constructor.add_vertical_space(0.1)
    constructor.add_table(ae.create_hour_type_usage_table)
    constructor.add_horizontal_line()
    constructor.add_normal_text(TEXT["NETWORK HOUR TYPE USAGE"]["subtext"])

    # Location Hours Preview
    constructor.add_page()
    constructor.add_h1_text(TEXT["LOCATION HOURS PREVIEW"]["title"])
    constructor.add_horizontal_line()
    TEXT = ae.calculate_current_next_month(df, TEXT, "LOCATION HOURS PREVIEW", "paragraph")
    constructor.add_normal_text(TEXT["LOCATION HOURS PREVIEW"]["paragraph"])
    constructor.add_vertical_space(0.1)
    constructor.add_h2_text(TEXT["LOCATION HOURS PREVIEW"]["subtitle"])
    constructor.add_image(ae.graph_sample_location_hours_current_month(df, directory), 3.75)
    constructor.add_image(ae.graph_sample_location_hours_next_month(df, directory), 3.75)

    # Program Hours Preview
    constructor.add_page()
    constructor.add_h1_text(TEXT["PROGRAM HOURS PREVIEW"]["title"])
    constructor.add_h2_text(TEXT["PROGRAM HOURS PREVIEW"]["subtitle"])
    constructor.add_image(ae.graph_sample_program_hours_current_month(df, directory), 3.75)
    constructor.add_image(ae.graph_sample_program_hours_next_month(df, directory), 3.75)
    #

    # Save PDF
    constructor.save_pdf()

    # Save State
    ae.save_state(TEXT, TEXT_SAVE_NAME.replace('resources/', ''), directory + "/resources")
    ae.save_state(WEIGHTS, WEIGHTS_SAVE_NAME.replace('resources/', ''), directory + "/resources")
    ae.save_state(RECOMMENDED_FILTERS, RECOMMENDED_FILTERS_SAVE_NAME.replace('resources/', ''), directory + "/resources")
    ae.save_state(PROFILE_COMPLETION_TIERS, PROFILE_COMPLETION_TIERS_SAVE_NAME.replace('resources/', ''), directory + "/resources")
