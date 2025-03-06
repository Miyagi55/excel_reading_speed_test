# convert_xlsx_to_csv.py
import os
import pandas as pd
from tqdm import tqdm

def convert_xlsx_to_csv(input_folder='excel_files', output_folder='csv_files'):
    """Convert all XLSX files in input_folder to CSV files in output_folder"""
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Get all XLSX files
    xlsx_files = [f for f in os.listdir(input_folder) if f.endswith(('.xlsx', '.xls'))]
    
    if not xlsx_files:
        print(f"No Excel files found in {input_folder}!")
        return
    
    print(f"Converting {len(xlsx_files)} Excel files to CSV...")
    
    # Convert each file with progress bar
    for file in tqdm(xlsx_files, desc="Converting XLSX to CSV"):
        input_path = os.path.join(input_folder, file)
        output_path = os.path.join(output_folder, file.replace('.xlsx', '.csv').replace('.xls', '.csv'))
        
        # Read Excel and write to CSV
        df = pd.read_excel(input_path, engine='openpyxl')
        df.to_csv(output_path, index=False)

if __name__ == "__main__":
    convert_xlsx_to_csv()