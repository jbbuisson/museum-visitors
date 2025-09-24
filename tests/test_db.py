import museums_db

from pprint import pprint

if __name__ == "__main__":
    museums_db.init_db()

    museum_city_data = museums_db.db.get_museum_city_data()
    pprint(museum_city_data)
    print(f"Total records in database: {len(museum_city_data)}")
