import datetime
import pandas as pd
import re

logger = logging.getLogger()
logging.basicConfig(level="INFO")


def filter_by_from_date(from_date: datetime, local_df: pd.DataFrame) -> pd.DataFrame:
    raise NotImplementedError


def filter_by_to_date(to_date: datetime, local_df: pd.DataFrame) -> pd.DataFrame:
    raise NotImplementedError


def filter_by_country(country: str, local_df: pd.DataFrame) -> pd.DataFrame:
    raise NotImplementedError


def filter_by_category(category: str, local_df: pd.DataFrame) -> pd.DataFrame:
    raise NotImplementedError


def filter_by_apd(articles_per_day: int, local_df: pd.DataFrame) -> pd.DataFrame:
    raise NotImplementedError


def filter_by_query(query: str, local_df: pd.DataFrame) -> pd.DataFrame:
    '''Searches the cached dataframe for all the instances of the query and returns the resultant dataframe'''

    query = query.lower()

    result_frame = local_df[local_df['title'].str.contains(
        query, flags=re.IGNORECASE, regex=True)]

    del query, local_df

    return result_frame


def filter_by_timestamp(from_date: datetime, to_date: datetime, articles_per_day: int, local_df: pd.DataFrame) -> pd.DataFrame:
    '''Filters by the timeperiod & articles per day and returns the results'''

    from_timestamp = int(datetime.datetime.timestamp(from_date))
    to_timestamp = int(datetime.datetime.timestamp(to_date))

    result_frame = local_df[(local_df["unix timestamp"] >= from_timestamp) & (
        local_df["unix timestamp"] <= to_timestamp)]
    result_frame.sort_values(
        by="unix timestamp", ascending=False, inplace=True)
    result_frame["unix timestamp"] = result_frame["unix timestamp"].apply(
        lambda x: datetime.datetime.utcfromtimestamp(x).date().strftime('%d-%m-%Y'))
    dates = result_frame["unix timestamp"].unique()

    titles = []

    for d in dates:
        _recs = result_frame[result_frame["unix timestamp"] == d]
        titles += _recs["title"].iloc[:articles_per_day].to_list()

    result_frame = result_frame[result_frame["title"].isin(
        titles)][["title", "source", "timestamp", "url", "category", "country"]]

    del from_timestamp, to_timestamp, titles

    return result_frame
