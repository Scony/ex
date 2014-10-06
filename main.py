# tornado
import tornado.ioloop
import tornado.web
from   tornado.options import define, options
# mongodb
import pymongo
# json
import json
# objectid
from bson.objectid import ObjectId
# os
import os

connection = pymongo.Connection('localhost')
db = connection['ex']

define("port", default=8888, help="run on the given port", type=int)

class RootHandler(tornado.web.RequestHandler): # todo: change
	def get(self):
		self.write(str(db['commands'].find_one({})['_id']))

class CommandsHandler(tornado.web.RequestHandler):
	def get(self):
		jcommands = []
		for command in db['commands'].find({}):
			command['_id'] = str(command['_id'])
			jcommands.append(command)
		self.write(json.dumps(jcommands)+'\n')

	def post(self):
		self.set_status(201)
		_id = db['commands'].insert({'name': '', 'description': ''})
		self.set_header("Location", "/commands/"+str(_id))

class PopularCommandsHandler(tornado.web.RequestHandler):
	def get(self):
		jcommands = []
		for command in db['commands'].find({}):
			command['_id'] = str(command['_id'])
			jcommands.append(command)
		self.write(json.dumps(jcommands[:2])+'\n')

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
				if 'name' in updates and len(updates['name']) and db['commands'].find_one({'name': updates['name']}):
					self.set_status(409)
				else:
					db['commands'].update({'_id': row['_id']},{'$set':updates})
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
			jexamples = []
			for example in examples:
				votes = db['votes'].find({'example': example['_id']})
				score = 0;
				for vote in votes:
					score += vote['value']
				example['_id'] = str(example['_id'])
				example['score'] = score
				jexamples.append(example)
			decorated = [(dict_['score'], dict_) for dict_ in jexamples]
			try:
				decorated.sort()
			except:
				pass
			decorated.reverse()
			jexamples = [dict_ for (key, dict_) in decorated]
			self.write(json.dumps(jexamples)+'\n')
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
	def get(self):
		jexamples = []
		for example in db['examples'].find({}):
			example['_id'] = str(example['_id'])
			jexamples.append(example)
		self.write(json.dumps(jexamples)+'\n')

	def post(self):
		self.set_status(201)
		_id = db['examples'].insert({'example': '', 'description': ''})
		self.set_header("Location", "/examples/"+str(_id))

class PopularExamplesHandler(tornado.web.RequestHandler):
	def get(self):
		jexamples = []
		for example in db['examples'].find({}):
			example['_id'] = str(example['_id'])
			jexamples.append(example)
		self.write(json.dumps(jexamples[:2])+'\n')

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
			jvotes = []
			for vote in db['votes'].find({'example': row['_id'], 'value': 1}):
				vote['_id'] = str(vote['_id'])
				vote['example'] = str(vote['example'])
				jvotes.append(vote)
			self.write(json.dumps(jvotes)+'\n')
		else:
			self.set_status(404)

	def post(self, _id):
		row = db['examples'].find_one({'_id': ObjectId(_id)})
		if row:
			keys = {'example': row['_id'], 'ip': self.request.remote_ip}
			data = {'example': row['_id'], 'ip': self.request.remote_ip, 'value': 1}
			db['votes'].update(keys, data, True)
		else:
			self.set_status(404)

class ExampleDownvotesHandler(tornado.web.RequestHandler):
	def get(self, _id):
		row = db['examples'].find_one({'_id': ObjectId(_id)})
		if row:
			jvotes = []
			for vote in db['votes'].find({'example': row['_id'], 'value': -1}):
				vote['_id'] = str(vote['_id'])
				vote['example'] = str(vote['example'])
				jvotes.append(vote)
			self.write(json.dumps(jvotes)+'\n')
		else:
			self.set_status(404)

	def post(self, _id):
		row = db['examples'].find_one({'_id': ObjectId(_id)})
		if row:
			keys = {'example': row['_id'], 'ip': self.request.remote_ip}
			data = {'example': row['_id'], 'ip': self.request.remote_ip, 'value': -1}
			db['votes'].update(keys, data, True)
		else:
			self.set_status(404)

class ExampleVoteHandler(tornado.web.RequestHandler):
	def get(self, _id, _id2):
		row = db['examples'].find_one({'_id': ObjectId(_id)})
		if row:
			row2 = db['votes'].find_one({'example': row['_id'], '_id': ObjectId(_id2)})
			if row2:
				row2['_id'] = str(row2['_id'])
				row2['example'] = str(row2['example'])
				self.write(json.dumps(row2)+'\n')
			else:
				self.set_status(404)
		else:
			self.set_status(404)

	def delete(self, _id, _id2):
		row = db['examples'].find_one({'_id': ObjectId(_id)})
		if row:
			row2 = db['votes'].find_one({'example': row['_id'], '_id': ObjectId(_id2)})
			if row2:
				if row2['ip'] == self.request.remote_ip:
					db['votes'].remove({'example': row['_id'], '_id': ObjectId(_id2), 'ip': self.request.remote_ip})
				else:
					self.set_status(403)
			else:
				self.set_status(404)
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
			jcommands = []
			for command in commands:
				command['_id'] = str(command['_id'])
				jcommands.append(command)
			self.write(json.dumps(jcommands)+'\n')
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
		jvotes = []
		for vote in db['votes'].find({}):
			vote['_id'] = str(vote['_id'])
			vote['example'] = str(vote['example'])
			jvotes.append(vote)
		self.write(json.dumps(jvotes)+'\n')

class TestHandler(tornado.web.RequestHandler):
	def get(self):
		self.set_status(303)
		self.set_header("Location", "/commands")

if __name__ == "__main__":
	tornado.options.parse_command_line()
	application = tornado.web.Application([
		("/", RootHandler),
		("/commands", CommandsHandler),
		("/commands/popular", PopularCommandsHandler),
		("/commands/([a-z0-9]+)", CommandHandler),
		("/commands/([a-z0-9]+)/examples", CommandExamplesHandler),
		("/commands/([a-z0-9]+)/examples/([a-f0-9]{24})", CommandExampleHandler),
		("/examples", ExamplesHandler),
		("/examples/popular", PopularExamplesHandler),
		("/examples/([a-f0-9]{24})", ExampleHandler),
		("/examples/([a-f0-9]{24})/upvotes", ExampleUpvotesHandler),
		("/examples/([a-f0-9]{24})/upvotes/([a-f0-9]{24})", ExampleVoteHandler),
		("/examples/([a-f0-9]{24})/downvotes", ExampleDownvotesHandler),
		("/examples/([a-f0-9]{24})/downvotes/([a-f0-9]{24})", ExampleVoteHandler),
		("/examples/([a-f0-9]{24})/commands", ExampleCommandsHandler),
		("/examples/([a-f0-9]{24})/commands/([a-z0-9]+)", ExampleCommandHandler),
		("/votes", VotesHandler),
		("/test", TestHandler),
		("/webapp/()$", tornado.web.StaticFileHandler, {'path':'./index.html'}),
		("/webapp/(.*)", tornado.web.StaticFileHandler, {'path':'./'}),
	])
	application.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
