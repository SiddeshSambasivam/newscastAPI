# Standard library imports
import os
import datetime
import json
import gc

# Third party imports
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from pymongo import MongoClient
import pymongo
import pandas as pd
import logging
from os.path import basename
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings
import tracemalloc


# Local library imports
from newscast.spiders.newscast import newscast

# setup logger for the pipeline
log = logging.getLogger(__name__)
logging.basicConfig(level="INFO", filename='crawl.log')
logging.getLogger('scrapy').setLevel(logging.WARNING)
logging.getLogger('scrapy').propagate = False


client = None
db = None
UNIX_TIMESTAMP = "unix timestamp"
CRAWL_LOG_PATH = "crawl.log"


def connect_to_database():

    global client
    global db

    client = MongoClient(
        f"mongodb+srv://admin:thisisatestpassword@db-news-and-tweets.buxsd.mongodb.net/test")
    db = client.daily_feeds.feeds


def send_email_log(crawl_len: int) -> None:
    '''
    sends the crawl log to the mail
    crawl_len: number of news articles crawled 
    '''

    log.info("Sending log to the project email...")

    gmailUser = 'dailybugle.project@gmail.com'
    gmailPassword = 'thisisatestpassword'
    recipient = 'dailybugle.project@gmail.com'

    with open("./timestamp.log") as file_:
        timestamp = file_.read()

    Message = f""
    Subject = f"LOG: {timestamp} - crawled {crawl_len}"

    msg = MIMEMultipart()
    msg['From'] = gmailUser
    msg['To'] = recipient
    msg['Subject'] = Subject
    msg.attach(MIMEText(Message))

    with open(CRAWL_LOG_PATH, "rb") as file:
        part = MIMEApplication(
            file.read(),
            Name=basename(CRAWL_LOG_PATH)
        )

    # After the file is closed
    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(
        CRAWL_LOG_PATH)
    msg.attach(part)

    mail_server = smtplib.SMTP('smtp.gmail.com', 587)
    mail_server.ehlo()
    mail_server.starttls()
    mail_server.ehlo()
    mail_server.login(gmailUser, gmailPassword)
    mail_server.sendmail(gmailUser, recipient, msg.as_string())
    mail_server.close()

    os.remove("crawl.log")
    log.info("Log mail sent")


def convert_str_to_datetime(s: str):
    '''Returns a datetime object from datetime string'''

    try:
        datetime_ = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        try:
            datetime_ = datetime.datetime.strptime(s, "%d/%m/%Y, %H:%M:%S")
        except ValueError:
            datetime_ = datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M:%SZ")

    return datetime_


def datetime_to_str(x: str) -> str:
    '''converts datetime object to string'''
    return x.strftime("%d/%m/%Y, %H:%M:%S")


def get_dataframe():
    '''Returns the dataframe from reading the crawled data'''

    # get the preprocesses database
    try:
        df = pd.read_csv('./crawl.csv')
    except pd.errors.EmptyDataError:
        return []

    df = df[df.category != 'category']  # Remove multiple headers

    # convert the timestamp to a uniform string for sorting
    df.timestamp = df.timestamp.apply(lambda x: convert_str_to_datetime(x))

    df.sort_values(by=['timestamp'], ascending=False, inplace=True)
    df[UNIX_TIMESTAMP] = df["timestamp"].apply(
        lambda x: datetime.datetime.timestamp(x))

    # ensure the elements are of type int
    df[UNIX_TIMESTAMP] = list(
        map(int, df[UNIX_TIMESTAMP].to_list()))

    df["timestamp"] = df.timestamp.apply(lambda x: datetime_to_str(x))

    return df


def to_database() -> None:
    '''
    Writes the crawled data to the database
    '''
    df = get_dataframe()

    number_of_records_crawled = len(df)

    if isinstance(df, list):
        log.info("No records to add")
        os.remove("crawl.csv")
        return None

    log.info(f"Inserting {number_of_records_crawled} records to the database")

    records = json.loads(df.T.to_json()).values()

    global db
    db.insert(records)

    database_dataframe = pd.DataFrame(list(db.find({})))
    database_dataframe.sort_values(
        by="unix timestamp", ascending=False, inplace=True)
    checkpoint_timestamp = database_dataframe.iloc[0]["timestamp"]

    del db  # bson takes up a lot of memory

    with open("timestamp.log", 'w') as file_:
        file_.write(checkpoint_timestamp)

    table = database_dataframe["hash"].value_counts().rename_axis(
        'unique_values').reset_index(name='counts')

    if len(table[table.counts > 1]) == 0:
        logging.info(f"No duplicate records in database")
    else:
        logging.warning(
            f"There are {len(table[table.counts > 1])} duplicate records")

    del df, checkpoint_timestamp, records, database_dataframe, table
    logging.info("time log written")

    os.remove("crawl.csv")

    send_email_log(number_of_records_crawled)
    del number_of_records_crawled


def crawl_data():
    '''Crawls news data from the web'''

    connect_to_database()  # load the mongoDB database
    process = CrawlerProcess(get_project_settings())

    # countries = ["SG"]  # For development purposes
    countries = "US,SG,IN".split(',')

    for country in countries:

        baseurl = f"?hl=en-{country}&gl={country}&ceid={country}%3Aen"

        process.crawl(newscast, country_url=baseurl, country=country, db=db)
        log.info(f"Crawl complete for the country {country}...")

    process.start(stop_after_crawl=True)
    del process


def run():

    log.info("12 hours crawl starting...")

    crawl_data()  # crawl the data from web
    # write the data to the mongoDB database and send the logs to the email
    to_database()

    log.info("12 hours crawl complete")


if __name__ == "__main__":

    tracemalloc.start()
    gc.collect()
    run()
    gc.collect()
    current, peak = tracemalloc.get_traced_memory()

    print(
        f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")

    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')

    print("[ Top 10 ]")
    for stat in top_stats[:10]:
        print(stat)
    tracemalloc.stop()
