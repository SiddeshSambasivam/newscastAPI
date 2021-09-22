import pymongo
from itemadapter import ItemAdapter


class MongoDBPipeline:

    collection_name = "test_feed"

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DB", "items"),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):

        # TODO: Optimize the code below
        item_count_in_db = (
            self.db[self.collection_name].find({"hash": item.hash}).count()
        )

        if item_count_in_db == 0:
            self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())

        return item
