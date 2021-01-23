import datetime
from random import randint
import pytest
import pandas as pd
import sys
sys.path.append("./src")
from filters import filter_by_from_date, filter_by_to_date, filter_by_apd, filter_by_query, filter_by_country, filter_by_category  # nopep8


@pytest.fixture
def test_dataframe():
    '''Returns a valid dataframe used for testing'''
    cols = ["title", "source", "timestamp", "url", "category", "country"]
    df_dict = dict()
    for col in cols:
        df_dict[col] = []
        for i in range(5):
            if col == "timestamp":
                date = datetime.datetime(2021, randint(4, 8), randint(10, 20))
                df_dict[col].append(date)
            else:
                df_dict[col].append(f"{col}:{i+1}")
    return pd.DataFrame.from_dict(df_dict)


def test_filter_by_from_date(test_dataframe):
    from_date = datetime.datetime(2021, 3, 9)
    result = filter_by_from_date(from_date, test_dataframe)
    bool_test = True
    for _, row in result.iterrows():
        check = row["timestamp"] >= from_date
        bool_test = bool_test and check
    assert bool_test


def test_filter_by_to_date(test_dataframe):
    to_date = datetime.datetime(2021, 10, 25)
    result = filter_by_to_date(to_date, test_dataframe)
    bool_test = True
    for _, row in result.iterrows():
        check = row["timestamp"] <= to_date
        bool_test = bool_test and check
    assert bool_test


def test_filter_by_apd(test_dataframe):
    result = filter_by_apd(1, test_dataframe)
    count_dict = dict()
    bool_test = True
    for _, row in result.iterrows():
        curr_date = f'{row["timestamp"].day}/{row["timestamp"].month}/{row["timestamp"].year}'
        count_entry = count_dict.get(curr_date, 0)
        if count_entry != 0:
            bool_test = False
            break
        count_dict[curr_date] = 1
    assert bool_test


def test_filter_by_query(test_dataframe):
    result = filter_by_query("title", test_dataframe)
    assert test_dataframe.shape[0] == len(test_dataframe)


def test_filter_by_country(test_dataframe):
    try:
        filter_by_country("USA", test_dataframe)
    except Exception as e:
        assert type(e) == NotImplementedError


def test_filter_by_category(test_dataframe):
    try:
        filter_by_category("poltics", test_dataframe)
    except Exception as e:
        assert type(e) == NotImplementedError
