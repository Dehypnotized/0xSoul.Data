import os
import subprocess
import concurrent.futures
import csv
import glob
import datetime

def run_script(script_path):
    """Function to run a script."""
    try:
        result = subprocess.run(['python', script_path], check=True, capture_output=True, text=True)
        print(f"Script {script_path} finished with output:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Script {script_path} failed with error:\n{e.output}")

def merge_files():
    """Function to merge CSV files."""
    merged_data = {}

    for csv_file in glob.glob("*.csv"):
        print(f"Processing file: {csv_file}")

        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader, None)

            for row in reader:
                onion_link = row[0]
                if onion_link not in merged_data:
                    merged_data[onion_link] = row
                else:
                    merged_data[onion_link].extend(row[1:])

    for csv_file in glob.glob("*.csv"):
        if not csv_file.startswith("merged_onion_links_"):
            print(f"Deleting file: {csv_file}")
            os.remove(csv_file)

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_file = f"merged_onion_links_{timestamp}.csv"
    print(f"Writing merged data to {output_file}")

    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Onion Link', 'Additional Data...'])
        writer.writerows(merged_data.values())

    print("Merge completed!")

def main():
    root_folder = os.path.dirname(os.path.abspath(__file__))
    
    scripts_to_run = []
    for subdir, _, files in os.walk(root_folder):
        for file in files:
            if file.endswith('.py') and subdir != root_folder:
                scripts_to_run.append(os.path.join(subdir, file))

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(run_script, scripts_to_run)

    # Call the merge_files function after all scripts have finished executing
    merge_files()

if __name__ == "__main__":
    main()
