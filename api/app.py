import os

from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient

# FLASK Configs
app = Flask(__name__)
app.config["DEBUG"] = False
CORS(app)

# Environment Variables
PORT = int(os.environ.get("PORT", 10000))
USER = os.environ.get("user_")
PASS = os.environ.get("pass_")

MONGOSRV = f"mongodb+srv://{USER}:{PASS}@db-news-and-tweets.buxsd.mongodb.net/test"
client = MongoClient(MONGOSRV)
db = client.daily_feeds.feeds

@app.route("/api", methods=["GET"])
def endpoint():
    query = dict()
    params = request.args.to_dict()  # parse user params
    if "title" in params:
        query["title"] = {"$regex":params["title"]}
    if "start_date" in params:
        query["unix timestamp"] = {"$gte":int(params["start_date"])}
    if "end_date" in params:
        if "unix timestamp" not in query:
            query["unix timestamp"] = {}
        query["unix timestamp"]["$lte"] = int(params["end_date"])
    if "country" in params:
        query["country"] = params["country"]
    page_size = params.get("page_size",10)
    page = params.get("page",1)
    print(query)
    len_query_results = db.count_documents(query)
    print(len_query_results)
    
    query_results = db.find(query).sort("unix timestamp",-1).skip((page-1)*page_size if page>0 else 0).limit(page_size)
    query_results=list(query_results)
    for i in query_results:
        i["_id"] = str(i["_id"])
    response = {
        "records":query_results,
        "page_size":page_size,
        "page":page,
        "total_num_records":len_query_results
    }
    return jsonify(response)

app.run(host="0.0.0.0", port=PORT)
