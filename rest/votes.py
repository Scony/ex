import tornado.web
import pymongo
import json
from bson.objectid import ObjectId

connection = pymongo.Connection('localhost')
db = connection['ex']

class VotesHandler(tornado.web.RequestHandler):
	def get(self):
		jvotes = []
		for vote in db['votes'].find({}):
			vote['_id'] = str(vote['_id'])
			vote['example'] = str(vote['example'])
			jvotes.append(vote)
		self.write(json.dumps(jvotes)+'\n')
