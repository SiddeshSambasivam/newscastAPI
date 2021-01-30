import datetime
import logging
import re

import pandas as pd

logger = logging.getLogger()
logging.basicConfig(level="INFO")


def filter_by_from_date(from_date: datetime, local_df: pd.DataFrame) -> pd.DataFrame:
    '''Returns the dataframe after filtering samples published after the from_date'''

    result_frame = local_df[(local_df["timestamp"] >= from_date)]

    del from_date, local_df

    return result_frame


def filter_by_to_date(to_date: datetime, local_df: pd.DataFrame) -> pd.DataFrame:
    '''Returns the dataframe after filtering samples published till the to_date'''

    result_frame = local_df[(local_df["timestamp"] <= to_date)]

    del to_date, local_df

    return result_frame


def filter_by_apd(articles_per_day: int, local_df: pd.DataFrame) -> pd.DataFrame:
    '''Returns by selecting limited number of articles per day'''

    local_df.sort_values(by="timestamp", ascending=False, inplace=True)
    local_df["unix timestamp"] = local_df["timestamp"].apply(
        lambda x: datetime.datetime(x.year, x.month, x.day))

    dates = local_df["unix timestamp"].unique()
    titles = list()

    for d in dates:
        _recs = local_df[local_df["unix timestamp"] == d]
        _recs.sort_values(by="timestamp", ascending=False, inplace=True)
        titles += _recs["title"].iloc[:articles_per_day].to_list()

    result_frame = local_df[local_df["title"].isin(
        titles)][["title", "source", "timestamp", "url", "category", "country"]]

    del local_df, dates

    return result_frame


def filter_by_query(query: str, local_df: pd.DataFrame) -> pd.DataFrame:
    '''Searches the cached dataframe for all the instances of the query and returns the resultant dataframe'''

    query = query.lower()

    result_frame = local_df[local_df['title'].str.contains(
        query, flags=re.IGNORECASE, regex=True)]

    del query, local_df

    return result_frame


def filter_by_country(country: str, local_df: pd.DataFrame) -> pd.DataFrame:

    country = country.upper()

    result_frame = local_df[local_df['country']==country]

    del country

    return result_frame


def filter_by_category(category: str, local_df: pd.DataFrame) -> pd.DataFrame:
    raise NotImplementedError
