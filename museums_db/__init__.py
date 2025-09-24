# museums_db package init
from .data import get_most_visited_museums
from .db import init_db, insert_museum, insert_city, get_museum_city_data
from .model import run_regression