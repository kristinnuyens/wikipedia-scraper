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
    try:
        return session.get(ROOT + "/cookie", timeout=10).cookies
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Fetching cookie failed: {e}")
        return None

def get_first_paragraph(wikipedia_url, session):
    """Fetch the first meaningful paragraph from Wikipedia, handling infobox tables."""
    try:
        response = session.get(wikipedia_url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Fetching Wikipedia page failed: {wikipedia_url} | {e}")
        return None
    try:
        soup = BeautifulSoup(response.text, "html.parser")
        first_paragraph = None
        passed_table = False
        # 1️⃣ Paragraph after first table (infobox)
        for elem in soup.select("div.mw-parser-output > *"):
            if elem.name == "table":
                passed_table = True
                continue
            if passed_table and elem.name == "p":
                text = elem.get_text(strip=True)
                if text and any(c.isalpha() for c in text):
                    first_paragraph = text
                    break
        # 2️⃣ Fallback: first non-empty paragraph anywhere
        if not first_paragraph:
            for p in soup.select("div.mw-parser-output p"):
                text = p.get_text(strip=True)
                if text and any(c.isalpha() for c in text):
                    first_paragraph = text
                    break
        # 3️⃣ Clean paragraph
        if first_paragraph:
            first_paragraph = re.sub(
                r"\s+", " ",
                re.sub(r"\[[^\]]*\]|\([^\)]*?pronunciation[^\)]*?\)|&[a-z]+?;", "", first_paragraph)
            ).strip()
        return first_paragraph
    except Exception as e:
        print(f"[ERROR] Parsing Wikipedia page failed: {wikipedia_url} | {e}")
        return None

def get_leaders():
    """Return a dictionary of leaders per country, with first paragraph from Wikipedia."""
    leaders_per_country = {}
    with requests.Session() as session:
        session.headers.update(HEADERS)
        # Fetch countries safely
        try:
            cookies = get_cookies(session)
            if cookies is None:
                cookies = {}
            countries = session.get(ROOT + "/countries", cookies=cookies, timeout=10).json()
        except (requests.exceptions.RequestException, ValueError) as e:
            print(f"[ERROR] Fetching countries failed: {e}")
            return {}
        for country in countries:
            try:
                cookies = get_cookies(session)
                if cookies is None:
                    cookies = {}
                response = session.get(ROOT + "/leaders", cookies=cookies, params={"country": country}, timeout=10)
                data = response.json()
                if isinstance(data, dict):
                    data = data.get("leaders", [])
            except (requests.exceptions.RequestException, ValueError) as e:
                print(f"[ERROR] Fetching leaders for {country} failed: {e}")
                data = []
            # Add cleaned first paragraph from Wikipedia safely
            for leader in data:
                wiki_url = leader.get("wikipedia_url")
                if wiki_url:
                    leader["first_paragraph"] = get_first_paragraph(wiki_url, session)
            leaders_per_country[country] = data
    return leaders_per_country

def save(leaders_per_country):
    """Save leaders_per_country to a JSON file."""
    try:
        with open("leaders.json", "w", encoding="utf-8") as f:
            json.dump(leaders_per_country, f, ensure_ascii=False, indent=4)
        print("Saved leaders_per_country to leaders.json")
    except Exception as e:
        print(f"[ERROR] Saving JSON failed: {e}")

# --- Main execution ---
if __name__ == "__main__":
    leaders_per_country = get_leaders()
    save(leaders_per_country)
    print("Scraping complete!")