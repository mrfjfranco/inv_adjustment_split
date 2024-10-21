import pandas as pd
import os
import sys

def get_current_dir():
    if getattr(sys, 'frozen', False):
        # If the application is bundled by PyInstaller
        return os.path.dirname(sys.executable)
    else:
        # If the application is run directly from the script
        return os.path.dirname(os.path.abspath(__file__))

# Get the current directory
current_dir = get_current_dir()

# Define the input and output folder paths
input_folder = os.path.join(current_dir, 'input')
output_folder = os.path.join(current_dir, 'output')

# Ensure the input and output folders exist
if not os.path.exists(input_folder):
    os.makedirs(input_folder)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Ensure the input folder exists and find the CSV file in it
input_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]
if not input_files:
    print(f"No CSV files found in the input folder: {input_folder}")
else:
    source_file_path = os.path.join(input_folder, input_files[0])

    try:
        # Load the source CSV into a DataFrame
        source_df = pd.read_csv(source_file_path)
        
        # Print ASCII Art Message
        print(r"""
        by Francisco J. Franco @mr.fjfranco
        """)

        # Ask the user for the part number and adjustment number
        part_number = input("Please enter the part number: ")
        adjustment_number = input("Please enter the adjustment number: ")

        # Ensure the correct column name is used
        serial_number_column = 'Serial #'

        # Create a new DataFrame with the required columns
        new_df = pd.DataFrame({
            'Part': part_number,
            'Location': source_df['Location'],
            'Manufacturer': '',
            'SerialNumber': source_df[serial_number_column],
            'Quantity': -1,
            'Lot': '',
            'Memo': '',
            'PartCost': '',
            'AdjustmentType': '',
            'AdjustmentReason': ''
        })

        # Split the DataFrame into chunks of 100 records
        chunks = [new_df[i:i + 100] for i in range(0, len(new_df), 100)]

        # Save each chunk into a new CSV file
        for idx, chunk in enumerate(chunks):
            chunk_file_name = f'{output_folder}/{adjustment_number}-{str(idx + 1).zfill(3)}.csv'
            chunk.to_csv(chunk_file_name, index=False)

        # Print number of files created
        print("")
        print(f"{len(chunks)} files have been created successfully in the output folder.")
        print("")

    except Exception as e:
        print(f"An error occurred: {e}")

# Prompt user to press a key to close
input("You can close the terminal now and thank Francisco :).")
