import scrapy
import logging
from ..items import NewscastItem
import datetime
import pandas as pd
from hashlib import sha256


class newscast(scrapy.Spider):

    name = "top_stories"

    def __init__(self, *args, **kwargs):

        super(newscast, self).__init__(*args, **kwargs)

        for k, v in kwargs.items():
            print(k, v, '\n')
            setattr(self, k, v)

        TAGS = {
            "business": "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pIUWlnQVAB",
            "technology": "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB",
            "entertainment": "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNREpxYW5RU0FtVnVHZ0pWVXlnQVAB",
            "sports": "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp1ZEdvU0FtVnVHZ0pWVXlnQVAB",
            "science": "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp0Y1RjU0FtVnVHZ0pWVXlnQVAB",
            "health": "https://news.google.com/topics/CAAqIQgKIhtDQkFTRGdvSUwyMHZNR3QwTlRFU0FtVnVLQUFQAQ",
        }

        self.start_urls = [v+self.country_url for k, v in TAGS.items()]
        self.crawled = 0

        # instantiate the database and get the recent timestamp
        try:
            self.tstamp_check = self.db.find()[0]["timestamp"]
            raw_df = list(self.db.find({}))
            self.database_dataframe = pd.DataFrame(raw_df)
            self.database_dataframe.sort_values(
                by="unix timestamp", ascending=False, inplace=True)
            self.checkpoint_timestamp = self.database_dataframe.iloc[0]["unix timestamp"]
        except:
            logging.error("MongoDB database not loaded")
            self.tstamp_check = None

        del self.db

    def change_datetime_format(self, x: str) -> str:
        '''converts the datetime format'''

        try:
            datetime_object = datetime.datetime.strptime(
                x, "%Y-%m-%dT%H:%M:%SZ")
        except:
            logging.error(f"datetime conversion error: {x}")
            return x

        return datetime_object.strftime("%d/%m/%Y, %H:%M:%S")

    def parse(self, response):

        source = response.xpath(
            "//article[@class=' MQsxIb xTewfe R7GTQ keNKEd j7vNaf Cc0Z5d EjqUne']/div[@class='QmrVtf RD0gLb kybdz']/div[@class='SVJrMe']/a[@class='wEwyrc AVN2gc uQIVzc Sksgp']/text()").extract()
        title = response.xpath(
            "//article[@class=' MQsxIb xTewfe R7GTQ keNKEd j7vNaf Cc0Z5d EjqUne']/h3[@class='ipQwMb ekueJc RD0gLb']/a/text()").extract()

        url = []
        for u in response.xpath("//article[@class=' MQsxIb xTewfe R7GTQ keNKEd j7vNaf Cc0Z5d EjqUne']/h3[@class='ipQwMb ekueJc RD0gLb']/a[@class='DY5T1d RZIKme']/@href").extract():
            url.append("https://news.google.com"+u[1:])

        timestamp = response.xpath(
            "//article[@class=' MQsxIb xTewfe R7GTQ keNKEd j7vNaf Cc0Z5d EjqUne']/div[@class='QmrVtf RD0gLb kybdz']/div[@class='SVJrMe']/time[@class='WW6dff uQIVzc Sksgp']/@datetime").extract()

        cols = zip(source, title, url, timestamp)
        category = response.xpath(
            "//div[@class='xMjzl']/h2/text()").extract()[0]

        def set_item(src, headline, link, tstamp, category, country, hash_) -> NewscastItem:
            '''
            Sets all the fields and returns the item
            NOTE: To avoid redundant code

            '''

            item = NewscastItem()
            item["source"] = src
            item["title"] = headline
            item["url"] = link
            item["timestamp"] = tstamp
            item["category"] = category
            item["country"] = country
            item["hash"] = hash_

            return item

        for (src, headline, link, tstamp) in cols:

            str_ = ' <JOIN> '.join([headline, self.country])
            hash_ = sha256(str_.encode('utf-8')).hexdigest()
            tstamp = self.change_datetime_format(tstamp)

            if self.tstamp_check == None:
                self.crawled += 1
                item = set_item(src, headline, link, tstamp,
                                category, self.country, hash_)
                yield item

            else:

                # True -> the record already exists
                condn = hash_ in self.database_dataframe.hash.to_list()

                logging.warning(
                    f" Condition status: {condn}")

                if not condn:
                    self.crawled += 1
                    item = set_item(src, headline, link, tstamp,
                                    category, self.country, hash_)

                    yield item

        logging.warning(
            f"{self.country} : {category} - Total of {self.crawled} records added")
