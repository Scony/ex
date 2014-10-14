import pymongo

connection = pymongo.Connection('localhost')
db = connection['ex']
