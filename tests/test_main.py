import sys
import os

import museums_db
import pandas as pd

from pprint import pprint


def main(init_db=False):
    if init_db:
        # Initialize the database
        museums_db.init_db()

        df_museums = museums_db.get_most_visited_museums()
        print(f"Loaded {len(df_museums)} museums")
        print(df_museums.head())

        museums_db.db.insert_museums_data(df_museums)

        df_cities_countries = museums_db.extract_cities_and_countries(df_museums)
        print(df_cities_countries.head())

        museums_db.get_cities_population(df_cities_countries)
        print(df_cities_countries.head())

        museums_db.insert_cities_data(df_cities_countries)

    museum_city_data = museums_db.get_museum_city_data()
    df_select_data = pd.json_normalize(museum_city_data)

    print(df_select_data)


if __name__ == "__main__":
    main()
