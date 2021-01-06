import os
import logging
from datetime import datetime
import re

import flask
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
import pymongo
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit

app = Flask(__name__)
app.config["DEBUG"] = False
CORS(app)

logger = logging.getLogger()
apscheduler_logger = logging.getLogger("apscheduler").setLevel(logging.WARNING)
logging.basicConfig(level="INFO")

PORT = int(os.environ.get("PORT", 10000))
user_ = os.environ.get("user_")
pass_ = os.environ.get("pass_")


data_frame = None # local caching

scheduler = BackgroundScheduler()
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

def cache_data(start=True):

    global data_frame

    # mongoDB database
    client = MongoClient(
        f"mongodb+srv://{user_}:{pass_}@db-news-and-tweets.buxsd.mongodb.net/test")
    db = client.daily_feeds.feeds
    data_frame = pd.DataFrame(list(db.find({})))
    data_frame.sort_values(by=["unix timestamp"], inplace=True)
    # data_frame["title"] = list(map(str.lower, data_frame["title"].to_list()))
    logger.info(f"Cached {len(data_frame)} records")    

    del db, client

scheduler.add_job(
    func=cache_data,
    trigger=IntervalTrigger(seconds=5),
    # trigger=IntervalTrigger(minutes=75),
    replace_existing=True)


def parse_data(record:list) -> dict:
    '''Converts a record in a dataframe to dict'''

    cols = ["title", "source", "timestamp", "url", "category", "country"]
    result = dict()
    for k, v in zip(cols, record):
        result.update({k:v})
        
    return result

def query_search(query:str):

    query = query.lower()
    result_frame = data_frame[data_frame['title'].str.contains(query, flags=re.IGNORECASE, regex=True)]

    return result_frame

def get_results(from_date:datetime, to_date:datetime, query:str = None, articles_per_day:int=10) -> dict:
    '''Returns a dict with a list of all the results based on params'''
    print("query: ", query)
    if query == None:
        '''In case no query provided, return the top 10 recent headlines'''

        if from_date != datetime(datetime.utcnow().year, datetime.utcnow().month, datetime.utcnow().day) or to_date != None:
            "return the top results in the given timeframe"
            pass

        results = [ parse_data(row[0]) for row in zip(data_frame.iloc[:articles_per_day][["title", "source", "timestamp", "url", "category", "country"]].to_numpy())]
        
        return {"results":results}
    
    results = [ parse_data(row[0]) for row in zip(query_search(query).iloc[:articles_per_day][["title", "source", "timestamp", "url", "category", "country"]].to_numpy())]
    
    return {"results":results}

@app.route("/api", methods=["GET"])
def endpoint():
    '''parses all the params and returns the result json'''

    # Initialization of the default params
    config = {
        "query":  None,
        "from_date": datetime(datetime.utcnow().year, datetime.utcnow().month, datetime.utcnow().day),
        "to_date": None,
        "articles_per_day": 10,
    }
    # -1 - Most recent
    #  1 - Least recent 
    sortBy = -1 
    
    params = request.args.to_dict() # parse user params
    for k, v in params.items():
        if k not in config:
            response = flask.Response()
            response.status_code = 422
            return response

        config[k] = v

    query = config["query"]
    from_date = config["from_date"]
    to_date = config["to_date"]
    articles_per_day = int(config["articles_per_day"])

    results = get_results(
        query= query, 
        from_date= from_date, 
        to_date= to_date, 
        articles_per_day= articles_per_day
        )
    return flask.jsonify(results)


if __name__ == "__main__":

    print(user_, pass_)
    cache_data() # cache data at the startup
    app.run(debug=True, host="0.0.0.0", port=PORT)
