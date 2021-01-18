import os
import logging
import datetime
import re
import time

import flask
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
import pymongo
import pandas as pd
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit


from utils import convert_str_to_datetime
from utils import parse_data
from utils import parse_results

# FLASK Configs
app = Flask(__name__)
app.config["DEBUG"] = False
CORS(app)

# Set up logger and the logging levels
logger = logging.getLogger()
apscheduler_logger = logging.getLogger("apscheduler").setLevel(logging.ERROR)
logging.basicConfig(level="INFO")

# Environment Variables
PORT = int(os.environ.get("PORT", 10000))
user_ = os.environ.get("user_")
pass_ = os.environ.get("pass_")

# Caching Variables
INITIAL_CACHE = True
data_frame = None  # local caching: contains all the records in the database

# Setting up the background processes
scheduler = BackgroundScheduler()
scheduler.start()
atexit.register(lambda: scheduler.shutdown())
cache_job_start = None


def cache_data() -> None:
    '''
    Caches the database locally during startup and 
    creates a job to caches database recurring for every 75 minutes
    '''

    global data_frame
    global INITIAL_CACHE

    if INITIAL_CACHE:
        logging.info("removing initial cache")
        global cache_job_start
        cache_job_start.remove()
        cache_job_start = scheduler.add_job(
            func=cache_data,
            trigger=IntervalTrigger(minutes=75),
            replace_existing=True)
        INITIAL_CACHE = False

    # mongoDB database
    db_start = time.time()
    client = MongoClient(
        f"mongodb+srv://{user_}:{pass_}@db-news-and-tweets.buxsd.mongodb.net/test")
    db = client.daily_feeds.feeds
    db_end = time.time()

    sort_start = time.time()
    data_frame = pd.DataFrame(list(db.find({})))
    sort_end = time.time()
    logging.info(
        f"Database loaded in {(db_end - db_start)} seconds and sorted in {(sort_end-sort_start)} seconds, with initial cache condition set to {INITIAL_CACHE}")
    data_frame.sort_values(by=["unix timestamp"],
                           ascending=False, inplace=True)
    logger.info(f"Cached {len(data_frame)} records")

    del db, client


# Starts the initial caching after 10 seconds
cache_job_start = scheduler.add_job(
    func=cache_data,
    trigger=IntervalTrigger(seconds=10),
    replace_existing=True)


def query_search(query: str) -> pd.DataFrame:
    '''Searches the cached dataframe for all the instances of the query and returns the resultant dataframe'''

    query = query.lower()

    result_frame = data_frame[data_frame['title'].str.contains(
        query, flags=re.IGNORECASE, regex=True)]
    del query

    return result_frame


def getby_timestamp(from_date: datetime, to_date: datetime, articles_per_day: int, local_df) -> pd.DataFrame:
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


def get_results(from_date: str, to_date: str, query: str = None, articles_per_day: int = 10) -> dict:
    '''Returns a dict of the search results with all the user constraints'''

    timeperiod_condn = (from_date != datetime.datetime.utcnow().date().strftime("%d/%m/%Y, %H:%M:%S")
                        or to_date != "".join([datetime.datetime.utcnow().date().strftime("%d/%m/%Y"), ", 23:59:59"]))

    from_date = convert_str_to_datetime(from_date)
    to_date = convert_str_to_datetime(to_date)

    if query == None:

        if timeperiod_condn:
            '''return the top results in the given timeframe'''

            results = getby_timestamp(
                from_date, to_date, articles_per_day, data_frame)

            results = parse_results(
                raw_results=results, articles_per_day=articles_per_day)
            return {"len": len(results), "results": results}

        # In case no query provided, return the top 10 recent headlines
        results = parse_results(
            raw_results=results, articles_per_day=articles_per_day)

        return {"len": len(results), "results": results}

    results = query_search(query)

    if timeperiod_condn:
        '''return the top results in the given timeframe'''

        results = getby_timestamp(
            from_date, to_date, articles_per_day, results)
        results = parse_results(raw_results=results)

        return {"len": len(results), "results": results}

    results = parse_results(
        raw_results=results, articles_per_day=articles_per_day)

    # NOTE: Implement crawling when a topic has zero results

    return {"len": len(results), "results": results}


@app.route("/api", methods=["GET"])
def endpoint():
    '''parses all the params and returns the result json'''

    # Initialization of the default params
    config = {
        "query":  None,
        "from_date": datetime.datetime.utcnow().date().strftime("%d/%m/%Y, 00:00:00"),
        "to_date": datetime.datetime.utcnow().date().strftime("%d/%m/%Y, 23:59:29"),
        "articles_per_day": 10,
    }

    params = request.args.to_dict()  # parse user params
    for k, v in params.items():
        if k not in config:
            response = flask.Response()
            response.status_code = 422
            return response

        config[k] = v

    query = config["query"]
    articles_per_day = int(config["articles_per_day"])

    if convert_str_to_datetime(config["from_date"]) == None or convert_str_to_datetime(config["to_date"]) == None:
        response = flask.Response()
        response.status_code = 422
        return response

    results = get_results(
        query=query,
        from_date=config["from_date"],
        to_date=config["to_date"],
        articles_per_day=articles_per_day
    )

    return flask.jsonify(results)


if __name__ == "__main__":

    # cache_data() # cache data at the startup
    app.run(debug=True, host="0.0.0.0", port=PORT)
