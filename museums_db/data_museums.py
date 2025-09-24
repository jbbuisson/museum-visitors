from pprint import pprint
import requests
import wikitextparser as wtp
import pandas as pd
from pathlib import Path
import dotenv
import re
import time
import pickle

CACHE_FOLDER = Path("cache")


def get_most_visited_museums(min_visitors=2_000_000) -> pd.DataFrame:
    """
    Retrieve from Wikipedia the list of museums with more than min_visitors annually.
    Returns a DataFrame with museum name, city, country, and annual visitors.
    """
    df_museum_data = get_raw_museum_data()

    clean_museum_data(df_museum_data)
    df_filtered = filter_museum_data(df_museum_data, min_visitors)

    assert (
        df_filtered.shape[0] == 53
    ), f"As of 2025/09/24, 53 museums should be found with at least {min_visitors} visitors"

    df_cleaned = df_filtered[["Name_clean", "City_clean", "country_clean", "annual_visitors"]].copy()
    df_cleaned = df_cleaned.rename(
        columns={
            "Name_clean": "name",
            "City_clean": "city",
            "country_clean": "country",
        }
    )

    return df_cleaned


def get_raw_museum_data(cache_data=True, cache_duration=86400) -> pd.DataFrame:
    cache_file = CACHE_FOLDER / "museum_data_cache.pkl"
    cache_meta_file = CACHE_FOLDER / "museum_data_cache_meta.txt"
    # Check cache
    if cache_data and cache_file.exists() and cache_meta_file.exists():
        try:
            with open(cache_meta_file, "r") as f:
                cache_time = float(f.read().strip())
            if time.time() - cache_time < cache_duration:
                with open(cache_file, "rb") as f:
                    df = pickle.load(f)
                return df
        except Exception:
            pass

    df = get_raw_data_from_wikipedia()

    # Save to cache
    if cache_data:
        try:
            with open(cache_file, "wb") as f:
                pickle.dump(df, f)
            with open(cache_meta_file, "w") as f:
                f.write(str(time.time()))
        except Exception:
            pass

    return df


def get_raw_data_from_wikipedia(page: str = "List_of_most-visited_museums"):
    # Fetch fresh data
    url = "https://api.wikimedia.org/core/v1/wikipedia/en/page/" + page

    dotenv.load_dotenv()
    api_key = dotenv.get_key(".env", "WIKIMEDIA_API_KEY")

    headers = {"Authorization": api_key, "User-Agent": "jb"}

    response = requests.get(url, headers=headers)
    data = response.json()
    parsed_data = wtp.parse(data["source"])
    section = parsed_data.sections[1]
    table = section.tables[0]
    table_data = table.data()

    df = pd.DataFrame(table_data[1:], columns=table_data[0])

    return df


def clean_museum_data(df_museum_data):
    clean_country_column(df_museum_data)
    clean_columns(
        df_museum_data,
        [
            "Name",
            "City",
        ],
    )
    clean_visitors_column(df_museum_data)


def clean_country_column(df):
    def extract_country(val):
        if pd.isnull(val):
            return None
        s = str(val)
        # Remove wiki markup like {{flag|France}} or {{flag|United Kingdom}}
        if s.startswith("{{flag|"):
            return s.replace("{{flag|", "").replace("}}", "").strip()
        # Remove other curly braces or wiki markup
        s = s.replace("{{", "").replace("}}", "").strip()
        # Remove any remaining pipes
        s = s.split("|")[-1].strip()
        # Remove brackets if present
        s = s.replace("[", "").replace("]", "").strip()
        return s

    country_col = [col for col in df.columns if "Country" in col or "country" in col][0]
    df["country_clean"] = df[country_col].apply(extract_country)
    return df


def clean_columns(df, columns_to_clean):
    def extract_value(val):
        if pd.isnull(val):
            return None
        s = str(val)
        # Remove wiki markup like [[Paris]] or [[Vatican City]], [[Rome]]
        # Split on ',' and take the first value (if multiple)
        s = s.split(",")[0]
        # Remove brackets
        s = s.replace("[", "").replace("]", "").strip()
        # Remove extra whitespace
        return s

    for column_to_clean in columns_to_clean:
        if column_to_clean not in df.columns:
            continue
        df[column_to_clean + "_clean"] = df[column_to_clean].apply(extract_value)


def clean_visitors_column(df):
    visitor_col = [col for col in df.columns if "Visitor" in col or "visitors" in col][0]
    df["annual_visitors"] = df[visitor_col].apply(parse_visitors)
    return df


def parse_visitors(val):
    if pd.isnull(val):
        return 0
    s = str(val)

    # Remove references and templates
    s = s.split("<")[0]
    s = s.split("{{")[0]
    s = s.split("(")[0]
    s = s.strip()

    # Handle 'million' cases
    match = re.search(r"([\d\.,]+)\s*million", s, re.IGNORECASE)
    if match:
        num = match.group(1).replace(",", "").replace(".", "")
        # If number like '3.78', treat as 3,780,000
        if "." in match.group(1):
            try:
                return int(float(match.group(1).replace(",", "")) * 1_000_000)
            except Exception:
                return 0
        try:
            return int(num) * 1_000
        except Exception:
            print(f"Warning: could not parse visitors value '{val}'")
            return 0

    # Handle numbers with mix of commas and dots (e.g. '4.230,000')
    match = re.search(r"([\d,.]+)", s)
    if match:
        try:
            return int(match.group(1).replace(",", "").replace(".", ""))
        except Exception:
            return 0

    # Fallback
    try:
        return int(s)
    except Exception:
        print(f"Warning: could not parse visitors value '{val}'")
        return 0


def filter_museum_data(df, min_visitors):
    df_filtered = filter_by_min_visitors(df, min_visitors)
    return df_filtered


def filter_by_min_visitors(df, min_visitors):
    return df[df["annual_visitors"] >= min_visitors]
