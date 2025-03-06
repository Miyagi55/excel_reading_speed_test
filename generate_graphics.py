# visualize_results.py
import pandas as pd
import matplotlib.pyplot as plt
import os

def visualize_performance(csv_path='performance_results.csv', output_file='performance_chart.png'):
    """Create and save a bar chart from performance results with additional metrics"""
    try:
        # Check if input file exists
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Could not find '{csv_path}'. Please run the main script first.")
        
        # Read the results CSV
        df = pd.read_csv(csv_path)
        
        # Verify we have the expected columns
        required_columns = {'Library', 'Duration (seconds)', 'Rows Read', 'Files Processed', 'Total Size'}
        if not required_columns.issubset(df.columns):
            raise ValueError(f"CSV file must contain columns: {required_columns}")
        
        # Ensure data is sorted by duration (should be from main script, but confirm here)
        df = df.sort_values('Duration (seconds)')
        
        # Create bar plot
        plt.figure(figsize=(12, 7))
        bars = plt.bar(df['Library'], df['Duration (seconds)'], color='skyblue')
        
        # Customize the plot
        plt.title('CSV Reading Performance Comparison (Fastest to Slowest)', fontsize=14, pad=15)
        plt.xlabel('Library', fontsize=12)
        plt.ylabel('Duration (seconds)', fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width()/2.,
                height,
                f'{height:.2f}',
                ha='center',
                va='bottom'
            )
        
        # Create legend text with additional metrics (using first row for shared values)
        legend_text = (
            f"Files Processed: {df['Files Processed'].iloc[0]}\n"
            f"Total Size: {df['Total Size'].iloc[0]}\n"
            "Rows Read:\n" +
            "\n".join(f"  {row['Library']}: {row['Rows Read']}" for _, row in df.iterrows())
        )
        
        # Add legend
        plt.legend([legend_text], loc='upper left', title='Metrics', bbox_to_anchor=(1.05, 1), borderaxespad=0.)
        
        # Adjust layout to accommodate legend
        plt.tight_layout()
        
        # Save the plot
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()  # Close the figure to free memory
        
        # Verify the file was created
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"Chart successfully saved as '{output_file}' (Size: {file_size} bytes)")
        else:
            raise RuntimeError(f"Failed to save chart to '{output_file}'")
        
    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"Error creating visualization: {str(e)}")

if __name__ == "__main__":
    visualize_performance()