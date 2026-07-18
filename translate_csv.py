# /// script
# dependencies = [
#   "pandas",
# ]
# ///

import argparse
import pandas as pd
import os


def load_column_mapping(mapping_file):
    """
    Load column mapping from a name/value pairs file.

    Supported line formats:
    - Old Name=New Name
    - Old Name:New Name

    Blank lines and lines starting with '#' are ignored.
    """
    if not os.path.exists(mapping_file):
        print(f"Error: Mapping file '{mapping_file}' was not found.")
        return None

    column_map = {}

    try:
        with open(mapping_file, "r", encoding="utf-8") as f:
            for line_number, raw_line in enumerate(f, start=1):
                line = raw_line.strip()

                if not line or line.startswith("#"):
                    continue

                separator = "=" if "=" in line else ":" if ":" in line else None
                if separator is None:
                    print(
                        f"Warning: Skipping invalid mapping at line {line_number}: '{raw_line.rstrip()}'"
                    )
                    continue

                old_name, new_name = line.split(separator, 1)
                old_name = old_name.strip()
                new_name = new_name.strip()

                if not old_name or not new_name:
                    print(
                        f"Warning: Skipping empty mapping at line {line_number}: '{raw_line.rstrip()}'"
                    )
                    continue

                column_map[old_name] = new_name
    except Exception as e:
        print(f"Error reading mapping file '{mapping_file}': {e}")
        return None

    if not column_map:
        print(f"Error: No valid mappings found in '{mapping_file}'.")
        return None

    return column_map

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
    parser = argparse.ArgumentParser(description="Translate and filter columns in a CSV file.")
    parser.add_argument("--input", "-i", default="source_data.csv", help="Path to the source CSV file (default: source_data.csv)")
    parser.add_argument("--output", "-o", default="transformed_data.csv", help="Path for the output CSV file (default: transformed_data.csv)")
    parser.add_argument("--map", "-m", default="column_map.txt", help="Path to the column mapping file (default: column_map.txt)")
    args = parser.parse_args()

    INPUT_CSV = args.input
    OUTPUT_CSV = args.output
    MAP_FILE = args.map

    COLUMN_MAP = load_column_mapping(MAP_FILE)
    if COLUMN_MAP is None:
        raise SystemExit(1)

    translate_csv(INPUT_CSV, OUTPUT_CSV, COLUMN_MAP)
