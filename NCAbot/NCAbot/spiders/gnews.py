from enum import Enum
from dataclasses import dataclass, field
from typing import Type, List

import scrapy

from ..items import NewscastItem
from ..utils import change_datetime_format, generate_hash, get_unix_timestamp


class GNewsCategoryTypes(Enum):
    """
    Enum class for the different types of google news categories.
    """

    BUSINESS = "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pIUWlnQVAB"
    TECHNOLOGY = "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB"
    ENTERTAINMENT = "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNREpxYW5RU0FtVnVHZ0pWVXlnQVAB"
    SPORTS = "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp1ZEdvU0FtVnVHZ0pWVXlnQVAB"
    SCIENCE = "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp0Y1RjU0FtVnVHZ0pWVXlnQVAB"
    HEALTH = "https://news.google.com/topics/CAAqIQgKIhtDQkFTRGdvSUwyMHZNR3QwTlRFU0FtVnVLQUFQAQ"


@dataclass
class GNewsCountry:

    country: str
    source_xpath: str = "//article[@class=' MQsxIb xTewfe R7GTQ keNKEd j7vNaf Cc0Z5d EjqUne']/div[@class='QmrVtf RD0gLb kybdz']/div[@class='SVJrMe']/a[@class='wEwyrc AVN2gc uQIVzc Sksgp']/text()"
    title_xpath: str = "//article[@class=' MQsxIb xTewfe R7GTQ keNKEd j7vNaf Cc0Z5d EjqUne']/h3[@class='ipQwMb ekueJc RD0gLb']/a/text()"
    url_xpath: str = "//article[@class=' MQsxIb xTewfe R7GTQ keNKEd j7vNaf Cc0Z5d EjqUne']/h3[@class='ipQwMb ekueJc RD0gLb']/a[@class='DY5T1d RZIKme']/@href"
    timestamp_xpath: str = "//article[@class=' MQsxIb xTewfe R7GTQ keNKEd j7vNaf Cc0Z5d EjqUne']/div[@class='QmrVtf RD0gLb kybdz']/div[@class='SVJrMe']/time[@class='WW6dff uQIVzc Sksgp']/@datetime"
    category_xpath: str = "//div[@class='xMjzl']/h2/text()"
    category_urls: List[str] = field(init=False)

    def __post_init__(self):
        """Initialize URLs for all categories"""
        query_value = (
            f"?hl=en-{self.country}&gl={self.country}&ceid={self.country}%3Aen"
        )
        category_urls = []

        for category in GNewsCategoryTypes:
            category_urls.append(category.value + query_value)

        self.category_urls = category_urls


class GoogleNewsSpider(scrapy.Spider):
    """Spider to scrape content from google news"""

    name = "googleNews"
    allowed_domains = ["https://news.google.com"]

    def __init__(self, gnew_country_obj: Type[GNewsCountry]) -> None:
        super(GoogleNewsSpider, self).__init__()
        self.gnew_country_obj = gnew_country_obj
        self.start_urls = self.gnew_country_obj.category_urls

    def parse(self, response):

        source = response.xpath(self.gnew_country_obj.source_xpath).extract()
        title = response.xpath(self.gnew_country_obj.title_xpath).extract()

        urls = [
            self.allowed_domains[0] + url[1:]
            for url in response.xpath(self.gnew_country_obj.url_xpath).extract()
        ]

        timestamp = response.xpath(self.gnew_country_obj.timestamp_xpath).extract()
        category = response.xpath(self.gnew_country_obj.category_xpath).extract()[0]

        cols = zip(source, title, urls, timestamp)
        for src, headline, link, tstamp in cols:

            hash_value = generate_hash(f"{headline}/{self.gnew_country_obj.country}")
            timestamp_object, timestamp = change_datetime_format(tstamp)
            unix_timestamp = get_unix_timestamp(timestamp_object)

            item = NewscastItem(
                src,
                headline,
                link,
                timestamp,
                unix_timestamp,
                category,
                self.gnew_country_obj.country,
                hash_value,
            )

            yield item
