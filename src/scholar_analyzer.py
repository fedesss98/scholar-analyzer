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
    fig, ax = plt.subplots(figsize=(10, 4), tight_layout=True)

    ax.hist(data["date"])
    ax.set_title("Number of pubblications per year")

    return fig


def plot_trend(data, title, agg="count"):
    if agg == "count":
        xy = data.groupby("date").count()
    elif agg == "sum":
        xy = data.groupby("date").sum()

    x = [int(i) for i in xy.index]
    y = xy.values.flatten()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(x, y, linewidth=0.1)

    ax.set_title(title)
    
    plt.show()
    return fig


def main(q):
    print(f'Running analysis for "{q}"')
    data_folder = Path("./data")
    input_file = data_folder / f"results_{q.replace(' ', '_')}.json"

    if not input_file.exists():
        raise FileNotFoundError(f"File associated with query {q} does not exists.")
    else:
        df = pd.read_json(input_file)

    # Correct dates
    df["date"] = df.date.apply(lambda x: int(x) if x.strip().isnumeric() else None)

    # Plot Distribution of pubblications by data
    plot_trend(df[["date", "title"]], "Number of pubblications per year")
    plot_trend(df[["date", "citations"]], "Number of citations per year", "sum")
    plot_distribution(df)
    plt.show()


if __name__ == "__main__":
    args = parser.parse_args()
    query:str = args.query
    main(query)


