"""
JSON to CSV
Created by Federico Amato - 2025/02

Convert the JSON file for one query to a csv file---human readable
"""
import pandas as pd
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(
    prog="Google Scholar Scraper",
    description="Scrape one query from Google Scholar and save all the results" \
        "found on the engine up to a certain number of pages.\n" \
        "Specify the research query and optionally the number of pages with the -p parameter.\n", 
)
parser.add_argument("query", type=str, help="Research Query for Google Scholar")


def main(q):
    
    data_folder = Path("./data")
    filename = data_folder / f"results_{q.replace(' ', '_')}.json"

    # Read JSON file
    df = pd.read_json(filename)
    # Save CSV file
    df.to_csv(data_folder / f"{q.replace(' ', '_')}.csv", index=False)

    return None


if __name__ == "__main__":
    args = parser.parse_args()
    query:str = args.query
    main(query)
