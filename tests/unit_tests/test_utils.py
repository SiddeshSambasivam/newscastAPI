from random import randint
import pytest
import pandas as pd
import sys
sys.path.append("./src")
from utils import parse_data, parse_results  # nopep8


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
    return pd.DataFrame.from_dict(df_dict)


def test_parse_results_valid(valid_data_frame):
    cols = ["title", "source", "timestamp", "url", "category", "country"]
    test_row = list(zip(valid_data_frame[cols].to_numpy()))[0][0]
    result = parse_data(test_row)
    assert len(result) == len(cols)


def test_parse_results_invalid(invalid_data_frame):
    cols = ["title", "source", "timestamp", "url", "category", "country"]
    test_row = list(zip(invalid_data_frame[cols].to_numpy()))[0][0]
    try:
        result = parse_data(test_row)
    except Exception as e:
        assert type(e) == KeyError
