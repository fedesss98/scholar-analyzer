"""
Google Scholar Data Analyzer

Created by Federico Amato - 2025/02.

This program reads metadata from a Google Scholar's reserach query and display some statistics
"""
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import argparse

parser = argparse.ArgumentParser(
    prog="Google Scholar Data Analyzer", 
    description="Reads JSON data for a query and display some statistics")
parser.add_argument("query", type=str, help="Query to look for in the data folder")


def plot_distribution(data):
    fig, ax = plt.subplots(figsize=(8, 6), tight_layout=True)

    ax.hist(data["date"])
    ax.set_title("Number of pubblications per year")

    return fig


def main(q):
    print(f'Running analysis for "{q}"')
    data_folder = Path("./data")
    input_file = data_folder / f"results_{q.replace(' ', '_')}.json"

    if not input_file.exists():
        raise FileNotFoundError(f"File associated with query {q} does not exists.")
    else:
        df = pd.read_json(input_file)

    # Plot Distribution of pubblications by data
    plot_distribution(df)
    plt.show()


if __name__ == "__main__":
    args = parser.parse_args()
    query:str = args.query
    main(query)


