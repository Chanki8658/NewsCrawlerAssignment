ITEM_PIPELINES = {'dirbot.pipelines.FilterWordsPipeline': 1}
SPIDER_MODULES = ['dirbot.spiders']
NEWSPIDER_MODULE = 'dirbot.spiders'
DEFAULT_ITEM_CLASS = 'dirbot.items.Website'

#Avoid <urlopen error timed out>
AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""

#AWS
MONGODB_SERVER = '@ec2-54-144-216-55.compute-1.amazonaws.com'
MONGODB_PORT = 27017
MONGODB_DB = 'test'
MONGODB_COLLECTION = 'news'