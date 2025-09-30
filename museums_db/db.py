import os

import mysql.connector
from mysql.connector import IntegrityError


def get_connection():
    DB_CONFIG = {
        "host": os.getenv("DB_HOST", "127.0.0.1"),
        "port": os.getenv("DB_PORT", "3306"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_DATABASE", "museum_db"),
    }

    return mysql.connector.connect(**DB_CONFIG)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS museums (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            city VARCHAR(255),
            country VARCHAR(255),
            annual_visitors INT,
            UNIQUE (name, city, country)
        )
    """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS cities (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            country VARCHAR(255),
            population BIGINT,
            UNIQUE (name, country)
        )
    """
    )
    conn.commit()
    cursor.close()
    conn.close()


def insert_museums_data(df):
    conn = get_connection()
    cursor = conn.cursor()

    query = "INSERT IGNORE INTO museums (name, city, country, annual_visitors) VALUES (%s, %s, %s, %s)"

    museums = []
    for _, row in df.iterrows():
        museums.append((row["name"], row["city"], row["country"], row["annual_visitors"]))

    try:
        cursor.executemany(query, museums)
        conn.commit()
    except IntegrityError as e:
        print(f"Warning: Duplicate museum entry detected. {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def insert_cities_data(df):
    conn = get_connection()
    cursor = conn.cursor()

    query = "INSERT IGNORE INTO cities (name, country, population) VALUES (%s, %s, %s)"

    cities = []
    for _, row in df.iterrows():
        cities.append((row["city"], row["country"], row["population"]))

    try:
        cursor.executemany(query, cities)
        conn.commit()
    except IntegrityError as e:
        print(f"Warning: Duplicate city entry detected. {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def get_museum_city_data():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT m.name AS museum_name, m.city AS city_name, m.country AS country_name,
               m.annual_visitors, c.population
        FROM museums m
        INNER JOIN cities c ON m.city = c.name AND m.country = c.country
    """
    )
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results
