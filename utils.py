import datetime
import pandas as pd
import re

def parse_data(record:list) -> dict:
    '''Converts a record in a dataframe to dict'''

    cols = ["title", "source", "timestamp", "url", "category", "country"]
    result = dict()
    for k, v in zip(cols, record):
        result.update({k:v})
        
    return result

def convert_str_to_datetime(s: str):
    '''Returns a datetime object from datetime string'''
    
    try:
        datetime_ = datetime.datetime.strptime(s, "%d/%m/%Y, %H:%M:%S")
    except ValueError:
        datetime_ = None

    return datetime_


