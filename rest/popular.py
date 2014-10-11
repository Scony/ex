import tornado.web
import pymongo
import json
from bson.objectid import ObjectId

connection = pymongo.Connection('localhost')
db = connection['ex']

class PopularCommandsHandler(tornado.web.RequestHandler):
	def get(self):
		jcommands = []
		for command in db['commands'].find({}):
			command['_id'] = str(command['_id'])
			jcommands.append(command)
		self.write(json.dumps(jcommands[:2])+'\n')

class PopularExamplesHandler(tornado.web.RequestHandler):
	def get(self):
		jexamples = []
		for example in db['examples'].find({}):
			example['_id'] = str(example['_id'])
			jexamples.append(example)
		self.write(json.dumps(jexamples[:2])+'\n')
