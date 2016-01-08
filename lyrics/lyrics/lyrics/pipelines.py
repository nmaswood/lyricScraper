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

        try:

            genre = item["genre"]
            title = item["title"]
            url = item["url"]
            if  genre != "" and title != ""and  url != "":

                self.connection.insert(dict(item))
        except:

            url_two = item["url_two"]
            lyrics = item["lyrics"]
            song_name = item["song_name"]
            artist = item["artist"]

            if lyrics != "" and url_two != "" and song_name != "" and artist != "":
                self.connection.insert(dict(item))
        return item
