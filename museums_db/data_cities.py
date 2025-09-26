import geocoder
import pandas as pd

CACHE_FOLDER = "cache"


def extract_cities_and_countries(df_museums) -> pd.DataFrame:
    """
    Extract unique cities and countries from the museums DataFrame.
    Returns a DataFrame with unique city-country pairs.
    """
    df_cities = df_museums[["city", "country"]].drop_duplicates().reset_index(drop=True)
    return df_cities


def get_cities_population(df_cities) -> pd.DataFrame:
    """
    Retrieve populations for a list of cities using the GeoNames API.
    Expects a DataFrame with 'city' and 'country' columns.
    Returns a DataFrame with 'city', 'country', and 'population'.
    """
    populations = []
    for _, row in df_cities.iterrows():
        city = row["city"]
        country = row["country"]

        g = geocoder.geonames(f"{city}, {country}", key="geonames_jb")
        population = g.population if g.ok else 0
        populations.append(population)

    df_cities["population"] = populations
    return df_cities
