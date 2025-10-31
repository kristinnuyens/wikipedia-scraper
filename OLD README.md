# Wikipedia Scraper

## 🏢 Description

In this project, we created a scraper that built a JSON file with the political leaders of each country from [this API](https://country-leaders.onrender.com/docs).

Within this file, we included the first paragraph of the Wikipedia page of these leaders.

## 🧩 Installation

Clone this repository:

```
git clone https://github.com/kristinnuyens/wikipedia-scraper
cd wikipedia-scraper
```

## 📦 Repo structure

```
.
├── src/
│   ├── leaders_scraper.py
├── README.md
├── requirements.txt
├── wikipedia_scraper_RESTART.ipynb
└── wikipedia_scraper.ipynb
```
## 🛎️ Usage

1. Clone the repository to your local machine

2. Run the script, by executing `leaders_scraper.py` in the Terminal command line:

```
python3 leaders_scraper.py
```
## ⏱️ Timeline

I worked on this project for three days.

## 👩‍💻 Contributors

- Kristin Nuyens

## 📌 Personal Situation
This project was done as part of the AI & Data Science Bootcamp at BeCode.org.

Connect with me on [LinkedIn](https://www.linkedin.com/in/kristinnuyens/).


Once ready, move on to the next step and integrate your code into functions, create a `src` folder where you'll put the `leaders_scraper.py` 

#### 2a. A `leaders_scraper.py` module (Second MVP - OOP)

Now that you've made sure your code works! Let's practice restructuring your solution as a class.

Code up a `WikipediaScraper` scraper object that allows you to structurally retrieve data from the API.

The object should contain at least these six attributes: 
- `base_url: str` containing the base url of the API (https://country-leaders.onrender.com)
- `country_endpoint: str` → `/countries` endpoint to get the list of supported countries
- `leaders_endpoint: str` → `/leaders` endpoint to get the list of leaders for a specific country
- `cookies_endpoint: str` → `/cookie` endpoint to get a valid cookie to query the API
- `leaders_data: dict` is a dictionary where you store the data you retrieve before saving it into the JSON file
- `cookie: object` is the cookie object used for the API calls

The object should contain at least these five methods:
- `refresh_cookie() -> object` returns a new cookie if the cookie has expired
- `get_countries() -> list` returns a list of the supported countries from the API
- `get_leaders(country: str) -> None` populates the `leader_data` object with the leaders of a country retrieved from the API
- `get_first_paragraph(wikipedia_url: str) -> str` returns the first paragraph (defined by the HTML tag `<p>`) with details about the leader
- `to_json_file(filepath: str) -> None` stores the data structure into a JSON file

#### 2b. A `main.py` script

Bundle everything together in a `main.py` file that calls the `WikipediaScraper` object and saves the data into a JSON file.

### Quality Assurance

Read our ["Coding Best Practices Manifesto"](../../guidelines/PythonCodingBestPractices/coding-best-practices-manifesto.ipynb) and apply what's in there!

As an exercise, keep the must-have version separate from the nice-to-have version by using a different branch on GitHub. Please specify that in your README too.


## Deliverables

1. Publish your source code on your personal GitHub repository
    - `main.py`
    - `src/leaders_scraper.py`
    - `leaders_data.json` → the results file with a sensible structure containing the list of historical leaders for each country together with their details and the first paragraph (`<p>`) of the Wikipedia page
2. Pimp up the README file
   - Description
   - Installation
   - Usage
   - Visuals
   - ... anything else you find useful
3. Show case your repo! We will pseudo-randomly 2-3 colleagues to share their work during Friday's debrief (4:00 PM).

## Evaluation

| Criterion      | Indicator                                                    | Yes/No |
| -------------- | ------------------------------------------------------------ | ------ |
| 1. Is complete | Executes whithout errors                                     |        |
|                | Stores the correct information from the API in the file      |        |
| 2. Is correct  | The code is well typed                                       |        |
|                | Good usage of OOP                                            |        |
| 3. Is great    | Possibility to store output as a CSV file                    |        |
|                | Correct usage of `Session()`                                 |        |
|                | Multi-processing                                             |        |

## You got this!

![You've got this!](https://media.tenor.com/Y56BShm-6V0AAAAi/wikipedia-wikipedian.gif)