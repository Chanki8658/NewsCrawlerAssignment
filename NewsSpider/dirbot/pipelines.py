from scrapy.exceptions import DropItem
from scrapy.conf import settings
import pymongo
from pymongo import Connection
from pymongo import MongoClient

class FilterWordsPipeline(object):
    """A pipeline for filtering out items which contain certain words in their
    description"""

    # put all words in lowercase
    words_to_filter = ['politics', 'religion']

    def __init__(self):
        connection = MongoClient('mongodb://ec2-54-144-216-55.compute-1.amazonaws.com:27017')
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

        #clean up previous one before new crawling
        self.collection.remove({})

    def process_item(self, item, spider):
        valid = True
        for word in self.words_to_filter:
            if word in unicode(item['description']).lower():
                valid = False
                raise DropItem("Contains forbidden word: %s" % word)

        if valid:
            self.collection.insert(dict(item))

        return item