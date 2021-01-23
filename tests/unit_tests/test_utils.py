import datetime
from random import randint
import pytest
import pandas as pd
import sys
sys.path.append("./src")
from utils import parse_data, parse_results, convert_str_to_datetime  # nopep8


@pytest.fixture
def valid_data_frame():
    '''Returns a valid dataframe used for testing'''
    cols = ["title", "source", "timestamp", "url", "category", "country"]
    df_dict = dict()
    for col in cols:
        df_dict[col] = []
        for i in range(5):
            df_dict[col].append(f"{col}:{i+1}")
    return pd.DataFrame.from_dict(df_dict)


@pytest.fixture
def invalid_data_frame():
    '''Returns an invalid dataframe used for testing'''
    cols = ["title", "source", "timestamp", "url", "category", "country"]
    cols.pop(randint(0, len(cols)-1))
    df_dict = dict()
    for col in cols:
        df_dict[col] = []
        for i in range(5):
            df_dict[col].append(f"{col}:{i+1}")
    return pd.DataFrame.from_dict(df_dict), cols


@pytest.fixture
def valid_time():
    date, month, year, hour, minute, second = 1, 1, 2021, 0, 0, 0
    return f"{date}/{month}/{year}, {hour}:{minute}:{second}"


@pytest.fixture
def invalid_time():
    return ""


def test_parse_data_valid(valid_data_frame):
    cols = ["title", "source", "timestamp", "url", "category", "country"]
    test_row = list(zip(valid_data_frame[cols].to_numpy()))[0][0]
    result = parse_data(test_row)
    assert len(result) == len(cols)


def test_parse_data_invalid(invalid_data_frame):
    invalid_df, cols = invalid_data_frame
    test_row = list(zip(invalid_df[cols].to_numpy()))[0][0]
    try:
        result = parse_data(test_row)
    except Exception as e:
        assert type(e) == KeyError


def test_parse_results_valid(valid_data_frame):
    result = parse_results(valid_data_frame)
    num_cols = len(result[0])
    num_rows = len(result)
    assert valid_data_frame.shape == (num_rows, num_cols)


def test_parse_results_invalid(invalid_data_frame):
    invalid_df, cols = invalid_data_frame
    try:
        result = parse_results(invalid_df)
    except Exception as e:
        assert type(e) == KeyError


def test_convert_str_to_datetime_valid(valid_time):
    result = convert_str_to_datetime(valid_time)
    assert result.day == 1
    assert result.month == 1
    assert result.year == 2021
    assert type(result) == datetime.datetime


def test_convert_str_to_datetime_invalid(invalid_time):
    assert convert_str_to_datetime(invalid_time) is None
