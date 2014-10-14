import tornado.web
import json
from rest.connection import *
from bson.objectid import ObjectId

class CommandsHandler(tornado.web.RequestHandler):
	def get(self):
		jcommands = []
		for command in db['commands'].find({}):
			binds = db['binds'].find({'command': command['_id']})
			examples = 0;
			for bind in binds:
				examples += 1
			command['_id'] = str(command['_id'])
			command['examples'] = examples
			jcommands.append(command)
		self.write(json.dumps(jcommands)+'\n')

	def post(self):
		self.set_status(201)
		_id = db['commands'].insert({'name': '', 'description': ''})
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
				ok = True
				for key in allowed:
					if key in row and len(row[key]) != 0:
						ok = False
				if ok:
					_updates = {key : data[key] for key in set(allowed) & set(data.keys())}
					updates = {}
					for k,v in _updates.items():
						if type(v) is str:
							updates[k] = v
					db['commands'].update({'_id': row['_id']},{'$set':updates})
				else:
					self.set_status(409)
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
