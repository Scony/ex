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

class CommandExamplesHandler(tornado.web.RequestHandler):
	def get(self, _id):
		try:
			row = db['commands'].find_one({'$or': [{'_id': ObjectId(_id)}, {'name': _id}]})
		except:
			row = db['commands'].find_one({'name': _id})
		if row:
			binds = db['binds'].find({'command': row['_id']})
			ids = []
			for b in binds:
				ids.append(b['example'])
			examples = db['examples'].find({'_id': {'$in': ids}})
			for example in examples:
				example['_id'] = str(example['_id'])
				self.write(json.dumps(example)+'\n')
		else:
			self.set_status(404)

	def post(self, _id):
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
				if 'example' in data and type(data['example']) is str:
					try:
						row2 = db['examples'].find_one({'_id': ObjectId(data['example'])})
					except:
						self.set_status(400)
					else:
						data = {'command': row['_id'], 'example': ObjectId(data['example'])}
						db['binds'].update(data, data, True)
				else:
					self.set_status(400)
		else:
			self.set_status(404)

class CommandExampleHandler(tornado.web.RequestHandler):
	def get(self, _id, _id2):
		try:
			row = db['commands'].find_one({'$or': [{'_id': ObjectId(_id)}, {'name': _id}]})
		except:
			row = db['commands'].find_one({'name': _id})
		if row:
			row2 = db['binds'].find_one({'command': row['_id'], 'example': ObjectId(_id2)})
			if row2:
				self.set_status(303)
				self.set_header("Location", "/examples/"+_id2)				
			else:
				self.set_status(404)
		else:
			self.set_status(404)

	def delete(self, _id, _id2):
		try:
			row = db['commands'].find_one({'$or': [{'_id': ObjectId(_id)}, {'name': _id}]})
		except:
			row = db['commands'].find_one({'name': _id})
		if row:
			row2 = db['binds'].find_one({'command': row['_id'], 'example': ObjectId(_id2)})
			if row2:
				db['binds'].remove({'command': row['_id'], 'example': ObjectId(_id2)})
				self.set_status(410)
			else:
				self.set_status(404)
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

class ExampleHandler(tornado.web.RequestHandler):
	def get(self, _id):
		row = db['examples'].find_one({'_id': ObjectId(_id)})
		if row:
			row['_id'] = str(row['_id'])
			self.write(json.dumps(row))
		else:
			self.set_status(404)

	def put(self, _id):
		row = db['examples'].find_one({'_id': ObjectId(_id)})
		if row:
			try:
				data = json.loads(self.request.body.decode('utf-8'))
			except:
				self.set_status(400)
			else:
				allowed = ['example','description']
				_updates = {key : data[key] for key in set(allowed) & set(data.keys())}
				updates = {}
				for k,v in _updates.items():
					if type(v) is str:
						updates[k] = v
				db['examples'].update({'_id': row['_id']},{'$set':updates})
				# self.write(self.request.body.decode('utf-8')+"\n")
				# self.write(json.dumps(updates)+'\n')
		else:
			self.set_status(404)

	def delete(self, _id):
		row = db['examples'].find_one({'_id': ObjectId(_id)})
		if row:
			db['examples'].remove({'_id': row['_id']})
			self.set_status(410)
		else:
			self.set_status(404)

class ExampleUpvotesHandler(tornado.web.RequestHandler):
	def get(self, _id):
		row = db['examples'].find_one({'_id': ObjectId(_id)})
		if row:
			for vote in db['votes'].find({'example': row['_id']}):
				vote['_id'] = str(vote['_id'])
				self.write(json.dumps(vote)+'\n')
		else:
			self.set_status(404)

class ExampleCommandsHandler(tornado.web.RequestHandler):
	def get(self, _id):
		row = db['examples'].find_one({'_id': ObjectId(_id)})
		if row:
			binds = db['binds'].find({'example': row['_id']})
			ids = []
			for b in binds:
				ids.append(b['command'])
			commands = db['commands'].find({'_id': {'$in': ids}})
			for command in commands:
				command['_id'] = str(command['_id'])
				self.write(json.dumps(command)+'\n')
		else:
			self.set_status(404)

	def post(self, _id):
		row = db['examples'].find_one({'_id': ObjectId(_id)})
		if row:
			try:
				data = json.loads(self.request.body.decode('utf-8'))
			except:
				self.set_status(400)
			else:
				if 'command' in data and type(data['command']) is str:
					try:
						row2 = db['commands'].find_one({'$or': [{'_id': ObjectId(data['command'])}, {'name': data['command']}]})
					except:
						row2 = db['commands'].find_one({'name': data['command']})
					if row2:
						data = {'example': row['_id'], 'command': row2['_id']}
						db['binds'].update(data, data, True)
					else:
						self.set_status(400)
				else:
					self.set_status(400)
		else:
			self.set_status(404)

class ExampleCommandHandler(tornado.web.RequestHandler):
	def get(self, _id, _id2):
		row = db['examples'].find_one({'_id': ObjectId(_id)})
		if row:
			try:
				row2 = db['commands'].find_one({'$or': [{'_id': ObjectId(_id2)}, {'name': _id2}]})
			except:
				row2 = db['commands'].find_one({'name': _id2})
				if row2:
					bind = db['binds'].find_one({'example': ObjectId(_id), 'command': row2['_id']})
					if bind:
						self.set_status(303)
						self.set_header("Location", "/commands/"+_id2)
					else:
						self.set_status(404)
				else:
					self.set_status(404)
		else:
			self.set_status(404)

	def delete(self, _id, _id2):
		row = db['examples'].find_one({'_id': ObjectId(_id)})
		if row:
			try:
				row2 = db['commands'].find_one({'$or': [{'_id': ObjectId(_id2)}, {'name': _id2}]})
			except:
				row2 = db['commands'].find_one({'name': _id2})
				if row2:
					bind = db['binds'].find_one({'example': ObjectId(_id), 'command': row2['_id']})
					if bind:
						db['binds'].remove({'example': ObjectId(_id), 'command': row2['_id']})
						self.set_status(410)
					else:
						self.set_status(404)
				else:
					self.set_status(404)
		else:
			self.set_status(404)

class VotesHandler(tornado.web.RequestHandler):
	def get(self):
		for vote in db['votes'].find({}):
			vote['_id'] = str(vote['_id'])
			self.write(json.dumps(vote)+'\n')

class TestHandler(tornado.web.RequestHandler):
	def get(self):
		self.set_status(303)
		self.set_header("Location", "/commands")

if __name__ == "__main__":
	tornado.options.parse_command_line()
	application = tornado.web.Application([
		("/", RootHandler),
		("/commands", CommandsHandler),
		("/commands/([a-z0-9]+)", CommandHandler),
		("/commands/([a-z0-9]+)/examples", CommandExamplesHandler),
		("/commands/([a-z0-9]+)/examples/([a-f0-9]{24})", CommandExampleHandler),
		("/examples", ExamplesHandler),
		("/examples/([a-f0-9]{24})", ExampleHandler),
		("/examples/([a-f0-9]{24})/upvotes", ExampleUpvotesHandler),
		# ("/examples/([a-f0-9]{24})/upvotes/([a-f0-9]{24})", ExampleUpvoteHandler),
		# ("/examples/([a-f0-9]{24})/downvotes", ExampleDownvotesHandler),
		# ("/examples/([a-f0-9]{24})/downvotes/([a-f0-9]{24})", ExampleDownvoteHandler),
		("/examples/([a-f0-9]{24})/commands", ExampleCommandsHandler),
		("/examples/([a-f0-9]{24})/commands/([a-z0-9]+)", ExampleCommandHandler),
		("/votes", VotesHandler),
		("/test", TestHandler),
	])
	application.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
