# museums_db package init
from .data_museums import get_most_visited_museums
from .data_cities import extract_cities_and_countries, get_cities_population
from .db import init_db, insert_museums_data, insert_cities_data, get_museum_city_data
from .model import run_regression
