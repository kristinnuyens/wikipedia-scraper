
# I only just started looking at making the script more reusable using OOP

#!/usr/bin/env python3
# leaders_scraper_oop.py
import requests
from bs4 import BeautifulSoup
import json
import re


class APIClient:
    ROOT = "https://country-leaders.onrender.com"
    USER_AGENT = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.0.1 "
        "Safari/605.1.15 wikipedia-scraper/1.0 (email: kristin.nuyens@gmail.com)"
    )

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.USER_AGENT})

    def _refresh_cookie(self):
        response = self.session.get(f"{self.ROOT}/cookie", timeout=10)
        return response.cookies

    def get_countries(self):
        cookies = self._refresh_cookie()
        response = self.session.get(f"{self.ROOT}/countries", cookies=cookies, timeout=10)
        return response.json()

    def get_leaders(self, country):
        cookies = self._refresh_cookie()
        response = self.session.get(
            f"{self.ROOT}/leaders", cookies=cookies, params={"country": country}, timeout=10
        )
        data = response.json()
        return data.get("leaders", []) if isinstance(data, dict) else data


class WikipediaFetcher:
    def __init__(self, session=None):
        self.session = session or requests.Session()

    def get_first_paragraph(self, url):
        response = self.session.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

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

        if not first_paragraph:
            for p in soup.select("div.mw-parser-output p"):
                text = p.get_text(strip=True)
                if text and any(c.isalpha() for c in text):
                    first_paragraph = text
                    break

        if first_paragraph:
            first_paragraph = re.sub(
                r"\s+", " ",
                re.sub(r"\[[^\]]*\]|\([^\)]*?pronunciation[^\)]*?\)|&[a-z]+?;", "", first_paragraph)
            ).strip()

        return first_paragraph


class LeaderSaver:
    def save_to_json(self, data, filename="leaders.json"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"✅ Saved leaders to {filename}")


class LeaderScraper:
    def __init__(self):
        self.api = APIClient()
        self.wikipedia = WikipediaFetcher()
        self.saver = LeaderSaver()

    def scrape_all(self):
        leaders_per_country = {}
        countries = self.api.get_countries()

        for country in countries:
            leaders = self.api.get_leaders(country)
            for leader in leaders:
                if "wikipedia_url" in leader:
                    leader["first_paragraph"] = self.wikipedia.get_first_paragraph(
                        leader["wikipedia_url"]
                    )
            leaders_per_country[country] = leaders

        return leaders_per_country

    def run(self):
        data = self.scrape_all()
        self.saver.save_to_json(data)
        print("Scraping complete!")


if __name__ == "__main__":
    scraper = LeaderScraper()
    scraper.run()
