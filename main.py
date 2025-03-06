# main.py
import os
import time
import logging
from tqdm import tqdm
import pandas as pd
import polars as pl
import dask.dataframe as dd
import fireducks.pandas as fd
from datetime import datetime

# Set up logging
logging.basicConfig(
    filename=f'read_performance_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

def get_csv_files(folder_path='csv_files'):
    """Get list of CSV files with their sizes"""
    files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    file_info = [(f, os.path.getsize(os.path.join(folder_path, f))) for f in files]
    return file_info

def test_library(library_func, files, folder_path, desc):
    """Test reading performance and count rows"""
    start_time = time.time()
    total_rows = 0
    
    for file, _ in tqdm(files, desc=desc):
        try:
            df = library_func(os.path.join(folder_path, file))
            # Count rows depending on library type
            if isinstance(df, (pd.DataFrame, fd.DataFrame)):
                total_rows += len(df)
            elif isinstance(df, pl.DataFrame):
                total_rows += df.height
            elif isinstance(df, dd.DataFrame):
                total_rows += len(df)
        except Exception as e:
            logging.error(f"Error in {desc} for file {file}: {str(e)}")
    
    duration = time.time() - start_time
    logging.info(f"{desc} completed in {duration:.2f} seconds, read {total_rows} rows")
    return duration, total_rows

def save_results(results):
    """Save results to CSV"""
    results_df = pd.DataFrame(results)
    results_df.to_csv('performance_results.csv', index=False)
    logging.info("Results saved to performance_results.csv")

def format_size(bytes_size):
    """Convert bytes to human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.2f} GB"

def main():
    folder_path = 'csv_files'
    
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' not found! Please run convert_xlsx_to_csv.py first.")
        logging.error(f"Folder '{folder_path}' not found")
        return
    
    csv_files = get_csv_files(folder_path)
    if not csv_files:
        print("No CSV files found in the folder!")
        logging.error("No CSV files found")
        return
    
    total_size = sum(size for _, size in csv_files)
    print(f"Found {len(csv_files)} CSV files to process (Total size: {format_size(total_size)})")
    logging.info(f"Starting processing of {len(csv_files)} files, total size: {format_size(total_size)}")
    
    # Define test configurations
    tests = {
        'Pandas': lambda path: pd.read_csv(path),
        'Polars': lambda path: pl.read_csv(
            path,
            infer_schema_length=10000,
            ignore_errors=True
        ),
        #'Dask': lambda path: dd.read_csv(path).compute(),
        'Fireducks': lambda path: fd.read_csv(path)
    }
    
    # Run tests and collect results
    results = {
        name: test_library(func, csv_files, folder_path, f"{name} Processing")
        for name, func in tests.items()
    }
    
    # Sort results by duration (fastest to slowest)
    sorted_results = sorted(results.items(), key=lambda x: x[1][0])
    
    # Create results dictionary with all data
    results_dict = {
        'Library': [name for name, _ in sorted_results],
        'Duration (seconds)': [dur for _, (dur, _) in sorted_results],
        'Rows Read': [rows for _, (_, rows) in sorted_results],
        'Files Processed': [len(csv_files)] * len(sorted_results),
        'Total Size': [format_size(total_size)] * len(sorted_results)
    }
    
    # Save results
    save_results(results_dict)
    
    # Print summary
    print("\nPerformance Summary (Fastest to Slowest):")
    print(f"Total files: {len(csv_files)}, Total size: {format_size(total_size)}")
    for name, (dur, rows) in sorted_results:
        print(f"{name}: {dur:.2f} seconds, {rows} rows read")

if __name__ == "__main__":
    main()