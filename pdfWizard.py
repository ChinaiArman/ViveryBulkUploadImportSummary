"""
"""


# PACKAGE IMPORTS
from fpdf import FPDF                   # FPDF, a class containing methods used to create PDFs.
import pandas as pd                     # Pandas, used to represent CSVs and large data sets as a DataFrame.
import argparse, os, glob, shutil       # Argparse, OS, Glob, and Shutil, used for File Manipulation and the Command Line Interface
import json                             # JSON, used to parse JSON files and convert to Dictionary data types.
import math                             # Math, used for basic mathematical operations.
import datetime, calendar               # Datetime and Calendar, used to handle date related tasks and allows python to have access to real world calendar data.
from PIL import Image                   # Image, used to handle varius tasks with Image files like PNGs.

# LOCAL FILE IMPORTS
import analyticsEngine as ae            # AnalyticsEngine, used as an API to parse and process the Bulk Upload Data File into small chunks of information.

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
PAGE_WIDTH = 8.5                                                            # The width of the page in inches.
PAGE_HEIGHT = 11                                                            # The height of the page in inches.
H1_TEXT_SIZE = 20                                                           # The header 1 font size.
H2_TEXT_SIZE = 14                                                           # The header 2 font size.
NORMAL_TEXT_SIZE = 13                                                       # The normal text font size.
SUBTITLE_TEXT_SIZE = 10                                                     # The subtitle text font size.
TABLE_TEXT_SIZE = 10                                                        # The table text font size.
APPENDIX_LINES_PER_PAGE = 25                                                # The number of rows per page for appendix pages.
FIRST_APPENDIX_PAGE = 13                                                    # The first page of the appendix
TABLE_CHAR_PER_CELL = {1: 100, 2: 50, 3: 28, 4: 20, 5: 12, 6: 10}           # A dictionary used to map the number of characters per cell.

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
        self.appendix_page_numbers = {}

        # Appendix Page Numbers
        current_page = FIRST_APPENDIX_PAGE
        self.appendix_page_numbers[TEXT["APPENDIX ORGANIZATION LIST"]["title"]] = current_page
        current_page += max(math.ceil(len(ae.create_organization_table(df).dropna(thresh=2))/APPENDIX_LINES_PER_PAGE), 1)
        self.appendix_page_numbers[TEXT["APPENDIX LOCATION LIST"]["title"]] = current_page
        current_page += max(math.ceil(len(ae.create_location_table(df).dropna(thresh=2))/APPENDIX_LINES_PER_PAGE), 1)
        self.appendix_page_numbers[TEXT["APPENDIX PROGRAM LIST"]["title"]] = current_page
        current_page += max(math.ceil(len(ae.create_program_table(df).dropna(thresh=2))/APPENDIX_LINES_PER_PAGE), 1)
        self.appendix_page_numbers[TEXT["APPENDIX PROGRAM PROFILE COMPLETION LIST"]["title"]] = current_page
        current_page += max(math.ceil(len(ae.create_program_profile_completion_table(df).dropna(thresh=2))/APPENDIX_LINES_PER_PAGE), 1)
        self.appendix_page_numbers[TEXT["APPENDIX ORGANIZATION CONTACT INFORMATION"]["title"]] = current_page
        current_page += max(math.ceil(len(ae.create_organization_contact_information_table(df).dropna(thresh=2))/APPENDIX_LINES_PER_PAGE), 1)
        self.appendix_page_numbers[TEXT["APPENDIX LOCATION CONTACT INFORMATION"]["title"]] = current_page
        current_page += max(math.ceil(len(ae.create_location_contact_information_table(df).dropna(thresh=2))/APPENDIX_LINES_PER_PAGE), 1)
        self.appendix_page_numbers[TEXT["APPENDIX PROGRAM CONTACT INFORMATION"]["title"]] = current_page
        current_page += max(math.ceil(len(ae.create_program_contact_information_table(df).dropna(thresh=2))/APPENDIX_LINES_PER_PAGE), 1)
        self.appendix_page_numbers[TEXT["APPENDIX PROGRAM TYPE"]["title"]] = current_page
        current_page += max(math.ceil(len(ae.create_program_by_program_type_table(df).dropna(thresh=2))/APPENDIX_LINES_PER_PAGE), 1)
        self.appendix_page_numbers[TEXT["APPENDIX PROGRAM AUDIENCE"]["title"]] = current_page
        current_page += max(math.ceil(len(ae.create_program_by_program_audience_table(df).dropna(thresh=2))/APPENDIX_LINES_PER_PAGE), 1)
        self.appendix_page_numbers[TEXT["APPENDIX PROGRAM LANGUAGES SPOKEN"]["title"]] = current_page
        current_page += max(math.ceil(len(ae.create_program_by_program_languages_spoken_table(df).dropna(thresh=2))/APPENDIX_LINES_PER_PAGE), 1)
        self.appendix_page_numbers[TEXT["APPENDIX PROGRAM FEATURES"]["title"]] = current_page
        current_page += max(math.ceil(len(ae.create_program_by_program_features_table(df).dropna(thresh=2))/APPENDIX_LINES_PER_PAGE), 1)
        self.appendix_page_numbers[TEXT["APPENDIX PROGRAM ITEMS OFFERED"]["title"]] = current_page
        current_page += max(math.ceil(len(ae.create_program_by_program_items_offered_table(df).dropna(thresh=2))/APPENDIX_LINES_PER_PAGE), 1)
        self.appendix_page_numbers[TEXT["APPENDIX PROGRAM DIETARY OPTIONS"]["title"]] = current_page
        current_page += max(math.ceil(len(ae.create_program_by_program_dietary_options_table(df).dropna(thresh=2))/APPENDIX_LINES_PER_PAGE), 1)
        self.appendix_page_numbers[TEXT["APPENDIX PROGRAM FILTERS AVAILABLE"]["title"]] = current_page
        current_page += max(math.ceil(len(ae.create_recommended_program_filters_table(df).dropna(thresh=2))/APPENDIX_LINES_PER_PAGE), 1)
        self.appendix_page_numbers[TEXT["APPENDIX LOCATION HOURS INFORMATION"]["title"]] = current_page
        current_page += max(math.ceil(len(ae.create_location_hours_table(df).dropna(thresh=2))/APPENDIX_LINES_PER_PAGE), 1)
        self.appendix_page_numbers[TEXT["APPENDIX PROGRAM HOURS INFORMATION"]["title"]] = current_page
        current_page += max(math.ceil(len(ae.create_program_hours_table(df).dropna(thresh=2))/APPENDIX_LINES_PER_PAGE), 1)
        self.appendix_page_numbers[TEXT["APPENDIX PROGRAM QUALIFICATIONS"]["title"]] = current_page
        current_page += max(math.ceil(len(ae.create_program_by_program_qualifications_table(df).dropna(thresh=2))/APPENDIX_LINES_PER_PAGE), 1)
        self.appendix_page_numbers[TEXT["APPENDIX PROGRAM SERVICE AREAS"]["title"]] = current_page
        current_page += max(math.ceil(len(ae.create_program_by_program_service_area_table(df).dropna(thresh=2))/APPENDIX_LINES_PER_PAGE), 1)

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
        self.pdf.add_font('Roobert Bold', '', fname='resources\Roobert Font Suite\TTF\Roobert-Bold.ttf')
        return
    

    def add_cover_page(self) -> None:
        """
        Adds a cover page to the PDF document.

        This method adds a background image, sets the date and title on the cover page of the PDF.

        Args:
            None

        Preconditions:
            - The method should be called after initializing the PDF document using the `pdfConstructor` class.
            - The resources folder should contain the necessary `cover.png` image.

        Raises:
            None

        Returns:
            None. The cover page is added to the PDF document.

        Example:
            >>> pdf = pdfConstructor()
            >>> pdf.add_cover_page()
            # The cover page is added to the PDF document.

        Additional Information:
            - The method sets the top, left, and right margins of the PDF to zero to position the background image.
            - The method sets the date font and calculates the current date in the format `MM DD, YYYY`.
            - The method sets the title font and retrieves the `network name` from the TEXT dictionary.
            - The title and date are added using `multi_cell` method for multiline display.
            - The top, left, and right margins are reset to their default values after adding the cover page.
            - No value is returned.
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
        current_date = datetime.date.today().strftime("%m/%d/%Y")
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


    def add_back_cover(self) -> None:
        """
        Adds a back cover page to the PDF document.

        This method adds a vertical space and a back cover image to the PDF document.

        Args:
            None

        Preconditions:
            - The method should be called after adding all the content to the PDF.
            - The resources folder should contain the necessary `back_cover.png` image.

        Raises:
            None

        Returns:
            None. The back cover page is added to the PDF document.

        Example:
            >>> pdf = pdfConstructor()
            >>> pdf.add_back_cover()
            # The back cover page is added to the PDF document.

        Additional Information:
            - The method calls the `add_vertical_space` method to create vertical spacing on the page.
            - The method adds the back cover image using the `add_image` method.
            - No value is returned.
        """
        # Set Vertical Height
        self.add_vertical_space(3.5)

        # Add back cover image
        self.add_image("resources\images\\back_cover.png", 2)
        return


    def add_page(self) -> None:
        """
        Adds a new page to the PDF document.

        This method adds a new page to the PDF document. If there are already existing pages,
        it also adds a footer to display the current page number.

        Args:
            None

        Preconditions:
            - The `pdf` attribute must be properly configured with content for the PDF.
            - The `page_no` attribute keeps track of the current page number.

        Raises:
            None

        Returns:
            None. A new page is added to the PDF document, and the footer with the current page number is displayed.

        Example:
            >>> pdf = pdfConstructor()
            >>> pdf.add_cover_page()
            # Add content to the PDF using other methods...
            >>> pdf.add_page()
            # A new page is added to the PDF document, and the footer with the current page number is displayed.

        Additional Information:
            - The method uses the `add_page` method of the `pdf` attribute to add a new page.
            - It then checks if the current page number (`page_no`) is greater than 1 (indicating there are already existing pages).
            - If there are existing pages, it sets the right margin to add a footer displaying the current page number.
            - The method uses the `cell` method of the `pdf` attribute to create the footer and display the page number.
            - Finally, the method resets the right margin and returns.
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
        Saves the PDF document to the specified directory.

        This method saves the PDF document to the directory specified during object initialization.
        If the file already exists in the directory, it will be replaced.

        Args:
            None

        Preconditions:
            - The `pdf` attribute must be properly configured with all the content to be included in the PDF.
            - The `filename` attribute must be set to a valid name for the PDF file.
            - The `directory` attribute must be set to a valid path to an existing directory.

        Raises:
            None

        Returns:
            None. The PDF document is saved to the specified directory.

        Example:
            >>> pdf = pdfConstructor()
            >>> pdf.add_cover_page()
            # Add content to the PDF using other methods...
            >>> pdf.save_pdf()
            # The PDF document is saved to the specified directory.

        Additional Information:
            - The method uses the `output` method of the `pdf` attribute to save the PDF.
            - It then attempts to move the saved PDF to the specified directory using `shutil.move`.
            - If an `OSError` occurs during the move (e.g., the file already exists in the directory), it deletes the existing file and moves the new PDF again.
            - No value is returned.
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
        Adds an image to the PDF document.

        This method adds an image to the PDF document using the provided file path and height. It automatically calculates
        the appropriate width to maintain the image's aspect ratio.

        Args:
            filepath (str): The file path to the image that needs to be added to the PDF.
            height (int): The desired height of the image in points (1/72 inch).
            pagenumber (int, optional): The page number to link the image to. Defaults to -2.

        Preconditions:
            - The `pdf` attribute must be properly configured with content for the PDF.
            - The `PAGE_WIDTH` attribute represents the width of the PDF page.
            - The `FPDF.get_y()` method returns the current Y position in the PDF document.
            - The `height` argument must be a positive integer representing the desired image height in points.
            - The `filepath` must be a valid path to an existing image file.

        Raises:
            None

        Returns:
            None. The image is added to the PDF document with the specified height.

        Example:
            >>> pdf = pdfConstructor()
            >>> pdf.add_cover_page()
            # Add content to the PDF using other methods...
            >>> pdf.add_image("resources/images/image.png", 200)
            # Adds the image located at "resources/images/image.png" to the PDF document with a height of 200 points.

        Additional Information:
            - The method uses the Python Imaging Library (PIL) to get the real width and height of the image.
            - It calculates the appropriate width to maintain the image's aspect ratio based on the provided height.
            - If the `pagenumber` argument is given, the method creates a link for the image to the specified page.
            - The `add_link()` method of the `pdf` attribute is used to create the link.
            - The image is then added to the PDF using the `image` method of the `pdf` attribute, and the link is attached.
            - Finally, the `ln()` method of the `pdf` attribute is used to move the cursor to the next line after the image.
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
        Adds two images side by side to the PDF document.

        This method adds two images to the PDF document side by side using the provided file paths and height. It automatically
        calculates the appropriate width to maintain the images' aspect ratios.

        Args:
            filepath_one (str): The file path to the first image that needs to be added to the PDF.
            filepath_two (str): The file path to the second image that needs to be added to the PDF.
            height (int): The desired height of the images in points (1/72 inch).
            pagenumber_one (int, optional): The page number to link the first image to. Defaults to -2.
            pagenumber_two (int, optional): The page number to link the second image to. Defaults to -2.

        Preconditions:
            - The `pdf` attribute must be properly configured with content for the PDF.
            - The `PAGE_WIDTH` attribute represents the width of the PDF page.
            - The `FPDF.get_y()` method returns the current Y position in the PDF document.
            - The `height` argument must be a positive integer representing the desired image height in points.
            - The `filepath_one` and `filepath_two` must be valid paths to existing image files.

        Raises:
            None

        Returns:
            None. The two images are added side by side to the PDF document with the specified height.

        Example:
            >>> pdf = pdfConstructor()
            >>> pdf.add_cover_page()
            # Add content to the PDF using other methods...
            >>> pdf.add_two_images("resources/images/image1.png", "resources/images/image2.png", 200)
            # Adds the images located at "resources/images/image1.png" and "resources/images/image2.png"
            # side by side to the PDF document with a height of 200 points.

        Additional Information:
            - The method uses the Python Imaging Library (PIL) to get the real width and height of the images.
            - It calculates the appropriate width to maintain the images' aspect ratios based on the provided height.
            - If the `pagenumber_one` and/or `pagenumber_two` arguments are given, the method creates links for the images to the specified pages.
            - The `add_link()` method of the `pdf` attribute is used to create the links.
            - The images are then added to the PDF using the `image` method of the `pdf` attribute, and the links are attached.
            - Finally, the `ln()` method of the `pdf` attribute is used to move the cursor to the next line after the images.
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
        self.pdf.image(filepath_two, ((PAGE_WIDTH - width*2)/2) + width, current_y, h=height, link=pagelink_two)
        self.pdf.ln(height)
        return


    def add_h1_text(self, text: str) -> None:
        """
        Adds an H1 heading to the PDF document.

        This method adds an H1 heading to the PDF document using the provided text. The H1 heading is centered,
        colored with custom color (0, 72, 61), and set in a specific font and size.

        Args:
            text (str): The text content of the H1 heading to be added.

        Preconditions:
            - The `pdf` attribute must be properly configured with content for the PDF.
            - The `FPDF.get_y()` method returns the current Y position in the PDF document.
            - The `H1_TEXT_SIZE` constant represents the font size for the H1 heading.
            - The `text` argument must be a non-empty string containing the content of the H1 heading.

        Raises:
            None

        Returns:
            None. The H1 heading with the specified text is added to the PDF document.

        Example:
            >>> pdf = pdfConstructor()
            >>> pdf.add_cover_page()
            # Add content to the PDF using other methods...
            >>> pdf.add_h1_text("Introduction")
            # Adds an H1 heading with the text "Introduction" to the PDF document.

        Additional Information:
            - The method uses the `FPDF.get_y()` method to get the current Y position in the PDF document and adjust the positioning accordingly.
            - If the current Y position is greater than 1, a line break of 0.5 is added before the H1 heading to create space.
            - The `set_text_color()` method of the `pdf` attribute is used to set the color of the H1 heading.
            - The `set_font()` method of the `pdf` attribute is used to set the font family and size for the H1 heading.
            - The `cell()` method of the `pdf` attribute is used to add the H1 heading with the provided text, centered horizontally.
            - After adding the H1 heading, a line break of 0.3 is added to create space between the heading and subsequent content.
        """
        self.pdf.set_y(FPDF.get_y(self.pdf))
        if FPDF.get_y(self.pdf) > 1:
            self.pdf.ln(0.5)
        self.pdf.set_text_color(0, 72, 61)
        self.pdf.set_font('Roobert Medium', '', H1_TEXT_SIZE)
        self.pdf.cell(0, 0, text, align='C')
        self.pdf.ln(0.3)
        return
    

    def add_normal_text(self, text: str, alignment: str='L', pagenumber: int=-2) -> None:
        """
        Adds normal text to the PDF document.

        This method adds normal text to the PDF document using the provided text content and optional alignment.
        The text is set in a specific font and size, and can be aligned to the left (default), right, center, or justified.

        Args:
            text (str): The text content to be added to the PDF.
            alignment (str, optional): The alignment of the text. Possible values are 'L' for left (default),
                                       'R' for right, 'C' for center, and 'J' for justified.
            pagenumber (int, optional): The page number to link the text to (default is -2, no link).

        Preconditions:
            - The `pdf` attribute must be properly configured with content for the PDF.
            - The `FPDF.get_y()` method returns the current Y position in the PDF document.
            - The `NORMAL_TEXT_SIZE` constant represents the font size for normal text.
            - The `text` argument must be a non-empty string containing the content to be added.
            - The `alignment` argument, if provided, must be one of the valid alignment values.

        Raises:
            None

        Returns:
            None. The normal text with the specified content and alignment is added to the PDF document.

        Example:
            >>> pdf = pdfConstructor()
            >>> pdf.add_cover_page()
            # Add content to the PDF using other methods...
            >>> pdf.add_normal_text("This is a sample paragraph.")
            # Adds normal text with the content "This is a sample paragraph." aligned to the left.

        Additional Information:
            - The method uses the `FPDF.get_y()` method to get the current Y position in the PDF document and adjust the positioning accordingly.
            - The method sets the text color, font family, and size for the normal text using the `set_text_color()` and `set_font()` methods of the `pdf` attribute.
            - The `multi_cell()` method of the `pdf` attribute is used to add the normal text with the provided content, size, and alignment.
            - If the `pagenumber` argument is provided and greater than -2, a link is added to the text that jumps to the specified page number when clicked.
            - The `markdown` parameter of the `multi_cell()` method is set to True to enable text formatting using Markdown syntax.
            - After adding the text, the X position is reset to 1 to maintain the left margin for subsequent content.
        """
        # Define Page Linker
        if pagenumber > -2:
            pagelink = self.pdf.add_link()
            self.pdf.set_link(pagelink, page=pagenumber)
        else:
            pagelink = None
        self.pdf.ln(0.10)
        self.pdf.set_y(FPDF.get_y(self.pdf))
        self.pdf.set_text_color(0, 72, 61)
        self.pdf.set_font('Roobert Regular', '', NORMAL_TEXT_SIZE)
        self.pdf.multi_cell(6.3, self.pdf.font_size + 0.05, text, align=alignment, markdown=True, link=pagelink)
        self.pdf.set_x(1)
        return


    def add_subtitle_text(self, text: str, pagenumber: int=-2) -> None:
        """
        Adds subtitle text to the PDF document.

        This method adds subtitle text to the PDF document using the provided text content and optional page link.
        The text is set in a specific font and size, and is centered horizontally in the document.

        Args:
            text (str): The subtitle text content to be added to the PDF.
            pagenumber (int, optional): The page number to link the text to (default is -2, no link).

        Preconditions:
            - The `pdf` attribute must be properly configured with content for the PDF.
            - The `FPDF.get_y()` method returns the current Y position in the PDF document.
            - The `SUBTITLE_TEXT_SIZE` constant represents the font size for subtitle text.
            - The `text` argument must be a non-empty string containing the subtitle content.
            - The `pagenumber` argument, if provided, must be greater than -2.

        Raises:
            None

        Returns:
            None. The subtitle text with the specified content is added to the PDF document.

        Example:
            >>> pdf = pdfConstructor()
            >>> pdf.add_cover_page()
            # Add content to the PDF using other methods...
            >>> pdf.add_subtitle_text("Subtitle")
            # Adds subtitle text with the content "Subtitle" centered horizontally.

        Additional Information:
            - The method uses the `FPDF.get_y()` method to get the current Y position in the PDF document and adjust the positioning accordingly.
            - The method sets the text color, font family, and size for the subtitle text using the `set_text_color()` and `set_font()` methods of the `pdf` attribute.
            - The `multi_cell()` method of the `pdf` attribute is used to add the subtitle text with the provided content, size, and center alignment.
            - If the `pagenumber` argument is provided and greater than -2, a link is added to the text that jumps to the specified page number when clicked.
            - After adding the subtitle text, the current Y position is adjusted to create spacing for subsequent content.
        """
        if pagenumber > -2:
            pagelink = self.pdf.add_link()
            self.pdf.set_link(pagelink, page=pagenumber)
        else:
            pagelink = None
        self.pdf.ln(0.1)
        self.pdf.set_y(FPDF.get_y(self.pdf))
        self.pdf.set_text_color(0, 72, 61)
        self.pdf.set_font('Roobert Light Italic', '', SUBTITLE_TEXT_SIZE)
        self.pdf.multi_cell(6.3, self.pdf.font_size, text, 0, 'C', link=pagelink)
        return


    def add_horizontal_line(self) -> None:
        """
        Adds a horizontal line to the PDF document.

        This method adds a horizontal line to the PDF document, extending across the full width of the page.
        The line is drawn with a specific color and width.

        Preconditions:
            - The `pdf` attribute must be properly configured with content for the PDF.
            - The `FPDF.get_y()` method returns the current Y position in the PDF document.

        Raises:
            None

        Returns:
            None. The horizontal line is added to the PDF document.

        Example:
            >>> pdf = pdfConstructor()
            >>> pdf.add_cover_page()
            # Add content to the PDF using other methods...
            >>> pdf.add_horizontal_line()
            # Adds a horizontal line to the PDF, extending across the full width of the page.

        Additional Information:
            - The method uses the `FPDF.get_y()` method to get the current Y position in the PDF document.
            - The `set_draw_color()` method of the `pdf` attribute is used to set the color of the line.
            - The `set_line_width()` method of the `pdf` attribute is used to set the width of the line.
            - The `line()` method of the `pdf` attribute is used to draw the horizontal line across the page.
            - After adding the horizontal line, the current Y position is adjusted to create spacing for subsequent content.
        """
        self.pdf.ln(0.05)
        self.pdf.set_draw_color(0, 72, 61)
        self.pdf.set_line_width(0.05)
        self.pdf.line(1, FPDF.get_y(self.pdf), PAGE_WIDTH - 1, FPDF.get_y(self.pdf))
        return


    def add_table(self, function) -> None:
        """
        """
        # Create iterable data
        df_copy = self.df.copy()
        df_copy = function(df_copy)
        list_of_lists = df_copy.values

        # Define number of columns
        num_of_columns = len(list(df_copy.columns))
        char_limit = TABLE_CHAR_PER_CELL[num_of_columns]
        
        # Header Row
        self.pdf.set_fill_color(0, 72, 61)
        self.pdf.set_text_color(250, 249, 246)
        self.pdf.set_font('Roobert Regular', 'B', H2_TEXT_SIZE)
        for element in list(df_copy.columns):
            self.pdf.cell((PAGE_WIDTH-2)/num_of_columns, self.pdf.font_size + 0.2, element, align='C', fill=True)
        self.pdf.ln(self.pdf.font_size + 0.2)
        self.pdf.set_x(1)

        # Datum Rows
        self.pdf.set_text_color(0, 72, 61)
        self.pdf.set_font('Roobert Regular', '', TABLE_TEXT_SIZE)
        for row in list_of_lists:
            for datum in row:
                if str(datum) == "nan":
                    datum = "null"
                if len(str(datum)) > char_limit:
                    self.pdf.cell((PAGE_WIDTH-2)/num_of_columns, self.pdf.font_size + 0.2, str(datum)[:char_limit] + "...", align='C')
                else:
                    self.pdf.cell((PAGE_WIDTH-2)/num_of_columns, self.pdf.font_size + 0.2, str(datum), align='C')
            self.pdf.ln(self.pdf.font_size + 0.2)
            self.pdf.set_x(1)
        
        # Save
        df_copy.to_csv(self.directory + "/csvs/" + function.__name__ + ".csv")
        return


    def add_appendix(self, function, title: str) -> None:
        """
        """
        # Create iterable data
        df_copy = self.df.copy()
        df_copy = function(df_copy)
        df_copy = df_copy.dropna(thresh=2)
        list_of_lists = df_copy.values

        # Catch NaN Tables
        if len(list_of_lists) == 0:
            self.add_h1_text(title)
            self.add_h2_text(df_copy.columns)
            self.add_vertical_space(0.25)
            self.add_normal_text("All values NaN", alignment='C')
            self.add_page()
            return

        # Define number of columns
        num_of_columns = len(list(df_copy.columns))
        char_limit = TABLE_CHAR_PER_CELL[num_of_columns]
        
        # Header Row
        for i in range(math.ceil(len(list_of_lists)/APPENDIX_LINES_PER_PAGE)):
            self.add_h1_text(title)
            self.pdf.set_fill_color(0, 72, 61)
            self.pdf.set_text_color(250, 249, 246)
            self.pdf.set_font('Roobert Regular', 'B', H2_TEXT_SIZE)
            for element in list(df_copy.columns):
                self.pdf.cell((PAGE_WIDTH-2)/num_of_columns, self.pdf.font_size + 0.2, element, align='C', fill=True)
            self.pdf.ln(self.pdf.font_size + 0.2)
            self.pdf.set_x(1)

            # Datum Rows
            self.pdf.set_text_color(0, 72, 61)
            self.pdf.set_font('Roobert Regular', '', TABLE_TEXT_SIZE)
            for row in list_of_lists[i*APPENDIX_LINES_PER_PAGE:(i+1)*APPENDIX_LINES_PER_PAGE]:
                for datum in row:
                    if str(datum) == "nan":
                        datum = ""
                    if len(str(datum)) > char_limit:
                        self.pdf.cell((PAGE_WIDTH-2)/num_of_columns, self.pdf.font_size + 0.2, str(datum)[:char_limit] + "...", align='C')
                    else:
                        self.pdf.cell((PAGE_WIDTH-2)/num_of_columns, self.pdf.font_size + 0.2, str(datum), align='C')
                self.pdf.ln(self.pdf.font_size + 0.2)
                self.pdf.set_x(1)
            self.add_page()
        
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
        self.pdf.set_font('Roobert Regular', 'B', H2_TEXT_SIZE)
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
    constructor.add_image(ae.create_map(df, directory), 4.2, pagenumber=constructor.appendix_page_numbers[TEXT["APPENDIX LOCATION LIST"]["title"]])
    constructor.add_subtitle_text(TEXT["LOCATION MAP"]["subtitle"])
    constructor.add_normal_text(TEXT["LOCATION MAP"]["paragraph"], alignment='C')

    # Network Overview
    constructor.add_h1_text(TEXT["NETWORK OVERVIEW"]["title"])
    constructor.add_table(ae.create_network_overview_table)
    constructor.add_horizontal_line()
    TEXT = ae.calculate_percent_locations_inactive(df, TEXT, "NETWORK OVERVIEW", "paragraph")
    constructor.add_normal_text(TEXT["NETWORK OVERVIEW"]["paragraph"], pagenumber=constructor.appendix_page_numbers[TEXT["APPENDIX LOCATION LIST"]["title"]])

    # Profile Completeness
    constructor.add_page()
    constructor.add_h1_text(TEXT["PROFILE COMPLETENESS"]["title"])
    constructor.add_horizontal_line()
    constructor.add_normal_text(TEXT["PROFILE COMPLETENESS"]["paragraph"])
    constructor.add_image(ae.graph_profile_grade(df, directory), 3.75, pagenumber=constructor.appendix_page_numbers[TEXT["APPENDIX PROGRAM PROFILE COMPLETION LIST"]["title"]])
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
    constructor.add_image(ae.graph_missing_organization_contact_info(df, directory), 3.75, pagenumber=constructor.appendix_page_numbers[TEXT["APPENDIX ORGANIZATION CONTACT INFORMATION"]["title"]])

    # Public Contact Information
    constructor.add_h1_text(TEXT["PUBLIC CONTACT INFORMATION"]["title"])
    constructor.add_horizontal_line()
    TEXT = ae.calculate_locations_programs_without_contact(df, TEXT, "PUBLIC CONTACT INFORMATION", "paragraph")
    constructor.add_normal_text(TEXT["PUBLIC CONTACT INFORMATION"]["paragraph"])
    constructor.add_vertical_space(0.075)
    constructor.add_h2_text(TEXT["PUBLIC CONTACT INFORMATION"]["subtitle"], padding=False)
    constructor.add_vertical_space(0.01)
    constructor.add_two_images(ae.graph_missing_location_contact_info(df, directory), ae.graph_missing_program_contact_info(df, directory), 2.25, pagenumber_one=constructor.appendix_page_numbers[TEXT["APPENDIX LOCATION CONTACT INFORMATION"]["title"]], pagenumber_two=constructor.appendix_page_numbers[TEXT["APPENDIX PROGRAM CONTACT INFORMATION"]["title"]])

    # Program Types
    constructor.add_page()
    constructor.add_h1_text(TEXT["PROGRAM TYPES"]["title"])
    constructor.add_horizontal_line()
    constructor.add_normal_text(TEXT["PROGRAM TYPES"]["paragraph one"])
    constructor.add_image(ae.graph_program_type(df, directory), 3.25, pagenumber=constructor.appendix_page_numbers[TEXT["APPENDIX PROGRAM TYPE"]["title"]])
    constructor.add_horizontal_line()
    constructor.add_vertical_space(0.1)
    TEXT = ae.calculate_food_distribution_program_percent(df, TEXT, "PROGRAM TYPES", "paragraph two")
    constructor.add_normal_text(TEXT["PROGRAM TYPES"]["paragraph two"])
    constructor.add_vertical_space(0.075)
    constructor.add_h2_text(TEXT["PROGRAM TYPES"]["subtitle"], padding=False)
    constructor.add_vertical_space(0.01)
    constructor.add_image(ae.graph_food_program_breakdown(df, directory), 3.25, pagenumber=constructor.appendix_page_numbers[TEXT["APPENDIX PROGRAM TYPE"]["title"]])

    # Filter Fields
    constructor.add_page()
    constructor.add_h1_text(TEXT["PROGRAM FILTER FIELDS"]["title"])
    constructor.add_horizontal_line()
    TEXT = ae.calculate_least_used_programs(df, TEXT, "PROGRAM FILTER FIELDS", "paragraph")
    constructor.add_normal_text(TEXT["PROGRAM FILTER FIELDS"]["paragraph"])
    constructor.add_image(ae.graph_program_filter_usage(df, directory), 3.75, pagenumber=constructor.appendix_page_numbers[TEXT["APPENDIX PROGRAM AUDIENCE"]["title"]])

    # Recommended Filter Options
    constructor.add_h1_text(TEXT["RECOMMENDED FILTER OPTIONS"]["title"])
    constructor.add_horizontal_line()
    constructor.add_normal_text(TEXT["RECOMMENDED FILTER OPTIONS"]["paragraph"], pagenumber=constructor.appendix_page_numbers[TEXT["APPENDIX PROGRAM FILTERS AVAILABLE"]["title"]])
    constructor.add_vertical_space(0.1)
    constructor.add_table(ae.create_recommended_filters_slice)

    # Network Hours Overview
    constructor.add_page()
    constructor.add_h1_text(TEXT["NETWORK HOURS OVERVIEW"]["title"])
    constructor.add_horizontal_line()
    constructor.add_normal_text(TEXT["NETWORK HOURS OVERVIEW"]["paragraph"])
    constructor.add_image(ae.graph_network_hours_overview(df, directory), 3.25, pagenumber=constructor.appendix_page_numbers[TEXT["APPENDIX LOCATION HOURS INFORMATION"]["title"]])

    # Network Hour Type Usage
    constructor.add_h1_text(TEXT["NETWORK HOUR TYPE USAGE"]["title"])
    constructor.add_horizontal_line()
    constructor.add_normal_text(TEXT["NETWORK HOUR TYPE USAGE"]["paragraph"], pagenumber=constructor.appendix_page_numbers[TEXT["APPENDIX LOCATION HOURS INFORMATION"]["title"]])
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
    constructor.add_image(ae.graph_sample_location_hours_current_month(df, directory), 3.65, pagenumber=constructor.appendix_page_numbers[TEXT["APPENDIX LOCATION HOURS INFORMATION"]["title"]])
    constructor.add_image(ae.graph_sample_location_hours_next_month(df, directory), 3.65, pagenumber=constructor.appendix_page_numbers[TEXT["APPENDIX LOCATION HOURS INFORMATION"]["title"]])

    # Program Hours Preview
    constructor.add_page()
    constructor.add_h1_text(TEXT["PROGRAM HOURS PREVIEW"]["title"])
    constructor.add_h2_text(TEXT["PROGRAM HOURS PREVIEW"]["subtitle"])
    constructor.add_image(ae.graph_sample_program_hours_current_month(df, directory), 3.65, pagenumber=constructor.appendix_page_numbers[TEXT["APPENDIX PROGRAM HOURS INFORMATION"]["title"]])
    constructor.add_image(ae.graph_sample_program_hours_next_month(df, directory), 3.65, pagenumber=constructor.appendix_page_numbers[TEXT["APPENDIX PROGRAM HOURS INFORMATION"]["title"]])
    constructor.add_horizontal_line()
    constructor.add_normal_text(TEXT["PROGRAM HOURS PREVIEW"]["paragraph"])

    # Missing Program Qualifications
    constructor.add_page()
    constructor.add_h1_text(TEXT["MISSING PROGRAM QUALIFICATIONS"]["title"])
    constructor.add_horizontal_line()
    constructor.add_normal_text(TEXT["MISSING PROGRAM QUALIFICATIONS"]["paragraph"])
    constructor.add_image(ae.graph_program_qualifications(df, directory), 3.15, pagenumber=constructor.appendix_page_numbers[TEXT["APPENDIX PROGRAM QUALIFICATIONS"]["title"]])

    # Missing Program Service Areas
    constructor.add_h1_text(TEXT["MISSING PROGRAM SERVICE AREA"]["title"])
    constructor.add_horizontal_line()
    constructor.add_normal_text(TEXT["MISSING PROGRAM SERVICE AREA"]["paragraph"])
    constructor.add_image(ae.graph_program_service_areas(df, directory), 3.15, pagenumber=constructor.appendix_page_numbers[TEXT["APPENDIX PROGRAM SERVICE AREAS"]["title"]])

    # Page Break
    constructor.add_page()
    constructor.add_vertical_space(4)
    constructor.add_normal_text("THIS PAGE INTENTIONALLY LEFT BLANK", alignment='C')

    # APPENDIX ORGANIZATION LIST
    constructor.add_page()
    constructor.add_appendix(ae.create_organization_table, TEXT["APPENDIX ORGANIZATION LIST"]["title"])

    # APPENDIX LOCATION LIST
    constructor.add_appendix(ae.create_location_table, TEXT["APPENDIX LOCATION LIST"]["title"])

    # APPENDIX PROGRAM LIST
    constructor.add_appendix(ae.create_program_table, TEXT["APPENDIX PROGRAM LIST"]["title"])

    # APPENDIX PROGRAM PROFILE COMPLETION LIST
    constructor.add_appendix(ae.create_program_profile_completion_table, TEXT["APPENDIX PROGRAM PROFILE COMPLETION LIST"]["title"])

    # APPENDIX ORGANIZATION CONTACT INFORMATION
    constructor.add_appendix(ae.create_organization_contact_information_table, TEXT["APPENDIX ORGANIZATION CONTACT INFORMATION"]["title"])

    # APPENDIX LOCATION CONTACT INFORMATION
    constructor.add_appendix(ae.create_location_contact_information_table, TEXT["APPENDIX LOCATION CONTACT INFORMATION"]["title"])
    
    # APPENDIX PROGRAM CONTACT INFORMATION
    constructor.add_appendix(ae.create_program_contact_information_table, TEXT["APPENDIX PROGRAM CONTACT INFORMATION"]["title"])

    # APPENDIX PROGRAM TYPE
    constructor.add_appendix(ae.create_program_by_program_type_table, TEXT["APPENDIX PROGRAM TYPE"]["title"])

    # APPENDIX PROGRAM AUDIENCE
    constructor.add_appendix(ae.create_program_by_program_audience_table, TEXT["APPENDIX PROGRAM AUDIENCE"]["title"])

    # APPENDIX PROGRAM LANGUAGES SPOKEN
    constructor.add_appendix(ae.create_program_by_program_languages_spoken_table, TEXT["APPENDIX PROGRAM LANGUAGES SPOKEN"]["title"])

    # APPENDIX PROGRAM FEATURES
    constructor.add_appendix(ae.create_program_by_program_features_table, TEXT["APPENDIX PROGRAM FEATURES"]["title"])

    # APPENDIX PROGRAM ITEMS OFFERED
    constructor.add_appendix(ae.create_program_by_program_items_offered_table, TEXT["APPENDIX PROGRAM ITEMS OFFERED"]["title"])

    # APPENDIX PROGRAM DIETARY OPTIONS
    constructor.add_appendix(ae.create_program_by_program_dietary_options_table, TEXT["APPENDIX PROGRAM DIETARY OPTIONS"]["title"])

    # APPENDIX PROGRAM FILTERS AVAILABLE
    constructor.add_appendix(ae.create_recommended_program_filters_table, TEXT["APPENDIX PROGRAM FILTERS AVAILABLE"]["title"])

    # APPENDIX LOCATION HOURS INFORMATION
    constructor.add_appendix(ae.create_location_hours_table, TEXT["APPENDIX LOCATION HOURS INFORMATION"]["title"])

    # APPENDIX PROGRAM HOURS INFORMATION
    constructor.add_appendix(ae.create_program_hours_table, TEXT["APPENDIX PROGRAM HOURS INFORMATION"]["title"])

    # APPENDIX PROGRAM QUALIFICATIONS
    constructor.add_appendix(ae.create_program_by_program_qualifications_table, TEXT["APPENDIX PROGRAM QUALIFICATIONS"]["title"])

    # APPENDIX PROGRAM SERVICE AREAS
    constructor.add_appendix(ae.create_program_by_program_service_area_table, TEXT["APPENDIX PROGRAM SERVICE AREAS"]["title"])

    # Back Cover
    constructor.add_back_cover()

    # Save PDF
    constructor.save_pdf()

    # Save State
    ae.save_state(TEXT, TEXT_SAVE_NAME.replace('resources/', ''), directory + "/resources")
    ae.save_state(WEIGHTS, WEIGHTS_SAVE_NAME.replace('resources/', ''), directory + "/resources")
    ae.save_state(RECOMMENDED_FILTERS, RECOMMENDED_FILTERS_SAVE_NAME.replace('resources/', ''), directory + "/resources")
    ae.save_state(PROFILE_COMPLETION_TIERS, PROFILE_COMPLETION_TIERS_SAVE_NAME.replace('resources/', ''), directory + "/resources")
