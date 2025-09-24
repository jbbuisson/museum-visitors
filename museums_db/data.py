import requests
import wikitextparser as wtp
import pandas as pd
import os
import dotenv

def get_most_visited_museums(min_visitors=2000000):
    """
    Retrieve the list of museums with more than min_visitors annually from Wikipedia.
    Returns a DataFrame with museum name, city, country, and annual visitors.
    """
    page = 'List_of_most-visited_museums'
    url = 'https://api.wikimedia.org/core/v1/wikipedia/en/page/' + page

    dotenv.load_dotenv()
    api_key = os.getenv('WIKIMEDIA_API_KEY')

    headers = {
        'Authorization': api_key,
        'User-Agent': 'jb'
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    parsed_data = wtp.parse(data['source'])
    section = parsed_data.sections[1]
    table = section.tables[0]
    table_data = table.data()

    index = 0
    for row in table_data:
        if index > 5:
            break

        print(row)
        index += 1

    df = pd.DataFrame(table_data[1:], columns=table_data[0])
    print(df)


def get_city_population(city, country=None):
	"""
	Retrieve city population from Wikipedia or external API (placeholder).
	Returns population as integer or None.
	"""
	# JBB
	# # Try Wikipedia first
	# wiki = wikipediaapi.Wikipedia('en')
	# page = wiki.page(city)
    # FIN JBB
	
	# Simple parsing: look for infobox population (real implementation should use API or regex)
	# Placeholder: return None
	return None
