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
mode_ = os.environ.get("mode_")

# Developement
if mode_ == None:
    from filters import filter_by_query, filter_by_to_date, filter_by_category, filter_by_apd, filter_by_country, filter_by_from_date
    from utils import parse_data, convert_str_to_datetime, parse_results, Namespace
    import argparse
    params = argparse.ArgumentParser()
    params.add_argument("--develop", type=bool, default=False,
                        help="Set the value to true during development")
    args = params.parse_args()
elif mode_ == "prod":
    from src.filters import filter_by_query, filter_by_to_date, filter_by_category, filter_by_apd, filter_by_country, filter_by_from_date
    from src.utils import parse_data, convert_str_to_datetime, parse_results, Namespace

    logger.info("Production Mode")
    args = Namespace(develop=False)

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

    convert_start = time.time()
    data_frame = pd.DataFrame(list(db.find({})))
    data_frame["timestamp"] = data_frame['timestamp'].apply(
        lambda x: convert_str_to_datetime(x))
    convert_end = time.time()

    logging.info(
        f"Database loaded in {(db_end - db_start)} seconds and converted to pandas dataframe in {(convert_end-convert_start)} seconds, with initial cache condition set to {INITIAL_CACHE}")

    data_frame.sort_values(by=["timestamp"],
                           ascending=False, inplace=True)

    logger.info(f"Cached {len(data_frame)} records")

    del db, client


# Starts the initial caching after 10 seconds
if args.develop:
    # load the dump data
    logger.info("Development mode")
    data_frame = pd.read_csv("./develop/development_data.csv")
    data_frame["timestamp"] = data_frame['timestamp'].apply(
        lambda x: convert_str_to_datetime(x))
    data_frame.sort_values(by=["timestamp"],
                           ascending=False, inplace=True)
    logging.info(f"Development Dataset Loaded")
else:
    # Production
    cache_job_start = scheduler.add_job(
        func=cache_data,
        trigger=IntervalTrigger(seconds=1),
        replace_existing=True)


def get_results(from_date: str, to_date: str, query: str = None, country:str= None, articles_per_day: int = 10) -> dict:
    '''
    Returns a dict of the search results with all the user constraints
    NOTE: Implement crawling when a topic has zero results
    '''

    global data_frame

    from_date = convert_str_to_datetime(from_date)
    to_date = convert_str_to_datetime(to_date)

    results = data_frame
    results = filter_by_from_date(from_date=from_date, local_df=results)
    results = filter_by_to_date(to_date=to_date, local_df=results)

    if country != None:
        results = filter_by_country(country=country, local_df=results)

    if query != None:
        results = filter_by_query(query=query, local_df=results)

    results = filter_by_apd(
        articles_per_day=articles_per_day, local_df=results)

    results = parse_results(raw_results=results)
    return_dict = {
        "len": len(results),
        "results": results
    }

    del results

    return return_dict


@app.route("/api", methods=["GET"])
def endpoint():
    '''Parses all the params and returns the result json'''

    # Initialization of the default params
    config = {
        "query":  None,
        "from_date": datetime.datetime.utcnow().date().strftime("%d/%m/%Y, 00:00:00"),
        "to_date": datetime.datetime.utcnow().date().strftime("%d/%m/%Y, 23:59:59"),
        "articles_per_day": 10,
        "country": None
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

    if convert_str_to_datetime(config["from_date"]) == None or convert_str_to_datetime(config["to_date"]) == None or \
            convert_str_to_datetime(config["from_date"]) > convert_str_to_datetime(config["to_date"]):

        if config["to_date"] != datetime.datetime.utcnow().date().strftime("%d/%m/%Y, 23:59:59") and \
                config["from_date"] == datetime.datetime.utcnow().date().strftime("%d/%m/%Y, 00:00:00"):

            config["from_date"] = data_frame.iloc[-1]["timestamp"].strftime(
                "%d/%m/%Y, %H:%M:%S")
        else:
            response = flask.Response()
            response.status_code = 422
            return response
    
    if config['country'] != None:
        config['country'] = config['country'].upper()

        if not config['country'] in ["US", "IN", "SG"]:
            response = flask.Response()
            response.status_code = 422
            return response

    results = get_results(
        query=query,
        from_date=config["from_date"],
        to_date=config["to_date"],
        articles_per_day=articles_per_day,
        country=config['country']
    )

    return flask.jsonify(results)


if __name__ == "__main__":

    # cache_data() # cache data at the startup
    app.run(debug=True, host="0.0.0.0", port=PORT)
