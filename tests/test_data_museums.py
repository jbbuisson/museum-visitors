import museums_db
import pytest
import pandas as pd


@pytest.mark.parametrize(
    "input_val,expected",
    [
        (None, 0),
        (pd.NA, 0),
        ("3 million", 3000000),
        ("3.78 million", 3780000),
        ("2,500,000", 2500000),
        ("4.230,000", 4230000),
        ("1,234,567", 1234567),
        ("500000", 500000),
        ("{{flag|France}}", 0),
        ("2.5 million<ref>", 2500000),
        ("2,000,000 (2019)", 2000000),
        ("1.2 million", 1200000),
        ("not a number", 0),
        ("", 0),
        ("3,000", 3000),
        ("1.5 million", 1500000),
        ("2.000.000", 2000000),
    ],
)
def test_parse_visitors(input_val, expected):
    assert museums_db.data_museums.parse_visitors(input_val) == expected


if __name__ == "__main__":
    df_museums_data = museums_db.get_most_visited_museums()
    print(df_museums_data.head())

    df_cities_countries = museums_db.extract_cities_and_countries(df_museums_data)
    print(df_cities_countries.head())
