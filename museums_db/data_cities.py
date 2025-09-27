import geocoder
import pandas as pd
from pathlib import Path
import pickle
import time
from museums_db.utils import load_cache, save_cache

CACHE_FOLDER = Path("cache")
CACHE_FOLDER.mkdir(parents=True, exist_ok=True)

CACHE_FOLDER.mkdir(parents=True, exist_ok=True)


def extract_cities_and_countries(df_museums) -> pd.DataFrame:
    """
    Extract unique cities and countries from the museums DataFrame.
    Returns a DataFrame with unique city-country pairs.
    """
    df_cities = df_museums[["city", "country"]].drop_duplicates().reset_index(drop=True)
    return df_cities


def get_cities_population(df_cities, cache_data=True, cache_duration=86400) -> pd.DataFrame:
    cache_file = CACHE_FOLDER / "cities_population_cache.pkl"
    cache_meta_file = CACHE_FOLDER / "cities_population_cache_meta.txt"

    # Check cache
    if cache_data and cache_file.exists() and cache_meta_file.exists():
        df = load_cache(cache_file, cache_meta_file, cache_duration)
        if df is not None:
            return df

    populations = []
    for _, row in df_cities.iterrows():
        city = row["city"]
        country = row["country"]

        g = geocoder.geonames(f"{city}, {country}", key="geonames_jb")
        population = g.population if g.ok else 0
        populations.append(population)
        
    df_cities["population"] = populations

    print(f"Cities with missing population: {df_cities[df_cities['population'] == 0].shape[0]}")
    print(df_cities.head())

    # Save to cache
    if cache_data:
        save_cache(df_cities, cache_file, cache_meta_file)

    return df_cities
