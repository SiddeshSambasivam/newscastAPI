import datetime
import pandas as pd
import re

logger = logging.getLogger()
logging.basicConfig(level="INFO")


def parse_results(raw_results: pd.DataFrame) -> list:
    '''Iterates through each record in dataframe and returning a list of all the records as dict'''

    results = [parse_data(row[0]) for row in zip(raw_results[[
        "title", "source", "timestamp", "url", "category", "country"]].to_numpy())]

    return results


def parse_data(record: list) -> dict:
    '''Converts a record in a dataframe to dict'''

    cols = ["title", "source", "timestamp", "url", "category", "country"]
    result = dict()
    for k, v in zip(cols, record):
        result.update({k: v})

    return result


def convert_str_to_datetime(s: str):
    '''Returns a datetime object from datetime string'''

    try:
        datetime_ = datetime.datetime.strptime(s, "%d/%m/%Y, %H:%M:%S")
    except ValueError:
        datetime_ = None

    return datetime_
