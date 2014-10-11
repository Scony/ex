import tornado.web
import pymongo
import json
from bson.objectid import ObjectId

connection = pymongo.Connection('localhost')
db = connection['ex']

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
