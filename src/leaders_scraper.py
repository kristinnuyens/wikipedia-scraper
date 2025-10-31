#!/usr/bin/env python3
# leaders_scraper.py
import requests
from bs4 import BeautifulSoup
import json
import re

# --- Constants ---
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.0.1 Safari/605.1.15 wikipedia-scraper/1.0 (email: kristin.nuyens@gmail.com)"
HEADERS = {"User-Agent": USER_AGENT}
ROOT = "https://country-leaders.onrender.com"

# --- Functions ---
def get_cookies(session):
    """Fetch a fresh cookie from the API using the given session."""
    return session.get(ROOT + "/cookie").cookies

# def get_first_paragraph(wikipedia_url, session):
#     """Fetch the first paragraph from Wikipedia and clean it using regex."""
#     response = session.get(wikipedia_url)
#     soup = BeautifulSoup(response.text, "html.parser")
#     for p in soup.select("div.mw-parser-output p"):
#         text = p.get_text(strip=True)
#         if text:
#             # Clean the paragraph
#             return re.sub(r"\s+", " ", re.sub(r"\[[^\]]*\]|\([^\)]*?pronunciation[^\)]*?\)|&[a-z]+?;", "", text)).strip()
#     return None

#  Below updated get_first_paragraph function that also works for the French Leaders after the above was fixed for US

def get_first_paragraph(wikipedia_url, session):
    """Fetch the first meaningful paragraph from Wikipedia, handling infobox tables."""
    response = session.get(wikipedia_url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    # 1️⃣ Try first paragraph after the first table (infobox)
    first_paragraph = None
    passed_table = False
    for elem in soup.select("div.mw-parser-output > *"):
        if elem.name == "table":
            passed_table = True
            continue
        if passed_table and elem.name == "p":
            text = elem.get_text(strip=True)
            if text and any(c.isalpha() for c in text):
                first_paragraph = text
                break
    # 2️⃣ Fallback: first non-empty paragraph anywhere in mw-parser-output
    if not first_paragraph:
        for p in soup.select("div.mw-parser-output p"):
            text = p.get_text(strip=True)
            if text and any(c.isalpha() for c in text):
                first_paragraph = text
                break
    # 3️⃣ Clean the paragraph (remove references, pronunciation, entities)
    if first_paragraph:
        first_paragraph = re.sub(
            r"\s+", " ",
            re.sub(r"\[[^\]]*\]|\([^\)]*?pronunciation[^\)]*?\)|&[a-z]+?;", "", first_paragraph)
        ).strip()
    return first_paragraph

def get_leaders():
    """Return a dictionary of leaders per country, with first paragraph from Wikipedia."""
    leaders_per_country = {}
    with requests.Session() as session:
        session.headers.update(HEADERS)
        # Fetch countries
        cookies = get_cookies(session)
        countries = session.get(ROOT + "/countries", cookies=cookies).json()
        for country in countries:
            # Refresh cookie per country
            cookies = get_cookies(session)
            response = session.get(ROOT + "/leaders", cookies=cookies, params={"country": country})
            data = response.json()
            if isinstance(data, dict):
                data = data.get("leaders", [])
            # Add cleaned first paragraph from Wikipedia
            for leader in data:
                if "wikipedia_url" in leader:
                    leader["first_paragraph"] = get_first_paragraph(leader["wikipedia_url"], session)
            leaders_per_country[country] = data
    return leaders_per_country

def save(leaders_per_country):
    """Save leaders_per_country to a JSON file."""
    with open("leaders.json", "w", encoding="utf-8") as f:
        json.dump(leaders_per_country, f, ensure_ascii=False, indent=4)
    print("Saved leaders_per_country to leaders.json")

# --- Main execution ---
if __name__ == "__main__":
    leaders_per_country = get_leaders()
    save(leaders_per_country)
    print("Scraping complete!")