"""
Google Scholar Data Analyzer

Created by Federico Amato - 2025/02.

This program reads metadata from a Google Scholar's reserach query and display some statistics
"""
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import numpy as np
from pathlib import Path

ROOT = Path("../")

import argparse

parser = argparse.ArgumentParser(
    prog="Google Scholar Data Analyzer", 
    description="Reads JSON data for a query and display some statistics")
parser.add_argument("query", type=str, help="Query to look for in the data folder")

# Enable LaTex figures formatting
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
})


def plot_cumsum_citations(data):
    fig, ax = plt.subplots(figsize=(10, 4), layout='tight')
    data = data[["date", "citations"]].groupby("date").sum().cumsum()
    x = [int(i) for i in data.index]
    y = data.values.flatten()

    ax.plot(x, y, lw=1)
    ax.set_title("Cumulated sum of citations")

    plt.show()
    return fig


def make_trend_figure(x, y, kind, title, hue):
    fig, ax = plt.subplots(figsize = (10, 4))
    
    if hue is not None:
        bar_cmap = plt.get_cmap("viridis")
        rescale = lambda y: (y - np.min(y)) / (np.max(y) - np.min(y))
        color = bar_cmap(rescale(hue))
        
        fig.colorbar(
            plt.cm.ScalarMappable(norm=Normalize(min(hue), max(hue)), cmap=bar_cmap),
            ax=ax, label="Cumulated number of citations", 
            ticks=np.linspace(min(hue), max(hue), 8, dtype=int),
        )
    else:
        color = "tab:blue"
    
    if kind == "bar":
        barp = ax.bar(x, y, color=color)
    elif kind == "line":
        ax.plot(x, y, lw=1)            
    
    ax.set_title(title)
    ax.annotate(f'Query: \n"{query.title()}"', (1991.3, 12.4),
            bbox=dict(boxstyle="round", pad=0.7,
                   ec="#cccccc",
                   fc="#fefefe",
                   ))
    
    return fig


def plot_trend(data, title, agg="sum", kind="bar", hue=0):
    if agg == "sum":
        xy = data.groupby("date").sum()
    elif agg == "count":
        xy = data.groupby("date").count()
        
    x = [int(i) for i in xy.index]
    y = xy.values.flatten()
    
    fig = make_trend_figure(x, y, kind, title, hue)

    plt.show()
    return fig


def main(q):
    print(f'Running analysis for "{q}"')
    data_folder = Path("./data")
    input_file = data_folder / f"results_{q.replace(' ', '_')}.json"

    # Check if output folder exists
    visualization_folder = data_folder / "visualization"
    visualization_folder.mkdir(parents=True, exist_ok=True)

    if not input_file.exists():
        raise FileNotFoundError(f"File associated with query {q} does not exists.")
    else:
        df = pd.read_json(input_file)

    # Correct dates
    df["date"] = df.date.apply(lambda x: int(x) if x.strip().isnumeric() else None)

    # Plot Distribution of pubblications by data
    cum_citations = df[["date", "citations"]].groupby("date").sum().cumsum().values.flatten()
    g_n_y = plot_trend(
        df[["date", "title"]], "Number of pubblications per year", "count", "bar", 
        hue=cum_citations)
    g_n_y.savefig(visualization_folder / f"pubblications_per_year_{q.replace(' ', '_')}.png")
    g_n_y.savefig(visualization_folder / f"pubblications_per_year_{q.replace(' ', '_')}.svg")
    
    # Plot Cumulative sum of citations
    g_c_y = plot_cumsum_citations(df)
    g_c_y.savefig(visualization_folder / f"cumulative_citations_{q.replace(' ', '_')}.png")
    g_c_y.savefig(visualization_folder / f"cumulative_citations_{q.replace(' ', '_')}.svg")


if __name__ == "__main__":
    args = parser.parse_args()
    query:str = args.query
    main(query)


