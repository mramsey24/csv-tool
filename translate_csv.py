# /// script
# dependencies = [
#   "pandas",
# ]
# ///

import pandas as pd
import os

def translate_csv(input_file, output_file, column_mapping):
    """
    Translates a CSV file. 
    The order of keys in column_mapping determines the order of columns in the output.
    Only columns listed in column_mapping will be kept (filtering).
    """
    try:
        if not os.path.exists(input_file):
            print(f"Error: The file '{input_file}' was not found.")
            return

        print(f"Reading {input_file}...")
        df = pd.read_csv(input_file)

        # 1. Identify which requested columns actually exist in the source file
        # We iterate through the mapping keys to maintain the user's desired order
        columns_to_keep = []
        missing_columns = []

        for old_col in column_mapping.keys():
            if old_col in df.columns:
                columns_to_keep.append(old_col)
            else:
                missing_columns.append(old_col)

        # 2. Warn the user about missing columns
        if missing_columns:
            print(f"Warning: The following requested columns were not found in source: {missing_columns}")

        if not columns_to_keep:
            print("Error: No valid columns found to extract. Check your mapping.")
            return

        # 3. Reorder and Filter
        # By passing the list 'columns_to_keep', pandas selects them in that specific order
        df_transformed = df[columns_to_keep].copy()

        # 4. Rename the columns based on the mapping
        df_transformed.rename(columns=column_mapping, inplace=True)

        # 5. Save result
        df_transformed.to_csv(output_file, index=False)
        print(f"Success! Translated file saved as: {output_file}")
        print(f"Final column order: {list(df_transformed.columns)}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # --- CONFIGURATION AREA ---
    
    INPUT_CSV = 'source_data.csv' 
    OUTPUT_CSV = 'transformed_data.csv'
    
    # THE TRANSLATION MAP
    # Rules:
    # 1. Order of keys = The order of columns in your NEW file.
    # 2. If a column is NOT in this dictionary, it will be DROPPED from the new file.
    # 3. Format -> 'Old Name': 'New Name'
    COLUMN_MAP = {        
        'Date': 'date',
        'Name': 'Payee',        
        'Category': 'category',
        'Custom Name': 'custom_name',                
        'Amount': 'amount',       

    }

    translate_csv(INPUT_CSV, OUTPUT_CSV, COLUMN_MAP)
