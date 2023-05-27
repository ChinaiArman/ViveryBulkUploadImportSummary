# Import packages
import argparse
import pandas as pd

# Import local files
from pdfConstructor import pdfConstructor


if __name__ == "__main__":
    # Define console parser
    parser = argparse.ArgumentParser(description="Create data visualizations for a Pre-Validated file")
    # Add file argument
    parser.add_argument("file", action="store", help="The file to validate.")
    # Console arguments
    args = parser.parse_args()
    
    # Create dataframe
    df = pd.read_csv(args.file, encoding='unicode_escape')
    
    # Create pdfConstructor instance
    constructor = pdfConstructor(df, args.file)

    # Create PDF
