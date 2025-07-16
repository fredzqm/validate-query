# First, you need to install the required libraries.
# Open your terminal or command prompt and run:
# pip install googlesearch-python pandas

import re
import pandas as pd
import time
from googlesearch import search

# --- Configuration ---
INPUT_CSV_FILE = 'queries.csv'   # The name of your input file
OUTPUT_CSV_FILE = 'results.csv' # The name of the output file

def perform_validation(query, expected_groups_str):
    """
    Searches Google for a given query and checks if any found Facebook group IDs
    match the list of expected group IDs.
    """
    print(f"--- Validating query: '{query}' ---")
    try:
        # Convert the comma-separated string of expected groups into a list of strings.
        # .strip() handles any accidental whitespace.
        expected_ids = [group.strip() for group in str(expected_groups_str).split(',')]
        print(f"Expected Group IDs: {expected_ids}")

        # Perform the Google search. We use a sleep_interval to be polite.
        search_results = search(query, num_results=20, lang="en", sleep_interval=2)

        # This regex now captures the numeric group ID from the URL.
        # The '()' creates a capturing group.
        facebook_group_pattern = re.compile(r'https://www.facebook.com/groups/(\d+)/?$')

        # Loop through all the URLs returned by the search
        for url in search_results:
            match = facebook_group_pattern.match(url)
            # Check if the URL is a Facebook Group URL in the correct format
            if match:
                found_id = match.group(1) # Extract the captured group ID (the numbers)
                print(f"  Found potential group in search results: {url} (ID: {found_id})")
                
                # Check if the ID we found is in our list of expected IDs
                if found_id in expected_ids:
                    print(f"  SUCCESS: Found matching group ID {found_id}.")
                    return "matched" # A match was found, so we can return and stop searching.

        # If the loop finishes and no match was ever found
        print("  FAILURE: No matching group found in the top search results.")
        return "not matched"

    except Exception as e:
        # Handle cases where the search itself fails
        print(f"An error occurred during the search for '{query}': {e}")
        return "error"

def main():
    """
    Main function to read the CSV, process each row, and save the results.
    """
    try:
        # Read the input CSV using pandas
        df = pd.read_csv(INPUT_CSV_FILE)
    except FileNotFoundError:
        print(f"Error: Input file '{INPUT_CSV_FILE}' not found.")
        print("Please create this file in the same directory as the script.")
        # We'll create a sample file to help the user.
        sample_data = {'Query': ['"Top Trader Jobe Goods"'], 'Expected Groups': ['2324243,425343141']}
        sample_df = pd.DataFrame(sample_data)
        sample_df.to_csv(INPUT_CSV_FILE, index=False)
        print(f"A sample file '{INPUT_CSV_FILE}' has been created for you to use as a template.")
        return

    # This list will hold the result ("matched" or "not matched") for each row
    validation_results = []

    # df.iterrows() lets us loop through the CSV row by row
    for index, row in df.iterrows():
        query = row['Query']
        expected_groups = row['Expected Groups']
        
        # Call our function to perform the search and validation
        result = perform_validation(query, expected_groups)
        validation_results.append(result)

    # Add the list of results as a new column in our data
    df['Google Search Validation'] = validation_results

    # Save the updated data to a new CSV file
    df.to_csv(OUTPUT_CSV_FILE, index=False)

    print(f"--- Processing complete. ---")
    print(f"Results have been saved to '{OUTPUT_CSV_FILE}'.")

# This ensures the main() function runs when you execute the script
if __name__ == "__main__":
    main()
