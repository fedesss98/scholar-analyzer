"""
GOOGLE SCHOLAR SCRAPER
Created by Federico Amato - 2025/02


"""
from typing import List
import pandas as pd
import requests
from bs4 import BeautifulSoup
import argparse
import json


parser = argparse.ArgumentParser(
    prog="Google Scholar Scraper",
    description="Scrape one query from Google Scholar and save all the results" \
        "found on the engine up to a certain number of pages.\n" \
        "Specify the research query and optionally the number of pages with the -p parameter.\n", 
)
parser.add_argument("query", help="Research Query for Google Scholar")
parser.add_argument("--pages", "-p", type=int, default=25, help="Maximum number of pages to scrape")


def split_greenbar(bar:str):
    data = bar.replace("\xa0", "").split("-")

    if len(data) == 3:
        authors:List[str] = data[0].split(",")
        date:str = data[1].split(",")[-1]
        journal:str = ', '.join(data[1].split(",")[:-1]).replace(u'\u2010', '-')
        publisher:str = data[2]
    else:
        authors:List[str] = data[0].split(",")
        date:str = data[1].split(",")[-1]
        journal = "-"
        publisher = "-"

    return authors, journal, date, publisher


def main(q:str, p:int):
    
    data = []
    headers = {
        'user-agent': 
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

    # Iterate over the specified number of pages
    for page in range(p): 

        # Built the GET request
        request_params = {
            "hl": "it",
            "q": f'\"{q.replace(" ", "+")}\"',
            "start": 10 * page,
        }
        url = "https://scholar.google.com/scholar"
        # Make the request
        r = requests.get(url, request_params, headers=headers)
        print(r.url)
        # Parse the request
        soup = BeautifulSoup(r.text, "lxml")
        # Check - print the first title of the page
        try:
            print(soup.find("h3").text)
        except AttributeError as e:
            print(f"Error: {e}")
        else:
            for i, div in enumerate(soup.find_all("div", class_="gs_ri")):
                green_bar:str = div.find("div", "gs_a").text
                authors, journal, date, publisher = split_greenbar(green_bar)

                paper_data = dict(
                    title = div.h3.text,
                    link = div.h3.a["href"],
                    authors = authors,
                    journal = journal,
                    date = date,
                    publisher = publisher,
                    summary = div.find("div", "gs_rs").text,
                    citations = div.find_all("a")[2].text.split()[-1],
                    result = 10 * page + i
                )
                data.append(paper_data)
    
    with open(f"./data/results_{q.replace(' ', '_')}.json", "w+") as f:
        json.dump(data, f, ensure_ascii=True, indent=4)

    return None

if __name__ == "__main__":
    args = parser.parse_args()

    q = args.query
    p = args.pages

    main(q, p)

