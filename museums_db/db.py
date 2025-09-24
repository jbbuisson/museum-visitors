import sqlite3
import pandas as pd

DB_PATH = 'museums.db'

def init_db():
	conn = sqlite3.connect(DB_PATH)
	c = conn.cursor()
	c.execute('''
		CREATE TABLE IF NOT EXISTS museums (
			id INTEGER PRIMARY KEY,
			name TEXT,
			city TEXT,
			country TEXT,
			annual_visitors INTEGER
		)
	''')
	c.execute('''
		CREATE TABLE IF NOT EXISTS cities (
			id INTEGER PRIMARY KEY,
			name TEXT,
			country TEXT,
			population INTEGER
		)
	''')
	conn.commit()
	conn.close()

def insert_museum(name, city, country, annual_visitors):
	conn = sqlite3.connect(DB_PATH)
	c = conn.cursor()
	c.execute('INSERT INTO museums (name, city, country, annual_visitors) VALUES (?, ?, ?, ?)',
			  (name, city, country, annual_visitors))
	conn.commit()
	conn.close()

def insert_city(name, country, population):
	conn = sqlite3.connect(DB_PATH)
	c = conn.cursor()
	c.execute('INSERT INTO cities (name, country, population) VALUES (?, ?, ?)',
			  (name, country, population))
	conn.commit()
	conn.close()

def get_museum_city_data():
	conn = sqlite3.connect(DB_PATH)
	query = '''
		SELECT m.name, m.city, m.country, m.annual_visitors, c.population
		FROM museums m
		JOIN cities c ON m.city = c.name AND m.country = c.country
	'''
	df = pd.read_sql_query(query, conn)
	conn.close()
	return df
