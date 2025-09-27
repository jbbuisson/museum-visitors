import museums_db
import pytest
import pandas as pd


@pytest.mark.parametrize(
    "input_val,expected",
    [
        (None, 0),
        (pd.NA, 0),
        ("3 million", 3_000_000),
        ("3.78 million", 3_780_000),
        ("2,500,000", 2_500_000),
        ("4.230,000", 4_230_000),
        ("1,234,567", 1_234_567),
        ("500000", 500_000),
        ("{{flag|France}}", 0),
        ("2.5 million<ref>", 2_500_000),
        ("2,000,000 (2019)", 2_000_000),
        ("1.2 million", 1_200_000),
        ("not a number", 0),
        ("", 0),
        ("3,000", 3_000),
        ("1.5 million", 1_500_000),
        ("2.000.000", 2_000_000),
    ],
)
def test_parse_visitors(input_val, expected):
    assert museums_db.data_museums.parse_visitors(input_val) == expected


if __name__ == "__main__":
    df_museums_data = museums_db.get_most_visited_museums()
    print(df_museums_data.head())

    df_cities_countries = museums_db.extract_cities_and_countries(df_museums_data)
    print(df_cities_countries.head())
