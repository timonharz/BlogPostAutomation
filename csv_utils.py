import csv
import pandas as pd
import os

def split_csv(input_file_url, max_file_size_mb, output_dir='data/splitted'):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Get the size of the input file
    input_file_size = os.path.getsize(input_file_url) / (1024 * 1024)  # in MB
    
    # Check if file size is smaller than the max limit
    if input_file_size <= max_file_size_mb:
        print(f"The file is already smaller than the max size of {max_file_size_mb} MB.")
        return

    # Open the input file
    with open(input_file_url, 'r', newline='', encoding='utf-8') as input_file:
        reader = csv.reader(input_file)
        header = next(reader)  # Save the header to include it in each split file
        
        print("Header: ", header)
        
        # Create output files
        file_count = 0
        current_file_size = 0
        current_rows = []
        current_file = None
        writer = None
        
        for row in reader:
            # Check the size of the current chunk
            print("Current file size: ", current_file_size)
            if current_file is None or current_file_size + len(str(row)) / (1024 * 1024) > max_file_size_mb:
                # Close the previous file if it exists
                if current_file:
                    current_file.close()

                # Increment file count and create a new output file
                file_count += 1
                output_file_url = os.path.join(output_dir, f"split_file_{file_count}.csv")
                current_file = open(output_file_url, 'w', newline='', encoding='utf-8')
                writer = csv.writer(current_file)
                writer.writerow(header)  # Write header first
                
                # Reset current file size and row collection
                current_file_size = 0
                current_rows = []

            # Add the current row to the list of rows
            current_rows.append(row)
            current_file_size += len(str(row)) / (1024 * 1024)  # Increment current file size in MB

            # Write the rows into the current file if we're not over the size limit
            if len(current_rows) > 0:
                writer.writerows(current_rows)
                current_rows = []  # Reset current rows

        # Ensure to close the last file if any rows were written
        if current_file:
            print("Current file", current_file)
            current_file.close()
    
    
if __name__ == '__main__':
    split_csv('data/lds/blog_posts.csv',  1)