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

    get_raw_data_from_geocoder(df_cities)

    print(f"Cities with missing population: {df_cities[df_cities['population'] == 0].shape[0]}")

    # Save to cache
    if cache_data:
        save_cache(df_cities, cache_file, cache_meta_file)

    return df_cities


def get_raw_data_from_geocoder(df_cities):
    populations = []
    errors = []
    max_retries = 3
    retry_delay = 2  # seconds

    for _, row in df_cities.iterrows():
        city = row["city"]
        country = row["country"]
        
        for attempt in range(max_retries):
            try:
                print(f"Fetching population for {city}, {country} (Attempt {attempt + 1})")
                g = geocoder.geonames(f"{city}, {country}", key="geonames_jb")
                if g.ok:
                    population = g.population
                    populations.append(population)
                    break
                else:
                    if attempt == max_retries - 1:
                        errors.append(f"Failed to get population for {city}, {country}: {g.error}")
                        populations.append(0)
            except Exception as e:
                if attempt == max_retries - 1:
                    errors.append(f"Error processing {city}, {country}: {str(e)}")
                    populations.append(0)
                time.sleep(retry_delay)
                continue
            
            time.sleep(retry_delay)  # Rate limiting protection
    
    if errors:
        print("Encountered errors while fetching population data:")
        for error in errors:
            print(f"- {error}")
            
    df_cities["population"] = populations
