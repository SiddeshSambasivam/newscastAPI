from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings

from NCAbot.spiders.gnews import GoogleNewsSpider, GNewsCountry

# TODO: Dockerize the crawling process
# TODO: Refactor code to add more countries
process = CrawlerProcess(get_project_settings())

gnew_country_obj = GNewsCountry("IN")
process.crawl(GoogleNewsSpider, gnew_country_obj=gnew_country_obj)

process.start(stop_after_crawl=True)
