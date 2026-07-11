# /// script
# dependencies = [
#   "pandas",
# ]
# ///

import pandas as pd
import os

def translate_csv(input_file, output_file, column_mapping):
    """
    Translates a CSV file by renaming columns and filtering for specific ones.
    """
    try:
        if not os.path.exists(input_file):
            print(f"Error: The file '{input_file}' was not found.")
            return

        print(f"Reading {input_file}...")
        df = pd.read_csv(input_file)

        # Find which columns from our map actually exist in the source
        existing_columns = {old: new for old, new in column_mapping.items() if old in df.columns}
        missing_columns = set(column_mapping.keys()) - set(df.columns)

        if missing_columns:
            print(f"Warning: The following columns were not found in source: {missing_columns}")

        # Filter and rename
        df_transformed = df[list(existing_columns.keys())].copy()
        df_transformed.rename(columns=existing_columns, inplace=True)

        # Save result
        df_transformed.to_csv(output_file, index=False)
        print(f"Success! Translated file saved as: {output_file}")
        print("New format structure:", list(df_transformed.columns))

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # --- CONFIGURATION ---
    INPUT_CSV = 'source_data.csv' 
    OUTPUT_CSV = 'transformed_data.csv'
    
    COLUMN_MAP = {
        'First Name': 'fname',
        'Last Name': 'lname',
        'Email Address': 'email',
        'User Age': 'age',
        'Job Title': 'role'
    }

    translate_csv(INPUT_CSV, OUTPUT_CSV, COLUMN_MAP)
