# tornado
import tornado.ioloop
import tornado.web
from   tornado.options import define, options
# mongodb
import pymongo
# json
import json
# objectid
from bson.errors import InvalidId
from bson.objectid import ObjectId

connection = pymongo.Connection('localhost')
db = connection['ex']

define("port", default=8888, help="run on the given port", type=int)

class RootHandler(tornado.web.RequestHandler):
	def get(self):
		self.write(str(db['commands'].find_one({})['_id']))

class CommandsHandler(tornado.web.RequestHandler):
	def get(self):		# todo: fix
		for command in db['commands'].find({}):
			command['_id'] = str(command['_id'])
			self.write(json.dumps(command)+'\n')

	def post(self):
		self.set_status(303)
		_id = db['commands'].insert({})
		self.set_header("Location", "/commands/"+str(_id))

class CommandHandler(tornado.web.RequestHandler):
	def get(self, _id):
		try:
			row = db['commands'].find_one({'$or': [{'_id': ObjectId(_id)}, {'name': _id}]})
		except:
			row = db['commands'].find_one({'name': _id})
		if row:
			row['_id'] = str(row['_id'])
			self.write(json.dumps(row))
		else:
			self.set_status(404)

	def put(self, _id):
		try:
			row = db['commands'].find_one({'$or': [{'_id': ObjectId(_id)}, {'name': _id}]})
		except:
			row = db['commands'].find_one({'name': _id})
		if row:
			try:
				data = json.loads(self.request.body.decode('utf-8'))
			except:
				self.set_status(400)
			else:
				allowed = ['name','description']
				_updates = {key : data[key] for key in set(allowed) & set(data.keys())}
				updates = {}
				for k,v in _updates.items():
					if type(v) is str:
						updates[k] = v
				db['commands'].update({'_id': row['_id']},{'$set':updates})
				# self.write(self.request.body.decode('utf-8')+"\n")
				# self.write(json.dumps(updates)+'\n')
		else:
			self.set_status(404)

	def delete(self, _id):
		try:
			row = db['commands'].find_one({'$or': [{'_id': ObjectId(_id)}, {'name': _id}]})
		except:
			row = db['commands'].find_one({'name': _id})
		if row:
			db['commands'].remove({'_id': row['_id']})
			self.set_status(410)
		else:
			self.set_status(404)

class ExamplesHandler(tornado.web.RequestHandler):
	def get(self):		# todo: fix
		for example in db['examples'].find({}):
			example['_id'] = str(example['_id'])
			self.write(json.dumps(example)+'\n')

	def post(self):
		self.set_status(303)
		_id = db['examples'].insert({})
		self.set_header("Location", "/examples/"+str(_id))

if __name__ == "__main__":
	tornado.options.parse_command_line()
	application = tornado.web.Application([
		("/", RootHandler),
		("/commands", CommandsHandler),
		("/commands/([a-z0-9]+)", CommandHandler),
		("/examples", ExamplesHandler),
	])
	application.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
