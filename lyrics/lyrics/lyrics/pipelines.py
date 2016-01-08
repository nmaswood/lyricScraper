import pymongo
from scrapy.exceptions import DropItem

from scrapy.conf import settings

class MongoDBPipeline(object):

    def __init__(self):

        connection = pymongo.MongoClient(
                settings['MONGODB_SERVER'],
                settings['MONGODB_PORT']
                )
        db = connection[settings['MONGODB_DB']]
        self.connection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):

        self.connection.insert(dict(item))
        return item

class FilterWordsPipeline(object):

    words_to_filter = ['right now this does nothing:/']

    def process_item(self, item , spider):

        for word in self.words_to_filter:
            if word in unicode(item['url']).lower():
                raise DropItem("Contains forbidden word {}".format(word))
            else:
                return item

